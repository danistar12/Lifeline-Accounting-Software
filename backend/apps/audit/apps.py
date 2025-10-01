from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.audit'
    verbose_name = 'Audit Logs'
    
    def ready(self):
        # Temporarily disable signals to prevent user creation issues
        # import apps.audit.signals
        pass
