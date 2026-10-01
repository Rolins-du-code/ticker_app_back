import math

from rest_framework import serializers
from .models import Partie, Ticket
# from .serializers import PartiePubliqueSerializer


class PartiePubliqueSerializer(serializers.ModelSerializer):
    """
    Serializer exposé à l'app mobile (utilisateurs).
    Ne révèle jamais le montant_collecte exact en FCFA — seulement
    une progression calculée, utile pour la barre de progression du front.
    """

    tickets_vendus = serializers.SerializerMethodField()
    tickets_necessaires = serializers.SerializerMethodField()
    progression_pourcentage = serializers.SerializerMethodField()

    class Meta:
        model = Partie
        fields = [
            "id",
            "titre",
            "description",
            "photo",
            "prix_produit",
            "prix_ticket",
            "date_debut",
            "date_fin",
            "statut",
            "tickets_vendus",
            "tickets_necessaires",
            "progression_pourcentage",
        ]
        # montant_collecte n'apparaît PAS dans cette liste → jamais envoyé
        # à l'app mobile, seulement visible côté /admin/

    def get_tickets_vendus(self, obj):
        return obj.tickets.exclude(statut="rembourse").count()

    def get_tickets_necessaires(self, obj):
        return math.ceil(obj.prix_produit / obj.prix_ticket)

    def get_progression_pourcentage(self, obj):
        vendus = self.get_tickets_vendus(obj)
        necessaires = self.get_tickets_necessaires(obj)
        if necessaires == 0:
            return 0
        return min(round((vendus / necessaires) * 100), 100)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "numero", "partie", "date_achat", "statut"]
        read_only_fields = ["numero", "date_achat", "statut"]


class AchatTicketSerializer(serializers.Serializer):
    """
    Ne correspond à aucun modèle : sert uniquement à valider
    les données envoyées par l'app mobile pour un achat.
    """
    quantite = serializers.IntegerField(min_value=1)