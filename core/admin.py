from django.contrib import admin
from django.contrib.admin import AdminSite

class GoldenAdminSite(AdminSite):
    site_header = "Golden Invest Administration"
    site_title = "Golden Invest Admin"
    index_title = "Bienvenue sur le tableau de bord Golden Invest"
    site_url = "/api/projects/"

admin_site = GoldenAdminSite(name='goldenadmin')
