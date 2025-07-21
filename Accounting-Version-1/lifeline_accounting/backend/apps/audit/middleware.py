import json
import re
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.conf import settings
from .utils import log_action
from apps.accounts.models import Company


class AuditLogMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log user actions for auditing purposes.
    
    This middleware captures:
    - Login/logout events
    - API access for specified views
    - Other configurable actions
    """
    
    # URLs that should not be logged (to prevent excessive logging)
    EXCLUDED_URLS = [
        r'^/admin/jsi18n/',
        r'^/static/',
        r'^/media/',
        r'^/favicon\.ico$',
    ]
    
    # Add additional patterns here if needed
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        
    def process_request(self, request):
        # Store the request body for potential logging
        if request.content_type == 'application/json' and request.body:
            try:
                request._body_data = json.loads(request.body)
            except json.JSONDecodeError:
                request._body_data = None
        else:
            request._body_data = None
        
        # Continue processing the request
        return None
        
    def process_response(self, request, response):
        # Check if this URL should be logged
        if self._should_skip_logging(request):
            return response
            
        # Only log API calls
        if not request.path.startswith('/api/'):
            return response
            
        # Skip OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return response
            
        # Attempt to determine the action type and description
        action_info = self._get_action_info(request, response)
        if not action_info:
            return response
            
        action_type, action_description = action_info
        
        # Try to determine the company from the request
        company = self._get_company(request)
        if not company:
            # If we can't determine the company, we can't log
            return response
            
        # Log the action
        try:
            log_action(
                request=request,
                company=company,
                action_type=action_type,
                action_description=action_description,
                # No specific object for middleware-level logging
                details=f"URL: {request.path}, Method: {request.method}, Status: {response.status_code}"
            )
        except Exception as e:
            # Log the exception but don't interrupt the response
            if settings.DEBUG:
                print(f"Error logging audit action: {e}")
                
        return response
        
    def _should_skip_logging(self, request):
        """
        Determine if this request should be skipped for logging.
        """
        path = request.path
        
        # Check against excluded URL patterns
        for pattern in self.EXCLUDED_URLS:
            if re.match(pattern, path):
                return True
                
        return False
        
    def _get_action_info(self, request, response):
        """
        Determine the action type and description based on the request and response.
        Returns (action_type, action_description) or None if no logging should occur.
        """
        from .models import AuditLog
        
        method = request.method
        path = request.path
        status = response.status_code
        
        # Skip failed requests (except unauthorized, which we want to log)
        if status >= 400 and status != 401:
            return None
            
        # Handle login/logout
        if path.endswith('/api/login/') and method == 'POST' and status == 200:
            return (AuditLog.LOGIN, "User logged in")
            
        if path.endswith('/api/logout/') and status == 200:
            return (AuditLog.LOGOUT, "User logged out")
            
        # Handle common API actions
        if method == 'GET':
            # Skip listing endpoints to avoid excessive logging
            if path.endswith('/') and '/' not in path.rstrip('/'):
                return None
            return (AuditLog.VIEW, f"Viewed resource at {path}")
            
        if method == 'POST':
            return (AuditLog.CREATE, f"Created resource at {path}")
            
        if method == 'PUT' or method == 'PATCH':
            return (AuditLog.UPDATE, f"Updated resource at {path}")
            
        if method == 'DELETE':
            return (AuditLog.DELETE, f"Deleted resource at {path}")
            
        # Default case
        return (AuditLog.OTHER, f"{method} request to {path}")
        
    def _get_company(self, request):
        """
        Try to determine the company from the request.
        """
        # First check if company ID is in the request data
        company_id = None
        
        # Try to get from request body
        if hasattr(request, '_body_data') and request._body_data:
            company_id = request._body_data.get('company')
            
        # Try to get from query parameters
        if not company_id:
            company_id = request.GET.get('company')
            
        # Try to get from request user
        if not company_id and hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'active_company') and request.user.active_company:
                return request.user.active_company
                
        # If we found a company ID, get the company
        if company_id:
            try:
                return Company.objects.get(id=company_id)
            except (Company.DoesNotExist, ValueError):
                pass
                
        # If we couldn't determine the company, try to use a default one
        # This is just a fallback - in a real system you might not want this
        try:
            return Company.objects.first()
        except Company.DoesNotExist:
            return None
