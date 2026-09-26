from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import InscriptionSerializer


# Create your views here.
class InscriptionView(generics.CreateAPIView):
    '''POST /api/accounts/inscription/
    ouvert a tous (AlloeAny) Puisque c'est justement pour creer un compte
    '''

    serializer_class = InscriptionSerializer
    permission_classes = [permissions.AllowAny]

