from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User

class SettingsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for retrieving and updating user or system settings.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def user(self, request):
        # Example: return user profile/settings
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            # Add more user settings here
        })

    @action(detail=False, methods=['post'])
    def update_user(self, request):
        # Example: update user settings
        user = request.user
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({'status': 'user settings updated'})

    @action(detail=False, methods=['get'])
    def system(self, request):
        # Example: return system-wide settings (stub)
        return Response({'maintenance_mode': False})

    @action(detail=False, methods=['post'])
    def update_system(self, request):
        # Example: update system-wide settings (stub)
        # Implement actual logic as needed
        return Response({'status': 'system settings updated'})
