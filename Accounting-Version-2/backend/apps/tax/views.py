from rest_framework import viewsets
from .models import TaxRate, TaxTransaction
from .serializers import TaxRateSerializer, TaxTransactionSerializer

class TaxRateViewSet(viewsets.ModelViewSet):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer

class TaxTransactionViewSet(viewsets.ModelViewSet):
    queryset = TaxTransaction.objects.all()
    serializer_class = TaxTransactionSerializer
