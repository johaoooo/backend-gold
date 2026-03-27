from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    INVESTISSEUR = 'investisseur'
    PORTEUR = 'porteur'
    
    ROLE_CHOICES = [
        (INVESTISSEUR, 'Investisseur'),
        (PORTEUR, 'Porteur de Projet'),
    ]
    
    # Champs existants
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PORTEUR)
    phone = models.CharField(max_length=20, blank=True)
    is_verified_kyc = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    # Nouveaux champs pour investisseurs
    # Informations personnelles
    full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    country_of_residence = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    # Informations professionnelles
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    investment_experience = models.CharField(
        max_length=20, 
        choices=[
            ('debutant', 'Débutant (0-2 ans)'),
            ('intermediaire', 'Intermédiaire (2-5 ans)'),
            ('expert', 'Expert (5+ ans)'),
        ],
        blank=True
    )
    investment_areas = models.CharField(max_length=200, blank=True)  # Secteurs d'intérêt
    investment_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    investment_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Informations financières
    investor_type = models.CharField(
        max_length=30,
        choices=[
            ('individual', 'Investisseur individuel'),
            ('family_office', 'Family Office'),
            ('institutionnel', 'Institutionnel'),
            ('business_angel', 'Business Angel'),
            ('autre', 'Autre'),
        ],
        blank=True
    )
    net_worth = models.CharField(max_length=50, blank=True)  # Valeur nette
    
    # Documents
    id_document = models.FileField(upload_to='kyc/documents/', null=True, blank=True)
    proof_of_address = models.FileField(upload_to='kyc/address/', null=True, blank=True)
    
    # Pourquoi investir ?
    motivation = models.TextField(blank=True, help_text="Pourquoi souhaitez-vous investir en Afrique ?")
    
    def __str__(self):
        return f"{self.username} ({self.role})"

# Ajouter dans la classe User (avant le __str__)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
