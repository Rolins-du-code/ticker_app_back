from django.db import transaction as db_transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Transaction
from games.models import Ticket


class ConfirmationPaiementView(APIView):
    """
    POST /api/payments/confirmer/
    Simule le webhook que l'opérateur Mobile Money appelle pour confirmer
    qu'un paiement a réellement été reçu. C'est ICI, et seulement ici,
    que les tickets sont créés — jamais à l'initiation du paiement.
    """
    permission_classes = [permissions.AllowAny]
    # AllowAny car c'est l'opérateur (serveur à serveur) qui appellera cette
    # route, pas un utilisateur connecté depuis l'app. En production, il
    # faudra la sécuriser avec une signature/clé secrète fournie par
    # l'opérateur — à faire quand on branchera la vraie API.

    def post(self, request):
        reference = request.data.get("reference")
        statut_paiement = request.data.get("statut")  # "reussi" ou "echoue"

        transaction = Transaction.objects.filter(reference_mobile_money=reference).first()
        if transaction is None:
            return Response({"erreur": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if transaction.statut != "en_attente":
            # Idempotence : si la même confirmation arrive deux fois
            # (bug réseau côté opérateur), on ne recrée pas les tickets.
            return Response({"message": "Transaction déjà traitée."})

        if statut_paiement != "reussi":
            transaction.statut = "echouee"
            transaction.save()
            return Response({"message": "Paiement échoué, transaction marquée échouée."})

        partie = transaction.partie
        if partie is None or partie.statut != "en_cours":
            transaction.statut = "echouee"
            transaction.save()
            return Response({"erreur": "Partie invalide ou terminée."}, status=status.HTTP_400_BAD_REQUEST)

        # db_transaction.atomic() : soit TOUT réussit ensemble (statut,
        # tickets, montant_collecte), soit rien n'est enregistré en cas
        # d'erreur au milieu. Ça évite le pire cas : argent reçu mais
        # aucun ticket créé.
        with db_transaction.atomic():
            transaction.statut = "reussie"
            transaction.save()

            tickets_crees = []
            for _ in range(transaction.quantite_tickets):
                ticket = Ticket.objects.create(user=transaction.user, partie=partie)
                tickets_crees.append(str(ticket.numero))

            partie.montant_collecte += transaction.montant
            partie.save()

        return Response({
            "message": "Paiement confirmé, tickets créés.",
            "tickets": tickets_crees,
        })