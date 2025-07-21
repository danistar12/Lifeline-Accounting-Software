from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import AuditLog
from .utils import get_object_changes

User = get_user_model()

# List of models to automatically audit
# You can add more models as needed
AUDITED_MODELS = {
    # Authentication and User Management
    User: {'app_label': 'accounts'},
    
    # Add more models here as needed
    # Example: YourModel: {'app_label': 'your_app'},
}


def get_company_from_instance(instance):
    """
    Try to determine the company from a model instance.
    This is a helper function for the signal handlers.
    """
    # Directly has company field
    if hasattr(instance, 'company'):
        return instance.company
        
    # User might have active_company
    if isinstance(instance, User) and hasattr(instance, 'active_company'):
        return instance.active_company
        
    # For company-specific models that have a foreign key to company
    for field in instance._meta.fields:
        if field.name.endswith('company') and hasattr(instance, field.name):
            return getattr(instance, field.name)
            
    # If we can't determine the company, use the first one (fallback)
    from apps.accounts.models import Company
    try:
        return Company.objects.first()
    except:
        return None


@receiver(post_save)
def model_post_save(sender, instance, created, **kwargs):
    """
    Signal handler to log model changes automatically.
    """
    # Check if this model should be audited
    if sender not in AUDITED_MODELS:
        return
        
    # Get company
    company = get_company_from_instance(instance)
    if not company:
        return
        
    # Determine action type
    action_type = AuditLog.CREATE if created else AuditLog.UPDATE
    
    # Create a descriptive action message
    model_name = instance._meta.verbose_name or instance.__class__.__name__
    if created:
        action_description = f"Created {model_name}: {instance}"
    else:
        action_description = f"Updated {model_name}: {instance}"
        
    # Create audit log
    AuditLog.objects.create(
        company=company,
        action_type=action_type,
        action_description=action_description,
        content_type_id=instance._meta.app_label,
        object_id=str(instance.pk),
        # No user context in signals, system action
        user=None,
    )


@receiver(post_delete)
def model_post_delete(sender, instance, **kwargs):
    """
    Signal handler to log model deletions automatically.
    """
    # Check if this model should be audited
    if sender not in AUDITED_MODELS:
        return
        
    # Get company
    company = get_company_from_instance(instance)
    if not company:
        return
        
    # Create a descriptive action message
    model_name = instance._meta.verbose_name or instance.__class__.__name__
    action_description = f"Deleted {model_name}: {instance}"
    
    # Create audit log
    AuditLog.objects.create(
        company=company,
        action_type=AuditLog.DELETE,
        action_description=action_description,
        content_type_id=instance._meta.app_label,
        object_id=str(instance.pk),
        # No user context in signals, system action
        user=None,
    )
