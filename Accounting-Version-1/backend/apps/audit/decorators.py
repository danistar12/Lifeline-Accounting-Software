import functools
from django.db import transaction
from .utils import log_action, get_object_changes


def audit_view(action_type=None, description_template=None):
    """
    Decorator to audit actions performed in a DRF view.
    
    Args:
        action_type: The action type from AuditLog.ACTION_CHOICES
        description_template: A template string that will be formatted with view attributes.
            Available placeholders: {object}, {model}, {pk}, {method}
            
    Example:
        @audit_view(action_type=AuditLog.UPDATE, description_template="Updated {model} {pk}")
        def update(self, request, *args, **kwargs):
            ...
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(self, request, *args, **kwargs):
            from .models import AuditLog
            
            # Get object if available (for retrieve, update, destroy)
            obj = None
            try:
                if hasattr(self, 'get_object'):
                    obj = self.get_object()
            except Exception:
                obj = None
                
            # Save old state for comparison if we're updating
            old_data = None
            if obj and action_type == AuditLog.UPDATE:
                old_data = {
                    field.name: getattr(obj, field.name)
                    for field in obj._meta.fields
                    if not field.name.startswith('_')
                }
                
            # For views that might affect multiple objects
            queryset = None
            if not obj and hasattr(self, 'get_queryset'):
                try:
                    queryset = self.get_queryset()
                except Exception:
                    queryset = None
                    
            # Execute the original view function
            with transaction.atomic():
                response = view_func(self, request, *args, **kwargs)
                
                # Determine action type if not provided
                final_action_type = action_type
                if not final_action_type:
                    if request.method == 'GET':
                        final_action_type = AuditLog.VIEW
                    elif request.method == 'POST':
                        final_action_type = AuditLog.CREATE
                    elif request.method in ('PUT', 'PATCH'):
                        final_action_type = AuditLog.UPDATE
                    elif request.method == 'DELETE':
                        final_action_type = AuditLog.DELETE
                    else:
                        final_action_type = AuditLog.OTHER
                        
                # Format description
                if description_template:
                    # Get object from response data if created
                    if not obj and final_action_type == AuditLog.CREATE and hasattr(response, 'data'):
                        # Try to get the created object
                        try:
                            model_class = self.get_serializer().Meta.model
                            obj_id = response.data.get('id')
                            if obj_id:
                                obj = model_class.objects.get(pk=obj_id)
                        except Exception:
                            pass
                            
                    # Format the description
                    model_name = None
                    pk_value = None
                    
                    if obj:
                        model_name = obj._meta.model.__name__
                        pk_value = obj.pk
                    elif queryset:
                        model_name = queryset.model.__name__
                        pk_value = kwargs.get('pk', None)
                        
                    description = description_template.format(
                        object=str(obj) if obj else None,
                        model=model_name,
                        pk=pk_value,
                        method=request.method
                    )
                else:
                    # Default description based on view name and method
                    view_name = self.__class__.__name__
                    description = f"{request.method} {view_name}"
                    
                # Determine company
                company = None
                # Try to get from request user's active company
                if hasattr(request.user, 'active_company') and request.user.active_company:
                    company = request.user.active_company
                # Try to get from the object
                elif obj and hasattr(obj, 'company'):
                    company = obj.company
                # Try to get from query params or POST data
                else:
                    company_id = request.query_params.get('company') or request.data.get('company')
                    if company_id:
                        from apps.accounts.models import Company
                        try:
                            company = Company.objects.get(id=company_id)
                        except Company.DoesNotExist:
                            pass
                            
                # Can't log without a company
                if not company:
                    return response
                    
                # For updates, get new state and compare
                data_before = None
                data_after = None
                
                if final_action_type == AuditLog.UPDATE and obj and old_data:
                    # Refresh object from database
                    obj.refresh_from_db()
                    
                    # Get current state
                    new_data = {
                        field.name: getattr(obj, field.name)
                        for field in obj._meta.fields
                        if not field.name.startswith('_')
                    }
                    
                    # Filter to changed fields
                    data_before = {}
                    data_after = {}
                    
                    for key, old_value in old_data.items():
                        new_value = new_data.get(key)
                        if old_value != new_value:
                            # Handle non-JSON serializable types
                            if hasattr(old_value, 'isoformat'):  # Date/datetime
                                old_value = old_value.isoformat()
                            if hasattr(new_value, 'isoformat'):
                                new_value = new_value.isoformat()
                                
                            data_before[key] = old_value
                            data_after[key] = new_value
                            
                # Log the action
                log_action(
                    request=request,
                    company=company,
                    action_type=final_action_type,
                    action_description=description,
                    obj=obj,
                    data_before=data_before,
                    data_after=data_after
                )
                
                return response
                
        return wrapped_view
    return decorator


def audit_change(view_func=None, action_description=None):
    """
    Simpler decorator for auditing model changes in ViewSets.
    This will automatically determine the action type and description.
    
    Args:
        view_func: The view function to wrap
        action_description: Optional description override
        
    When used without arguments: @audit_change
    When used with arguments: @audit_change(action_description="Custom description")
    """
    if view_func is None:
        return lambda f: audit_change(f, action_description)
        
    @functools.wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        from .models import AuditLog
        
        # Determine action type based on viewset action
        action_type = None
        if hasattr(self, 'action'):
            if self.action == 'list':
                action_type = AuditLog.VIEW
            elif self.action == 'retrieve':
                action_type = AuditLog.VIEW
            elif self.action == 'create':
                action_type = AuditLog.CREATE
            elif self.action in ('update', 'partial_update'):
                action_type = AuditLog.UPDATE
            elif self.action == 'destroy':
                action_type = AuditLog.DELETE
                
        # Create a default description
        if not action_description and hasattr(self, 'action') and hasattr(self, 'get_serializer'):
            model_name = self.get_serializer().Meta.model.__name__
            
            if self.action == 'list':
                description = f"Viewed {model_name} list"
            elif self.action == 'retrieve':
                description = f"Viewed {model_name} {{pk}}"
            elif self.action == 'create':
                description = f"Created new {model_name}"
            elif self.action in ('update', 'partial_update'):
                description = f"Updated {model_name} {{pk}}"
            elif self.action == 'destroy':
                description = f"Deleted {model_name} {{pk}}"
            else:
                description = f"{self.action.capitalize()} {model_name}"
        else:
            description = action_description
            
        # Apply the detailed decorator
        decorator = audit_view(action_type=action_type, description_template=description)
        return decorator(view_func)(self, request, *args, **kwargs)
        
    return wrapped_view
