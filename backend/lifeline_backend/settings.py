from pathlib import Path
from datetime import timedelta
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.100.5.61',  # production IP
    '02-vuweb01',   # server hostname
    'lifelinedatacenters.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'lifeline_backend',
    'apps.accounts',
    'apps.subscriptions',
    'apps.documents',
    'apps.importer',
    'apps.payroll',
    'apps.payments.apps.PaymentsConfig',
    # New modular apps
    'apps.banking',            # Bank accounts, statements, reconciliation
    'apps.reports',            # Financial reports (BS, IS, CF)
    'apps.dashboard',          # KPI and Dashboard endpoints
    'apps.audit',              # Audit logging system
    'apps.inventory',          # Inventory management
    'apps.projects',           # Projects and time entries
    'apps.budgets',            # Budget planning
    'apps.assets',             # Fixed assets
    'apps.integrations',       # External integrations
    'apps.taxes',              # Tax rates and transactions
    # Core app replacement - dedicated entity apps
    'apps.customers',          # Customer management
    'apps.vendors',            # Vendor management
    'apps.invoices',           # Invoice processing
    'apps.bills',              # Bill management
    'apps.accounting',         # Chart of accounts & general ledger
    'apps.customfields',       # Custom field functionality
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.audit.middleware.AuditLogMiddleware',  # Re-enabled with async support
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "https://10.100.5.61",
]

# Allow cookies/credentials to be included in CORS requests from the frontend
CORS_SUPPORTS_CREDENTIALS = True
CORS_ALLOW_CREDENTIALS = True

# Allow the frontend to send the custom X-Company-ID header in preflight requests
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'x-company-id',
]

# Development-friendly cookie settings
# Note: For local development it's easiest to run the frontend on the same host (localhost)
# to avoid cross-origin cookie issues. The settings below relax SameSite so cookies can be
# included in cross-site requests during local testing. Do NOT use these in production.
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Session security settings
SESSION_COOKIE_AGE = 3600  # 1 hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True  # Update session expiry on each request

# If you want to scope cookies to a specific domain, set SESSION_COOKIE_DOMAIN accordingly.
# For local testing we leave it unset so cookies are host-only.
# SESSION_COOKIE_DOMAIN = None

AUTH_USER_MODEL = 'accounts.User'

ROOT_URLCONF = 'lifeline_backend.urls'

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

WSGI_APPLICATION = 'lifeline_backend.wsgi.application'



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

# Use an isolated SQLite database when running the Django test suite
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
import os
# Use absolute URL path so templates generate /static/... links (important when WSGI is mounted at /api)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Use absolute URL path so templates generate /static/... links (important when WSGI is mounted at /api)
import os
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Allow Authorization: Bearer <token> as a fallback during local development
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'apps.accounts.authentication.JWTCookieAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),

    'ACCESS_TOKEN_COOKIE': 'access_token',
    'REFRESH_TOKEN_COOKIE': 'refresh_token',
    'ACCESS_TOKEN_COOKIE_HTTPONLY': True,
    'REFRESH_TOKEN_COOKIE_HTTPONLY': True,
    'ACCESS_TOKEN_COOKIE_SAMESITE': 'Lax',
    'REFRESH_TOKEN_COOKIE_SAMESITE': 'Lax',
    'ACCESS_TOKEN_COOKIE_SECURE': False, # Should be True in production
    'REFRESH_TOKEN_COOKIE_SECURE': False, # Should be True in production
}

# For local development allow JWT cookies to be sent in cross-site (frontend at different host)
# Set SameSite=None for dev so cookies are attached when using withCredentials
SIMPLE_JWT['ACCESS_TOKEN_COOKIE_SAMESITE'] = None
SIMPLE_JWT['REFRESH_TOKEN_COOKIE_SAMESITE'] = None

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
