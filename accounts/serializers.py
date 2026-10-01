from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
# get_user_model() récupère TOUJOURS le bon modèle User configuré dans
# AUTH_USER_MODEL — plus sûr que d'importer User directement, qui pourrait
# pointer vers le mauvais modèle si la config change un jour.


class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    # write_only=True : le mot de passe peut être ENVOYÉ à l'API,
    # mais ne sera jamais RENVOYÉ dans une réponse JSON.

    class Meta:
        model = User
        fields = ["id", "username", "phone_number", "password"]

    def create(self, validated_data):
        # On utilise create_user() (pas User.objects.create()) car
        # create_user() hache le mot de passe correctement avant stockage.
        # Un create() classique stockerait le mot de passe en clair — faille
        # de sécurité grave.
        return User.objects.create_user(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )