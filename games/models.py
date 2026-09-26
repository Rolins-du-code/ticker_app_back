import uuid
from django.db import models
#modele personnalise et on l'utilise pour le fait qu'il soit flexible et qu'on puisse le changer facilement dans le settings.py
from django.conf import settings 


# Create your models 

class Partie(models.Model):
    '''''
        Represente un produit mis en jeu(voiture, telephone etc)
        avec le prix du ticket, et la progression de la collecte.
    '''''
#liste des statuts de l'application
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),  #la partie , on vend les ticker
        ('reussi', 'Réussi'),      #Objectif atteint, le gagnant est tiré au sort
        ('annule', 'Annulé'),      #la partie est annulée, les tickets sont remboursés
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to="parties/", blank=True, null=True)
    prix_produit = models.DecimalField(max_digits=12, decimal_places=2)
    prix_ticket = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    montant_collecte = models.DecimalField(max_digits=12, decimal_places=2, default = 0.00)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default = 'en_cours')
    notification_finale_envoyee = models.BooleanField(default=False)
    ticker_gagnant = models.ForeignKey(
        "Ticker", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    def __str__(self):
        # Ce qui s'affiche dans l'admin Django a la place de l'objet partie(1)
        return self.titre
class Ticker(models.Model):
    '''''
    Represente un ticket achete par un utilisateur pour une partie donnee
    '''''
    STATUT_CHOICES = [
        ('valide', 'Valide'),  #le ticket normal enm attente de tirage
        ('gagnant', 'Gagnant'),  #le ticket gagnant
        ('rembourse', 'Remboursé'),  #le ticket remboursé et partie annulee
    ]
    numero = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickers")
    partie = models.ForeignKey(Partie, on_delete=models.CASCADE, related_name="tickers")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default = 'valide')
    date_achat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero}  - {self.partie.titre}"