from .settings import *

DEBUG = False
ALLOWED_HOSTS = [
    '10.100.5.61',  # production IP where backend is hosted
    '02-vuweb01',   # server hostname
    'lifelinedatacenters.com',
    'la.lldc.local',  # New proxy domain for backend
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

# Production CORS settings - Allow frontend proxy to access backend IP
CORS_ALLOWED_ORIGINS = [
    "https://10.100.5.61",
    "https://lifelinedatacenters.com", 
    "https://la.lldc.local",  # Frontend proxy domain
]

# CSRF trusted origins for admin and authentication
CSRF_TRUSTED_ORIGINS = [
    'https://10.100.5.61',
    'https://lifelinedatacenters.com',
    'https://la.lldc.local',  # Frontend proxy domain
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

# Production logging configuration for FedRAMP compliance
import os

# Production logs directory - use absolute path
LOGS_DIR = '/var/www/lifeline-accounting/backend/logs'

# Ensure logs directory exists with proper permissions
if not os.path.exists(LOGS_DIR):
    try:
        os.makedirs(LOGS_DIR, mode=0o755)
    except (OSError, PermissionError):
        # If we can't create logs directory, use a fallback location
        LOGS_DIR = '/tmp/lifeline-logs'
        try:
            os.makedirs(LOGS_DIR, mode=0o755, exist_ok=True)
        except (OSError, PermissionError):
            # Ultimate fallback - use console only
            LOGS_DIR = None

# Determine if we can use file logging
USE_FILE_LOGGING = LOGS_DIR is not None

# Override base logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'security': {
            'format': '[SECURITY] {asctime} - {levelname} - {message}',
            'style': '{',
        },
        'audit': {
            'format': '[AUDIT] {asctime} - {message}',
            'style': '{',
        },
        'production': {
            'format': '[PROD] {asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',  # Less verbose in production
            'class': 'logging.StreamHandler',
            'formatter': 'production',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',  # Only warnings and errors in production
            'propagate': False,
        },
        'apps.security.middleware': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.accounts.middleware': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'lifeline_backend': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Add file handlers if we can use file logging
if USE_FILE_LOGGING and LOGS_DIR:
    LOGGING['handlers'].update({
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'lifeline.log'),
            'maxBytes': 1024*1024*20,  # 20MB for production
            'backupCount': 15,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'INFO',  # Log all security events in production
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'security.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 25,
            'formatter': 'security',
        },
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'audit.log'),
            'maxBytes': 1024*1024*30,  # 30MB for audit trail
            'backupCount': 50,  # Keep more audit logs
            'formatter': 'audit',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'errors.log'),
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    })
    
    # Update loggers to use file handlers in production
    LOGGING['loggers']['django']['handlers'] = ['file', 'error_file', 'console']
    LOGGING['loggers']['apps.security.middleware']['handlers'] = ['security_file', 'audit_file', 'console']
    LOGGING['loggers']['apps.accounts.middleware']['handlers'] = ['security_file', 'audit_file', 'console']
    LOGGING['loggers']['lifeline_backend']['handlers'] = ['file', 'error_file', 'console']
    LOGGING['root']['handlers'] = ['file', 'console']
