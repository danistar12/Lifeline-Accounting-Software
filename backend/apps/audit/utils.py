from django.contrib.contenttypes.models import ContentType
from .models import AuditLog


def get_client_ip(request):
    """
    Get client IP address from request.
    
    Args:
        request: Django request object
        
    Returns:
        tuple: (ip_address, is_routable)
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    
    # Check if IP is private/non-routable
    is_routable = True
    private_ips = [
    '0.0.0.0', 'localhost',  # localhost
        '10.0.0.0/8',            # Class A private network
        '172.16.0.0/12',         # Class B private networks
        '192.168.0.0/16',        # Class C private networks
    ]
    
    # Simple check - not as comprehensive as ipware but works for most cases
    for private_ip in private_ips:
        if '/' in private_ip:
            network, bits = private_ip.split('/')
            network_parts = [int(p) for p in network.split('.')]
            ip_parts = [int(p) for p in ip.split('.')]
            
            # Simple subnet check
            if bits == '8':
                if ip_parts[0] == network_parts[0]:
                    is_routable = False
                    break
            elif bits == '12':
                if (ip_parts[0] == network_parts[0] and 
                    ip_parts[1] >= network_parts[1] and 
                    ip_parts[1] < network_parts[1] + 16):
                    is_routable = False
                    break
            elif bits == '16':
                if (ip_parts[0] == network_parts[0] and 
                    ip_parts[1] == network_parts[1]):
                    is_routable = False
                    break
        else:
            if ip == private_ip:
                is_routable = False
                break
    
    return ip, is_routable


def log_action(request, company, action_type, action_description, obj=None, data_before=None, data_after=None, details=None):
    """
    Log an action performed by a user or system.
    
    Args:
        request: The Django request object (can be None for system actions)
        company: The company instance this action belongs to
        action_type: Type of action (see AuditLog.ACTION_CHOICES)
        action_description: Description of the action
        obj: The object that was affected (optional)
        data_before: JSON-serializable data representing the state before (optional)
        data_after: JSON-serializable data representing the state after (optional)
        details: Additional textual details about the action (optional)
    
    Returns:
        The created AuditLog instance
    """
    # Initialize audit log data
    audit_data = {
        'CompanyID': company,
        'ActionType': action_type,
        'ActionDescription': action_description,
        'Details': details,
        'DataBefore': data_before,
        'DataAfter': data_after,
    }
    
    # Set user information if a request was provided
    if request:
        # Set user if authenticated
        if request.user and request.user.is_authenticated:
            audit_data['UserID'] = request.user
        
        # Get IP address
        client_ip, is_routable = get_client_ip(request)
        
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT')
        if user_agent:
            audit_data['UserAgent'] = user_agent
    
    # Set content object if provided
    if obj:
        audit_data['ContentType'] = ContentType.objects.get_for_model(obj)
        audit_data['ObjectID'] = str(obj.pk)
    
    # Create and return the audit log entry
    return AuditLog.objects.create(**audit_data)


def get_object_changes(old_instance, new_instance, exclude_fields=None):
    """
    Compare two model instances and return a dictionary of changes.
    
    Args:
        old_instance: The model instance before changes
        new_instance: The model instance after changes
        exclude_fields: List of field names to exclude from comparison
    
    Returns:
        tuple: (data_before, data_after) dictionaries containing only changed fields
    """
    if exclude_fields is None:
        exclude_fields = []
    
    # Standard fields to exclude
    exclude_fields.extend(['modified_at', 'updated_at', 'last_updated', 'modified_by'])
    
    # Get all field names
    fields = [field.name for field in old_instance._meta.fields 
              if field.name not in exclude_fields]
    
    data_before = {}
    data_after = {}
    
    for field in fields:
        old_value = getattr(old_instance, field)
        new_value = getattr(new_instance, field)
        
        # Handle many-to-many fields and FK relationships
        if hasattr(old_value, 'all'):  # Many-to-many or reverse FK
            continue
        
        # Convert non-serializable objects to string representation
        if hasattr(old_value, 'pk'):  # Foreign key
            old_value = str(old_value)
            
        if hasattr(new_value, 'pk'):  # Foreign key
            new_value = str(new_value)
            
        # Only include fields that have changed
        if old_value != new_value:
            data_before[field] = old_value
            data_after[field] = new_value
    
    return data_before, data_after
