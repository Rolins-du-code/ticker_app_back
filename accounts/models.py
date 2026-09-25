from django.contrib.auth.models import AbstractUser
from django.db import models

# Create de mon modele 
class User(AbstractUser):
    phone_nomber = models.CharField(max_length=20, unique=True)
    is_phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_nomber or self.username
