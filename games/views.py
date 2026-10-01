from decimal import Decimal
from rest_framework import generics
from rest_framework import permissions
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Partie
from .serializers import AchatTicketSerializer
from payments.models import Transaction
from payments.services import initier_paiement_mobile_money

# pour lister les partie 
from .serializers import PartiePubliqueSerializer
# from .serializers import PartieSerializer # Remplacez par le nom réel de votre sérialiseur si besoin


class AchatTicketView(APIView):
    """
    POST /api/games/parties/<id>/acheter/
    Initie un achat de ticket(s). Ne crée AUCUN ticket ici :
    seulement une Transaction "en_attente". Les tickets ne sont créés
    qu'à la confirmation du paiement (voir payments/views.py).
    """
    permission_classes = [permissions.IsAuthenticated]
    # IsAuthenticated : il faut être connecté pour acheter — on a besoin
    # de savoir QUI achète, impossible avec AllowAny.

    def post(self, request, pk):
        partie = Partie.objects.filter(pk=pk).first()
        if partie is None:
            return Response({"erreur": "Partie introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifications métier AVANT de créer quoi que ce soit
        if partie.statut != "en_cours":
            return Response({"erreur": "Cette partie n'est plus active."}, status=status.HTTP_400_BAD_REQUEST)

        if partie.date_fin < timezone.now():
            return Response({"erreur": "Cette partie est terminée."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AchatTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantite = serializer.validated_data["quantite"]

        montant_total = partie.prix_ticket * Decimal(quantite)

        # On appelle le service de paiement (stub pour l'instant)
        resultat_paiement = initier_paiement_mobile_money(
            montant=montant_total,
            numero_telephone=request.user.phone_number,
        )

        # On enregistre la transaction en "en_attente" — PAS encore de ticket
        transaction = Transaction.objects.create(
            quantite_tickets = quantite,
            user=request.user,
            partie = partie,
            montant=montant_total,
            type_transaction="achat",
            reference_mobile_money=resultat_paiement["reference"],
            statut="en_attente",
        )

        return Response(
            {
                "transaction_id": transaction.id,
                "reference": transaction.reference_mobile_money,
                "montant": str(montant_total),
                "quantite": quantite,
                "partie_id": partie.id,
                "statut": "en_attente",
                "message": "Paiement initié, en attente de confirmation.",
            },
            status=status.HTTP_201_CREATED,
        )



class PartieListView(generics.ListAPIView):
    """
    GET /api/games/parties/  → liste toutes les parties en cours.
    """
    queryset = Partie.objects.filter(statut="en_cours").order_by("date_fin")
    serializer_class = PartiePubliqueSerializer
    permission_classes = [permissions.AllowAny]


class PartieDetailView(generics.RetrieveAPIView):
    """
    GET /api/games/parties/<id>/  → détail d'une partie précise.
    """
    queryset = Partie.objects.all()
    serializer_class = PartiePubliqueSerializer
    permission_classes = [permissions.AllowAny]
