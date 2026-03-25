from rest_framework import serializers
from .models import Project, Investment


class ProjectSerializer(serializers.ModelSerializer):
    porteur = serializers.StringRelatedField(read_only=True)
    progression = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            'id', 'porteur', 'titre', 'description', 'secteur',
            'localisation', 'montant_cible', 'montant_actuel',
            'statut', 'progression', 'date_creation', 'date_limite'
        ]
        read_only_fields = ['id', 'porteur', 'montant_actuel', 'date_creation']


class InvestmentSerializer(serializers.ModelSerializer):
    investisseur = serializers.StringRelatedField(read_only=True)
    projet = serializers.StringRelatedField(read_only=True)
    projet_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Investment
        fields = ['id', 'investisseur', 'projet', 'projet_id', 'montant', 'statut', 'date', 'message']
        read_only_fields = ['id', 'investisseur', 'projet', 'statut', 'date']
