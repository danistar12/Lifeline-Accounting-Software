from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum, F
from .models import FixedAsset
from .serializers import FixedAssetSerializer
from decimal import Decimal

class FixedAssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FixedAssetSerializer
    
    def get_queryset(self):
        return FixedAsset.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns a summary of fixed assets including total value, depreciation, and count
        """
        assets = self.get_queryset()
        total_purchase_cost = assets.aggregate(Sum('purchase_cost'))['purchase_cost__sum'] or Decimal('0')
        total_current_value = assets.aggregate(Sum('current_value'))['current_value__sum'] or Decimal('0')
        total_depreciation = total_purchase_cost - total_current_value
        asset_count = assets.count()
        
        return Response({
            'total_purchase_cost': total_purchase_cost,
            'total_current_value': total_current_value,
            'total_depreciation': total_depreciation,
            'asset_count': asset_count
        })
