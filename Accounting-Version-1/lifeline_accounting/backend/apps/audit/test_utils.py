"""
Helper functions for testing audit logs in unit tests.
"""
from apps.audit.models import AuditLog
from django.contrib.auth import get_user_model
from apps.accounts.models import Company
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


def create_test_audit_log(company=None, user=None, action_type=AuditLog.OTHER, 
                         action_description="Test log entry", obj=None):
    """
    Creates an audit log entry for testing purposes.
    
    Args:
        company: The company instance (will create a test company if None)
        user: The user instance (will create a test user if None)
        action_type: The action type from AuditLog.ACTION_CHOICES
        action_description: Description of the action
        obj: Optional related object
        
    Returns:
        AuditLog instance
    """
    # Create test company if not provided
    if company is None:
        company, _ = Company.objects.get_or_create(
            name="Test Company",
            defaults={
                "legal_name": "Test Company, Inc.",
                "currency": "USD",
                "fiscal_year_end": "12-31"
            }
        )
        
    # Create test user if not provided
    if user is None:
        user, _ = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "test@example.com",
                "is_active": True
            }
        )
        
    # Create audit log entry
    audit_data = {
        "company": company,
        "user": user,
        "action_type": action_type,
        "action_description": action_description,
    }
    
    # Set content object if provided
    if obj:
        audit_data["content_type"] = ContentType.objects.get_for_model(obj)
        audit_data["object_id"] = obj.pk
        
    return AuditLog.objects.create(**audit_data)


def assert_audit_log_created(test_case, action_type=None, action_description=None, 
                            user=None, company=None, content_type=None, object_id=None):
    """
    Asserts that an audit log with the given criteria was created.
    Useful in test cases to verify that actions are being audited.
    
    Args:
        test_case: The TestCase instance
        action_type: The action type to look for
        action_description: Text that should be in the action description
        user: The user who should have performed the action
        company: The company the action should be associated with
        content_type: The content type that should be referenced
        object_id: The object ID that should be referenced
        
    Returns:
        The matching AuditLog instance if found, otherwise raises AssertionError
    """
    # Build query
    query = {}
    if action_type:
        query["action_type"] = action_type
    if user:
        query["user"] = user
    if company:
        query["company"] = company
    if content_type:
        if isinstance(content_type, str):
            app_label, model = content_type.split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        query["content_type"] = content_type
    if object_id:
        query["object_id"] = str(object_id)
        
    # Find matching logs
    logs = AuditLog.objects.filter(**query).order_by('-timestamp')
    
    # Filter by description text if provided
    if action_description and logs:
        logs = [log for log in logs if action_description in log.action_description]
        
    # Assert we found a match
    test_case.assertTrue(logs, f"No audit log found matching criteria: {query}")
    
    return logs[0]  # Return the most recent match
