from django.db import models
from django.conf import settings


class DemandeAide(models.Model):
    """
    Représente un signalement de détresse ou de problème par un utilisateur,
    visible par les autres utilisateurs de la plateforme (aide communautaire).
    """

    STATUT_CHOICES = [
        ("en_attente", "En attente"),   # pas encore examinée
        ("validee", "Validée"),         # jugée recevable, visible et aidable
        ("rejetee", "Rejetée"),         # jugée non recevable
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="demandes_aide")
    # La personne qui signale son problème

    nature = models.CharField(max_length=100)
    # Catégorie courte du problème, ex. "Maladie grave", "Escroquerie", "Autre"
    # (un CharField libre pour l'instant ; on pourra le transformer en choices
    # fixes plus tard si le client fournit une liste précise)

    description = models.TextField()
    # Explication détaillée de la situation, écrite par l'utilisateur

    aide_souhaitee = models.TextField()
    # Ce que l'utilisateur demande concrètement (montant, type de soutien...)

    justificatif = models.FileField(upload_to="demandes_aide/", blank=True, null=True)
    # Pièce jointe optionnelle (photo, document). blank/null=True car pas
    # obligatoire à la création — dépendra des conditions posées par le client.

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    # Tant que le client n'a pas fixé les critères de validation, tout reste
    # "en_attente" par défaut — la logique de validation viendra plus tard.

    date_creation = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.nature} — {self.user} — {self.statut}"


class Notification(models.Model):
    """
    Journal des notifications envoyées aux utilisateurs
    (ex. rappel de fin de partie, annonce du gagnant, remboursement).
    """

    TYPE_CHOICES = [
        ("fin_partie", "Fin de partie"),
        ("resultat", "Résultat / gagnant"),
        ("remboursement", "Remboursement"),
        ("aide", "Aide communautaire"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_envoi = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True : sert de log — on garde une trace de ce qui a été
    # envoyé et quand, utile pour le support et l'audit.

    def str(self):
        return f"{self.type_notification} → {self.user}"