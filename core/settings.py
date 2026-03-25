import os
import dj_database_url
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Sécurité ──────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-gold-invest-key-static')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',          # Railway
    '.up.railway.app',       # Railway preview
]

# ── Applications ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',  # ⚠️ DOIT être AVANT django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'accounts',
    'projects',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise après SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ── Base de données ───────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Railway fournit DATABASE_URL automatiquement
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'golden_db',
            'USER': 'postgres',
            'PASSWORD': 'postgres123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# ── Auth & JWT ────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ── CORS ──────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# ── Fichiers statiques (WhiteNoise) ───────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Divers ────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Jazzmin Admin Theme Configuration
JAZZMIN_SETTINGS = {
    "site_title": "Golden Invest Admin",
    "site_header": "Golden Invest",
    "site_brand": "Golden Invest",
    "welcome_sign": "Bienvenue sur l'administration Golden Invest",
    "copyright": "Golden Invest",
    "search_model": "accounts.User",
    "show_ui_builder": True,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    
    # Menu personnalisé
    "navigation": [
        {"name": "Dashboard", "icon": "fas fa-tachometer-alt", "url": "/admin/"},
        {"name": "Utilisateurs", "icon": "fas fa-users", "model": "accounts.User"},
        {"name": "Projets", "icon": "fas fa-project-diagram", "model": "projects.Project"},
        {"name": "Investissements", "icon": "fas fa-chart-line", "model": "projects.Investment"},
        {"name": "Groupes", "icon": "fas fa-layer-group", "model": "auth.Group"},
    ],
}

# PythonAnywhere settings
import os

# Allow PythonAnywhere host
ALLOWED_HOSTS = ['*']  # À restreindre après déploiement

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/home/votre_username/backend-gold/static'

# Render deployment
import os
import dj_database_url

if os.environ.get('RENDER'):
    # Disable HTTPS redirect
    SECURE_SSL_REDIRECT = False
    
    # Allow Render host
    ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
    
    # Database configuration from DATABASE_URL
    if 'DATABASE_URL' in os.environ:
        DATABASES['default'] = dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
# À ajouter à la fin de core/settings.py
import os
import dj_database_url

# Render deployment settings
if os.environ.get('RENDER'):
    # Security settings for free plan
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    
    # Allow all Render domains
    ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
    
    # Database
    if 'DATABASE_URL' in os.environ:
        DATABASES['default'] = dj_database_url.config(
            conn_max_age=600,
            ssl_require=False  # Free plan ne supporte pas SSL
        )
    
    # Static files
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Media files
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # Disable debug
    DEBUG = False
