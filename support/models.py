from django.db import models
from django.conf import settings
# Create your models here.
class DemandeAide(models.Model):
    '''Presente un siagnale de detresse par un utilisateur et visible par les autres utilisateurs de l'application'''
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),  #la demande est en attente de traitement
        ('valide', 'Validée'),  #la demande est validée
        ('rejetee', 'Rejetée'),  #la demande est rejetée
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="demandes_aide")
    nature = models.CharField(max_length=100)
    description = models.TextField()
    aide_souhaitee = models.TextField()
    justificatif = models.FileField(upload_to="demandes_aide/", blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nature} - {self.user} - {self.statut}"
class Notification(models.Model):
    ''' Journal des notifications envoyees aux utilisateurs (ex: rappel de fin de la partie annonce du gagnant etc )'''
    TYPE_CHOICES = [
        ('fin_partie', 'Fin de partie'),     #notification de rappel
        ('resultat', "Resultat / gagnant"), #notification de resultat
        ('remboursement', 'Remboursement'), #notification de remboursement
        ('aide', "Aide communautaire"),     #notification de demande d'aide
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(max_length=500)
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_notification} -> {self.user} - {self.date_envoi}"