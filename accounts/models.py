from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    INVESTISSEUR = 'investisseur'
    PORTEUR = 'porteur'
    
    ROLE_CHOICES = [
        (INVESTISSEUR, 'Investisseur'),
        (PORTEUR, 'Porteur de Projet'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PORTEUR)
    phone = models.CharField(max_length=20, blank=True)
    is_verified_kyc = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
