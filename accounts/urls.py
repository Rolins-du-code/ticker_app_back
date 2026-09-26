from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import InscriptionView

urlpatterns = [
    path("inscription/", InscriptionView.as_view(), name="connexion-refresh"),
    path("connexion/", TokenObtainPairView.as_view(), name="connexion"),
    path("connexion/refresh/", TokenRefreshView.as_view(), name="connexion-refresh")
]