from django.core.mail import send_mail
from django.conf import settings

def send_approval_pending_email(user):
    subject = "Bienvenue sur Golden Invest - Compte en attente de validation"
    message = f"""
Bonjour {user.username},

Votre compte a bien été créé sur Golden Invest.

Votre profil est en cours de validation par notre équipe.
Vous recevrez un email dès que votre compte sera activé.

En attendant, vous pouvez consulter notre plateforme :
https://effervescent-conkies-b4bf5b.netlify.app

À bientôt sur Golden Invest !
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

def send_account_approved_email(user):
    subject = "Golden Invest - Votre compte est maintenant actif !"
    message = f"""
Bonjour {user.username},

Bonne nouvelle ! Votre compte a été validé par notre équipe.

Vous pouvez dès maintenant vous connecter et découvrir les projets disponibles :
https://effervescent-conkies-b4bf5b.netlify.app/connexion

L'équipe Golden Invest
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
