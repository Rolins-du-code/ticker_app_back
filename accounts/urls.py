from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import InscriptionView

urlpatterns = [
    path("inscription/", InscriptionView.as_view(), name="inscription"),
    path("connexion/", TokenObtainPairView.as_view(), name="connexion"),
    # Retourne un couple {access, refresh} si username + password sont corrects

    path("connexion/refresh/", TokenRefreshView.as_view(), name="connexion-refresh"),
    # Permet d'obtenir un nouveau token "access" quand l'ancien expire,
    # sans redemander le mot de passe — utile pour ne pas déconnecter
    # l'utilisateur en permanence.
]