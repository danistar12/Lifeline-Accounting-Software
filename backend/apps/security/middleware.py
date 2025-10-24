import logging
from django.http import JsonResponse
from django.core.cache import cache
import time

logger = logging.getLogger(__name__)

class FedRAMPSecurityMiddleware:
    """
    FedRAMP-compliant security middleware with enhanced logging and threat detection
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.failed_login_threshold = 5
        self.lockout_duration = 900  # 15 minutes

    def __call__(self, request):
        # Log all requests for audit trail
        client_ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        
        # Check for suspicious activity
        if self.is_ip_blocked(client_ip):
            logger.warning(f"Blocked request from {client_ip} - IP is temporarily locked")
            return JsonResponse({'error': 'Access temporarily restricted'}, status=429)
        
        # Rate limiting check
        if self.is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JsonResponse({'error': 'Too many requests'}, status=429)
        
        response = self.get_response(request)
        
        # Log authentication events
        if hasattr(request, 'user') and request.user.is_authenticated:
            if request.path.startswith('/api/accounts/auth/login/'):
                logger.info(f"Successful login - User: {request.user.username}, IP: {client_ip}, UA: {user_agent}")
        
        # Add security headers
        self.add_security_headers(response)
        
        return response

    def get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_ip_blocked(self, ip):
        """Check if IP is temporarily blocked due to failed attempts"""
        return cache.get(f"blocked_ip_{ip}", False)

    def is_rate_limited(self, ip):
        """Basic rate limiting - 100 requests per minute"""
        cache_key = f"rate_limit_{ip}"
        requests = cache.get(cache_key, 0)
        if requests > 100:
            return True
        cache.set(cache_key, requests + 1, 60)  # 1 minute window
        return False

    def add_security_headers(self, response):
        """Add FedRAMP-compliant security headers"""
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    def block_ip(self, ip, duration=900):
        """Block an IP address for specified duration"""
        cache.set(f"blocked_ip_{ip}", True, duration)
        logger.critical(f"IP {ip} blocked for {duration} seconds due to security violation")

class AuditLoggingMiddleware:
    """
    Comprehensive audit logging for FedRAMP compliance
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        client_ip = self.get_client_ip(request)
        
        # Log request details
        if request.user.is_authenticated:
            user_id = request.user.id
            username = request.user.username
        else:
            user_id = None
            username = 'Anonymous'
        
        response = self.get_response(request)
        
        # Calculate response time
        response_time = (time.time() - start_time) * 1000
        
        # Log access attempt
        logger.info(
            f"ACCESS - User: {username} (ID: {user_id}) | "
            f"IP: {client_ip} | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Status: {response.status_code} | "
            f"Time: {response_time:.2f}ms"
        )
        
        # Log data modification attempts
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            logger.info(
                f"DATA_CHANGE - User: {username} | "
                f"Action: {request.method} | "
                f"Endpoint: {request.path} | "
                f"Status: {response.status_code}"
            )
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip