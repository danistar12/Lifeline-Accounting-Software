from rest_framework import generics, permissions
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer, AuditLogDetailSerializer


class AuditLogPermission(permissions.BasePermission):
    """
    Custom permission to allow only company admins and superusers to view audit logs.
    """
    def has_permission(self, request, view):
        # Only allow authenticated users
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Superusers can access all logs
        if request.user.is_superuser:
            return True
            
        # For company-specific users, they must be an admin
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
            
        return False


class AuditLogListView(generics.ListAPIView):
    """
    API endpoint that allows audit logs to be viewed.
    """
    serializer_class = AuditLogSerializer
    permission_classes = [AuditLogPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['action_type', 'user', 'company']
    search_fields = ['action_description', 'details', 'user__username', 'user__email', 'ip_address']
    ordering_fields = ['timestamp', 'user__username', 'action_type']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        """
        Filter logs based on the user's access.
        """
        user = self.request.user
        
        # Superusers see all logs
        if user.is_superuser:
            return AuditLog.objects.all()
            
        # Company admins see only their company's logs
        if hasattr(user, 'company') and user.company:
            return AuditLog.objects.filter(company=user.company)
            
        # Active company if multi-company user
        if hasattr(user, 'active_company') and user.active_company:
            return AuditLog.objects.filter(company=user.active_company)
            
        # Fallback - no logs
        return AuditLog.objects.none()
        
    def filter_queryset(self, queryset):
        """
        Additional filtering beyond the standard filters.
        """
        queryset = super().filter_queryset(queryset)
        
        # Filter by content type if specified
        content_type_model = self.request.query_params.get('content_type_model')
        content_type_app = self.request.query_params.get('content_type_app')
        
        if content_type_model and content_type_app:
            try:
                content_type = ContentType.objects.get(
                    model=content_type_model,
                    app_label=content_type_app
                )
                queryset = queryset.filter(content_type=content_type)
            except ContentType.DoesNotExist:
                pass
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset


class AuditLogDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows a single audit log to be viewed.
    """
    serializer_class = AuditLogDetailSerializer
    permission_classes = [AuditLogPermission]
    
    def get_queryset(self):
        """
        Filter logs based on the user's access.
        """
        user = self.request.user
        
        # Superusers see all logs
        if user.is_superuser:
            return AuditLog.objects.all()
            
        # Company admins see only their company's logs
        if hasattr(user, 'company') and user.company:
            return AuditLog.objects.filter(company=user.company)
            
        # Active company if multi-company user
        if hasattr(user, 'active_company') and user.active_company:
            return AuditLog.objects.filter(company=user.active_company)
            
        # Fallback - no logs
        return AuditLog.objects.none()
