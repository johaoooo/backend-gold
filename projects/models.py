from django.db import models
from django.conf import settings


class Project(models.Model):
    SECTEUR_CHOICES = [
        ('immobilier', 'Immobilier'),
        ('agriculture', 'Agriculture'),
        ('tech', 'Tech / Startup'),
        ('energie', 'Énergie / Solaire'),
    ]

    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours de financement'),
        ('ferme', 'Fermé'),
    ]

    porteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projets'
    )
    titre = models.CharField(max_length=200)
    description = models.TextField()
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES)
    localisation = models.CharField(max_length=100)
    montant_cible = models.DecimalField(max_digits=12, decimal_places=2)
    montant_actuel = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouvert')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.secteur})"

    @property
    def progression(self):
        if self.montant_cible > 0:
            return round((self.montant_actuel / self.montant_cible) * 100, 2)
        return 0


class Investment(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]

    investisseur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='investissements'
    )
    projet = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='investissements'
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    class Meta:
        unique_together = ('investisseur', 'projet')

    def __str__(self):
        return f"{self.investisseur.username} → {self.projet.titre} ({self.montant})"
