from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True, min_length= 6)

    class Meta:
        model = User
        fields = ["id", "username", "phone_number", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
        )