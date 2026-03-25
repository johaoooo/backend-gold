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
