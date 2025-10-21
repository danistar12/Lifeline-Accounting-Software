from .settings import *

DEBUG = False
ALLOWED_HOSTS = [
    '10.100.5.61',  # production IP
    '02-vuweb01',   # server hostname
    'lifelinedatacenters.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'LLAcctTemp',
        'USER': 'LLAcct',
        'PASSWORD': 'SilverMoon#3',
        'HOST': '10.100.5.27',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;Encrypt=no',
        }
    }
}

# Production CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://10.100.5.61",
    "https://lifelinedatacenters.com",
]

# Production cookie settings (secure for HTTPS)
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = '/var/www/lifeline-accounting/static/'
MEDIA_ROOT = '/var/www/lifeline-accounting/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
