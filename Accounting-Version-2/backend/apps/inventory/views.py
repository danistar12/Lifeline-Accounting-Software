from rest_framework import viewsets
from .models import InventoryLocation, Inventory
from .serializers import InventoryLocationSerializer, InventorySerializer
from apps.core.permissions import HasCompanyRole

class InventoryLocationViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryLocationSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Inventory Manager']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return InventoryLocation.objects.filter(company_id=company_id)

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Inventory Manager']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Inventory.objects.filter(company_id=company_id)
