import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lifeline_backend.settings_production')

application = get_wsgi_application()
