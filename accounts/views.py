from rest_framework import generics, permissions
from .serializers import InscriptionSerializer


class InscriptionView(generics.CreateAPIView):
    """
    POST /api/accounts/inscription/
    Ouvert à tous (AllowAny) puisque c'est justement pour créer un compte.
    """
    serializer_class = InscriptionSerializer
    permission_classes = [permissions.AllowAny]

