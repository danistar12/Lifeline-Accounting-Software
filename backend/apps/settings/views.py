from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from apps.accounts.models import UserSettings
from apps.accounts.serializers import UserSettingsSerializer

class SettingsViewSet(viewsets.ViewSet):
    """
    A ViewSet for retrieving and updating user settings and system settings.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'post'])
    def user(self, request):
        """
        GET: Retrieve user settings
        POST: Update user settings
        """
        user = request.user
        
        # Get or create user settings
        settings, created = UserSettings.objects.get_or_create(UserID=user)
        
        if request.method == 'GET':
            serializer = UserSettingsSerializer(settings)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'User settings updated successfully',
                    'data': serializer.data
                })
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_user(self, request):
        """
        Legacy endpoint - redirects to user() method
        """
        return self.user(request)

    @action(detail=False, methods=['get'])
    def system(self, request):
        # Example: return system-wide settings (stub)
        return Response({'maintenance_mode': False})

    @action(detail=False, methods=['post'])
    def update_system(self, request):
        # Example: update system-wide settings (stub)
        # Implement actual logic as needed
        return Response({'status': 'system settings updated'})
