from django.db import models
from django.conf import settings
from games.models import Ticket


class Transaction(models.Model):
    """
    Représente un mouvement d'argent : achat de ticket ou remboursement.
    """

    TYPE_CHOICES = [
        ("achat", "Achat"),
        ("remboursement", "Remboursement"),
    ]

    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("reussie", "Réussie"),
        ("echouee", "Échouée"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    # L'utilisateur concerné par ce mouvement d'argent

    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    # Lien vers le ticket concerné, si applicable.
    # SET_NULL : si le ticket est supprimé, on garde quand même la trace
    # comptable de la transaction (important pour l'audit).

    montant = models.DecimalField(max_digits=12, decimal_places=2)
    # Montant du mouvement, en FCFA

    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    # "achat" (utilisateur → plateforme) ou "remboursement" (plateforme → utilisateur)

    reference_mobile_money = models.CharField(max_length=100, unique=True, blank=True, null=True)
    # Identifiant renvoyé par l'API MTN MoMo / Orange Money.
    # unique=True : sert de garde-fou anti-double-traitement (idempotence) —
    # si la même référence arrive deux fois (ex. bug réseau), on la reconnaît.

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    partie = models.ForeignKey("games.Partie", on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")

    quantite_tickets= models.PositiveIntegerField(default=1)
    date_creation = models.DateTimeField(auto_now_add=True)
    # Horodatage automatique, utile pour la traçabilité/l'audit

    def str(self):
        return f"{self.type_transaction} — {self.montant} FCFA — {self.statut}"