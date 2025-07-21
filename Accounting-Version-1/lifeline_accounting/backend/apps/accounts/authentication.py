from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']) or None
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            return (user, validated_token)
        except Exception:
            return None
