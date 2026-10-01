from django.contrib import admin
from .models import Partie, Ticket


class PartieAdmin(admin.ModelAdmin):
    # readonly_fields : le champ reste visible dans l'admin (pratique pour
    # vérifier son état), mais impossible à modifier à la main — seul le
    # code métier (confirmation de paiement) peut le changer.
    readonly_fields = ["montant_collecte"]


admin.site.register(Partie, PartieAdmin)
admin.site.register(Ticket)