import secrets
from django.utils import timezone
from django.db import transaction as db_transaction
from celery import shared_task
from .models import Partie, Ticker
from payments.models import Transaction
from payments.services import rembourser_mobile_money
from support.models import Notification


@shared_task
def cloturer_parties_expirees():
    """
    Tâche planifiée (toutes les 60s) : vérifie les parties dont l'échéance
    est dépassée et encore "en_cours", puis déclenche le tirage ou le
    remboursement selon si l'objectif est atteint.
    """
    parties_expirees = Partie.objects.filter(
        statut="en_cours",
        date_fin__lte=timezone.now(),
    )

    for partie in parties_expirees:
        if partie.montant_collecte >= partie.prix_produit:
            _tirer_gagnant(partie)
        else:
            _rembourser_partie(partie)


def _tirer_gagnant(partie):
    """
    Tire un ticket gagnant au hasard parmi les tickets valides.
    secrets.choice() (pas random.choice()) : générateur cryptographique,
    non prévisible — essentiel pour la crédibilité du tirage.
    """
    tickets_valides = list(partie.tickets.filter(statut="valide"))

    if not tickets_valides:
        # Cas limite : objectif atteint mais aucun ticket valide
        # (ex. tous remboursés entre-temps) → on annule par sécurité
        _rembourser_partie(partie)
        return

    with db_transaction.atomic():
        gagnant = secrets.choice(tickets_valides)
        gagnant.statut = "gagnant"
        gagnant.save()

        partie.ticket_gagnant = gagnant
        partie.statut = "reussie"
        partie.save()

        # Notifie tous les participants du résultat
        for ticket in tickets_valides:
            Notification.objects.create(
                user=ticket.user,
                type_notification="resultat",
                message=(
                    f"Félicitations, vous avez gagné {partie.titre} !"
                    if ticket.id == gagnant.id
                    else f"Le tirage de {partie.titre} est terminé. Ce n'est pas vous cette fois."
                ),
            )


def _rembourser_partie(partie):
    """
    Objectif non atteint à l'échéance : rembourse tous les participants
    et annule la partie.
    """
    with db_transaction.atomic():
        tickets_a_rembourser = partie.tickets.exclude(statut="rembourse")

        for ticket in tickets_a_rembourser:
            resultat = rembourser_mobile_money(
                montant=partie.prix_ticket,
                numero_telephone=ticket.user.phone_number,
            )
            Transaction.objects.create(
                user=ticket.user,
                partie=partie,
                montant=partie.prix_ticket,
                type_transaction="remboursement",
                reference_mobile_money=resultat["reference"],
                statut="reussie",
            )
            ticket.statut = "rembourse"
            ticket.save()

            Notification.objects.create(
                user=ticket.user,
                type_notification="remboursement",
                message=f"La partie {partie.titre} a été annulée. Vous avez été remboursé.",
            )

        partie.statut = "annulee"
        partie.save()


@shared_task
def notifier_derniere_minute():
    """
    Tâche planifiée (toutes les 60s) : envoie une notification à tous les
    participants d'une partie dont l'objectif est atteint et qui entre
    dans ses 15 dernières minutes — une seule fois par partie.
    """
    seuil = timezone.now() + timezone.timedelta(minutes=15)

    parties_concernees = Partie.objects.filter(
        statut="en_cours",
        date_fin__lte=seuil,
        date_fin__gt=timezone.now(),
        notification_finale_envoyee=False,
    )

    for partie in parties_concernees:
        if partie.montant_collecte < partie.prix_produit:
            continue  # objectif pas encore atteint, pas de notif finale
        for ticket in partie.tickets.filter(statut="valide"):
            Notification.objects.create(
                user=ticket.user,
                type_notification="fin_partie",
                message=f"Dernière chance ! Le tirage de {partie.titre} a lieu dans quelques minutes.",
            )

        partie.notification_finale_envoyee = True
        partie.save()