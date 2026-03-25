from django.contrib import admin
from .models import Project, Investment

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titre', 'porteur', 'secteur', 'montant_cible', 'montant_actuel', 'statut', 'progression')
    list_filter = ('secteur', 'statut', 'date_creation')
    search_fields = ('titre', 'porteur__username', 'localisation')
    readonly_fields = ('progression',)

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('projet', 'investisseur', 'montant', 'statut', 'date')
    list_filter = ('statut', 'date')
    search_fields = ('projet__titre', 'investisseur__username')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Investment, InvestmentAdmin)
