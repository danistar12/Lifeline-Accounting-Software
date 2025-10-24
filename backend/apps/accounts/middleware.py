from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import time

class SessionSecurityMiddleware:
    """
    Middleware to enforce session security and automatic logout after inactivity
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Only check authenticated users
        if request.user.is_authenticated:
            current_time = time.time()
            
            # Check if this is the first request in session
            if 'last_activity' not in request.session:
                request.session['last_activity'] = current_time
                request.session['session_start'] = current_time
                request.session['user_id'] = request.user.id
                return response
            
            # Verify user identity hasn't changed (prevents admin hijacking)
            if request.session.get('user_id') != request.user.id:
                logout(request)
                if request.path.startswith('/api/'):
                    return JsonResponse({'error': 'Session security violation'}, status=401)
                return response
            
            last_activity = request.session.get('last_activity', current_time)
            time_since_activity = current_time - last_activity
            
            # Check for inactivity timeout (30 minutes = 1800 seconds)
            if time_since_activity > 1800:
                logout(request)
                # Clear all session data
                request.session.flush()
                if request.path.startswith('/api/'):
                    return JsonResponse({'error': 'Session expired due to inactivity'}, status=401)
                return response
            
            # Check for absolute session timeout (1 hour = 3600 seconds)
            session_start = request.session.get('session_start', current_time)
            total_session_time = current_time - session_start
            if total_session_time > 3600:
                logout(request)
                request.session.flush()
                if request.path.startswith('/api/'):
                    return JsonResponse({'error': 'Session expired - maximum time reached'}, status=401)
                return response
            
            # Update last activity time
            request.session['last_activity'] = current_time
        
        return response