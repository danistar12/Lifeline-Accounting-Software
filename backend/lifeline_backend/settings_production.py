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

# CSRF trusted origins for admin and authentication
CSRF_TRUSTED_ORIGINS = [
    'https://10.100.5.61',
    'https://lifelinedatacenters.com',
]

# Production cookie settings (secure for HTTPS)
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Session security settings
SESSION_COOKIE_AGE = 3600  # 1 hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True  # Update session expiry on each request
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # HTTPS required
SESSION_COOKIE_SAMESITE = 'Lax'

# Force logout after inactivity
SESSION_SECURITY_WARN_AFTER = 1800  # 30 minutes
SESSION_SECURITY_EXPIRE_AFTER = 3600  # 1 hour

STATIC_ROOT = '/var/www/lifeline-accounting/static/'
MEDIA_ROOT = '/var/www/lifeline-accounting/media/'

# Security settings for FedRAMP compliance
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# Session security for FedRAMP
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# Disable server tokens
USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
