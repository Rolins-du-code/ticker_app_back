import math

from rest_framework import serializers
from .models import Partie, Ticker

class PartiePublicSerializer(serializers.ModelSerializer):
    ''' COnvertit un objet partie en JSON et vice versa POUR L'API REST ce que l'app mobile comprend et envoie
    et il y a aussi une progression calculee, utile pour la barre de progression de l'app mobile'''
    tickets_vendus = serializers.SerializerMethodField()
    tickets_necessaires = serializers.SerializerMethodField()
    progression_pourcentage = serializers.SerializerMethodField()
    class Meta:
        model = Partie
        fields = [
            'id',
            "titre",
            "description",
            "photo",
            "prix_produit",
            "prix_ticket",
            "montant_collecte",
            "date_debut",
            "date_fin",
            "statut",
            "tickets_vendus",
            "tickets_necessaires",
            "progression_pourcentage",
        ]
    def get_tickets_vendus(self, obj):
        return obj.tickers.exclude(statut='rembourse').count()

    def get_tickets_necessaires(self, obj):
        return math.ceil(obj.prix_produit / obj.prix_ticket)

    def get_progression_pourcentage(self, obj):
        tickets_vendus = self.get_tickets_vendus(obj)
        tickets_necessaires = self.get_tickets_necessaires(obj)
        if tickets_necessaires == 0:
            return 0
        return min(round((tickets_vendus / tickets_necessaires) * 100), 100)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = [
            "id",
            "numero",
            "partie",
            "date_achat",
            "statut",
        ]
        read_only_fields = ["numero", "date_achat", "statut"]

class AchatTicketSerializer(serializers.Serializer):
    ''' Ne corres[pond a occcun model: sert uniquement a valider les
    donnees envoyer par l'app mobile pour l'achat d'un ticket'''''
    quantite = serializers.IntegerField(min_value=1)