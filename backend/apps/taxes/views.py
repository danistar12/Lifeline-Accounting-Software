from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TaxRate, TaxTransaction
from .serializers import TaxRateSerializer, TaxTransactionSerializer

class TaxRateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaxRateSerializer
    
    def get_queryset(self):
        return TaxRate.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

class TaxTransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaxTransactionSerializer
    
    def get_queryset(self):
        return TaxTransaction.objects.filter(company=self.request.user.company)
