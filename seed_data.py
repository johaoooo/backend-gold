import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User
from projects.models import Project, Investment
from django.contrib.auth.hashers import make_password

# Nettoyer les données existantes
print("🧹 Nettoyage des données existantes...")
User.objects.all().delete()
Project.objects.all().delete()
Investment.objects.all().delete()

# 1. Créer des porteurs
print("📝 Création des porteurs...")
porteur1 = User.objects.create(
    username="agritech_benin",
    email="contact@agritech.bj",
    password=make_password("porteur123"),
    role="porteur",
    is_verified_kyc=True,
    is_approved=True
)

porteur2 = User.objects.create(
    username="solarhub_sn",
    email="info@solarhub.sn",
    password=make_password("porteur123"),
    role="porteur",
    is_verified_kyc=True,
    is_approved=True
)

porteur3 = User.objects.create(
    username="immofacile_ci",
    email="contact@immofacile.ci",
    password=make_password("porteur123"),
    role="porteur",
    is_verified_kyc=True,
    is_approved=True
)

# 2. Créer des investisseurs approuvés
print("💰 Création des investisseurs...")
investisseur1 = User.objects.create(
    username="invest_ouattara",
    email="ouattara@invest.ci",
    password=make_password("invest123"),
    role="investisseur",
    is_verified_kyc=True,
    is_approved=True  # ✅ Approuvé par admin
)

investisseur2 = User.objects.create(
    username="invest_diop",
    email="diop@invest.sn",
    password=make_password("invest123"),
    role="investisseur",
    is_verified_kyc=True,
    is_approved=True
)

investisseur3 = User.objects.create(
    username="invest_nguyen",
    email="nguyen@invest.cm",
    password=make_password("invest123"),
    role="investisseur",
    is_verified_kyc=True,
    is_approved=True
)

# 3. Créer des projets (description détaillée)
print("🚀 Création des projets...")
projets_data = [
    {
        "porteur": porteur1,
        "titre": "AgriTech Bénin",
        "description": """AgriTech Bénin est une plateforme innovante qui connecte les agriculteurs béninois aux marchés urbains et internationaux via une solution IoT. Nous proposons :
- Capteurs connectés pour le suivi des cultures
- Application mobile pour les agriculteurs
- Marketplace pour la vente directe
- Système de micro-assurance intégré

Objectif : Augmenter de 40% les revenus des 5000 agriculteurs partenaires d'ici 2026.""",
        "secteur": "agriculture",
        "localisation": "Cotonou, Bénin",
        "montant_cible": 50000000,
        "montant_actuel": 12500000,
        "statut": "ouvert",
        "date_limite": "2025-12-31"
    },
    {
        "porteur": porteur2,
        "titre": "SolarHub Sénégal",
        "description": """SolarHub est une entreprise spécialisée dans l'installation de panneaux solaires dans les zones rurales du Sénégal. Notre modèle d'affaires :
- Paiement à l'usage (PAYG)
- Kit solaire domestique avec batteries
- Formation technique locale
- Maintenance sur 5 ans

Impact : 10 000 foyers équipés, réduction de 80% des dépenses énergétiques.""",
        "secteur": "energie",
        "localisation": "Dakar, Sénégal",
        "montant_cible": 120000000,
        "montant_actuel": 45000000,
        "statut": "ouvert",
        "date_limite": "2025-10-15"
    },
    {
        "porteur": porteur3,
        "titre": "ImmoFacile Côte d'Ivoire",
        "description": """ImmoFacile révolutionne la recherche immobilière en Afrique francophone avec :
- Visites virtuelles en 3D
- Documentation légale numérisée
- Mise en relation avec notaires partenaires
- Simulation de crédit intégrée

Déjà 1500 biens répertoriés à Abidjan. Expansion prévue vers Dakar et Yaoundé.""",
        "secteur": "immobilier",
        "localisation": "Abidjan, Côte d'Ivoire",
        "montant_cible": 80000000,
        "montant_actuel": 20000000,
        "statut": "ouvert",
        "date_limite": "2025-11-30"
    }
]

projets = []
for data in projets_data:
    projet = Project.objects.create(**data)
    projets.append(projet)
    print(f"  ✅ {projet.titre}")

# 4. Créer des investissements
print("💵 Création des investissements...")
investments_data = [
    {"investisseur": investisseur1, "projet": projets[0], "montant": 5000000, "statut": "accepte", "message": "Je crois au potentiel de l'agriculture connectée."},
    {"investisseur": investisseur1, "projet": projets[1], "montant": 10000000, "statut": "en_attente", "message": "Intéressé par les énergies renouvelables."},
    {"investisseur": investisseur2, "projet": projets[0], "montant": 7500000, "statut": "accepte", "message": "Excellent projet, je souhaite contribuer."},
    {"investisseur": investisseur2, "projet": projets[2], "montant": 20000000, "statut": "en_attente", "message": "Le marché immobilier ivoirien est prometteur."},
    {"investisseur": investisseur3, "projet": projets[1], "montant": 35000000, "statut": "accepte", "message": "Très bon modèle d'affaires."},
    {"investisseur": investisseur3, "projet": projets[2], "montant": 15000000, "statut": "refuse", "message": "Montant trop élevé pour mon portefeuille actuel."},
]

for data in investments_data:
    investment = Investment.objects.create(**data)
    print(f"  ✅ {investment.investisseur.username} → {investment.projet.titre} : {investment.montant} FCFA ({investment.statut})")

# 5. Créer un compte en attente d'approbation
print("⏳ Création d'un investisseur en attente d'approbation...")
investisseur_pending = User.objects.create(
    username="invest_new",
    email="new@invest.com",
    password=make_password("pending123"),
    role="investisseur",
    is_verified_kyc=True,
    is_approved=False  # ❌ En attente d'approbation
)

print("\n" + "="*50)
print("✅ SEED TERMINÉ !")
print("="*50)
print(f"📊 Résumé :")
print(f"   - {User.objects.count()} utilisateurs")
print(f"   - {Project.objects.count()} projets")
print(f"   - {Investment.objects.count()} investissements")
print(f"   - 1 investisseur en attente d'approbation")
print("\n🔑 Mots de passe :")
print("   - Porteurs : porteur123")
print("   - Investisseurs approuvés : invest123")
print("   - En attente : pending123")
