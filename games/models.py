import uuid
from django.db import models
from django.conf import settings
# settings.AUTH_USER_MODEL pointe vers accounts.User (notre modèle personnalisé)
# → on l'utilise au lieu d'importer User directement, pour rester flexible


class Partie(models.Model):
    """
    Représente un produit mis en jeu (téléphone, voiture, maison...)
    avec son prix, le prix du ticket, et la progression de la collecte.
    """

    # Liste des statuts possibles pour une partie.
    # Le premier élément = valeur stockée en base, le second = libellé lisible.
    STATUT_CHOICES = [
        ("en_cours", "En cours"),      # la partie tourne, on vend encore des tickets
        ("reussie", "Réussie"),        # objectif atteint, tirage effectué
        ("annulee", "Annulée"),        # objectif non atteint, remboursement fait
    ]

    titre = models.CharField(max_length=200)
    # Texte court, ex. "iPhone 16 Pro Max"

    description = models.TextField()
    # Texte long sans limite de taille, pour détailler le produit

    photo = models.ImageField(upload_to="parties/", blank=True, null=True)
    # Image du produit. upload_to="parties/" = rangée dans media/parties/
    # blank=True (facultatif dans les formulaires), null=True (facultatif en base)

    prix_produit = models.DecimalField(max_digits=12, decimal_places=2)
    # Prix cible du produit. DecimalField (pas FloatField) car on manipule
    # de l'argent : évite les erreurs d'arrondi liées aux nombres flottants.
    # max_digits=12 → jusqu'à 12 chiffres au total, decimal_places=2 → 2 après la virgule

    prix_ticket = models.DecimalField(max_digits=10, decimal_places=2)
    # Prix unitaire d'un ticket, même logique que prix_produit
    notification_finale_envoyee = models.BooleanField(default=False)
    montant_collecte = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Total déjà collecté sur cette partie. Mis à jour à chaque achat de ticket
    # (via le code métier, pas automatiquement par Django).
    # default=0 → une partie démarre toujours à 0 FCFA collecté

    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    # Bornes temporelles de la partie (date ET heure, pas juste la date)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_cours")
    # Utilise la liste STATUT_CHOICES définie plus haut ; démarre à "en_cours"

    ticket_gagnant = models.ForeignKey(
        "Ticket", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    # Lien vers le ticket tiré au sort. "Ticket" entre guillemets car la classe
    # Ticket est définie plus bas dans ce même fichier (référence "en avance").
    # on_delete=SET_NULL : si jamais le ticket est supprimé, ce champ redevient
    # vide au lieu de supprimer toute la partie.
    # related_name="+" : on n'a pas besoin d'accéder aux parties depuis un ticket
    # via ce lien précis (on le fait déjà via tickets.partie plus bas), donc on
    # désactive cet accès inverse pour éviter les conflits de noms.

    def str(self):
        # Ce qui s'affiche dans l'admin Django à la place de "Partie object (1)"
        return self.titre


class Ticket(models.Model):
    STATUT_CHOICES = [
        ("valide", "Valide"),
        ("gagnant", "Gagnant"),
        ("rembourse", "Remboursé"),
    ]

    numero = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    partie = models.ForeignKey(Partie, on_delete=models.CASCADE, related_name="tickets")
    date_achat = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="valide")

    def str(self):
        return f"{self.numero} — {self.partie.titre}"