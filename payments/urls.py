from django.urls import path
from .views import ConfirmationPaiementView

urlpatterns = [
    path("confirmer/", ConfirmationPaiementView.as_view(), name="paiement-confirmer"),
]