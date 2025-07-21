from rest_framework.permissions import BasePermission
from apps.accounts.models import UserCompanyRole

class HasCompanyRole(BasePermission):
    """
    Custom permission to only allow users with a specific role in a company to access an endpoint.
    """
    def has_permission(self, request, view):
        company_id = request.headers.get('X-Company-ID')
        if not company_id:
            return False

        user = request.user
        if not user or not user.is_authenticated:
            return False

        try:
            role = UserCompanyRole.objects.get(user=user, company_id=company_id)
            return role.role in getattr(view, 'allowed_roles', [])
        except UserCompanyRole.DoesNotExist:
            return False
