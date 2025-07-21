from rest_framework import viewsets
from .models import InventoryCategory, InventoryItem
from .serializers import InventoryCategorySerializer, InventoryItemSerializer
from apps.core.permissions import HasCompanyRole

class InventoryCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryCategorySerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Inventory Manager']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return InventoryCategory.objects.filter(company_id=company_id)

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Inventory Manager']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return InventoryItem.objects.filter(company_id=company_id)
