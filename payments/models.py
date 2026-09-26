from django.db import models
from django.conf import settings
from games.models import Ticker, Partie
# Create your models 

class Transaction(models.Model):
    '''''
    Represente une transaction de paiement pour un ticket achete par un utilisateur pour une partie donnee ou remboursement du ticket en cas d'echec de la transaction
    '''''
    TYPE_CHOICES = [
        ('achat', 'Achat'),  #transaction d'achat de ticket
        ('remboursement', 'Remboursement'),  #transaction de remboursement de ticket en cas d'echec de la transaction
    ]
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),  #la transaction est en cours de traitement
        ('reussi', 'Réussi'),      #la transaction est reussie et le ticket est valide
        ('echec', 'Echec'),        #la transaction a echoue et le ticket est rembourse
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    ticker = models.ForeignKey(Ticker, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default = 'en_cours')
    date_transaction = models.DateTimeField(auto_now_add=True)
    reference_mobile_money = models.CharField(max_length=100, unique=True, blank=True, null=True)
    partie = models.ForeignKey(
        "games.Partie", on_delete=models.SET_NULL, null=True, blank=True, related_name="transaction"
    )
    quantite_tickets = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.type_transaction} - {self.montant} FCFA - {self.statut}"