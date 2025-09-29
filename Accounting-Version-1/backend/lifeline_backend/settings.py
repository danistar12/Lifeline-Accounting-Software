from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


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
    "http://127.0.0.1:8080",
]

CORS_SUPPORTS_CREDENTIALS = True

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


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
#using sqlite for dev and testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Example SQL Server connection (uncomment and edit to use)
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'LLAcctTemp',
#         'USER': 'LLAcct',
#         'PASSWORD': 'SilverMoon#3',
#         'HOST': '10.100.5.27',
#         'PORT': '1433',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 18 for SQL Server',
#             'extra_params': 'TrustServerCertificate=yes;Encrypt=no',
#         },
#     }
# }

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
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Media files (User uploads)
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
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

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
