import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@golden.com',
        password='Admin123!'
    )
    print("✅ Superutilisateur admin créé avec succès")
else:
    print("ℹ️ Le superutilisateur admin existe déjà")
