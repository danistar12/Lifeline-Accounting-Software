from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for deployment verification
    """
    try:
        # Basic health checks
        from django.db import connection
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if we can import core modules
        from apps.accounts.models import User
        
        health_data = {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-11-07T00:00:00Z",
            "version": "2.0",
            "services": {
                "django": "running",
                "database": "connected",
                "auth": "available"
            }
        }
        
        return JsonResponse(health_data, status=200)
        
    except Exception as e:
        error_data = {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-11-07T00:00:00Z"
        }
        return JsonResponse(error_data, status=500)