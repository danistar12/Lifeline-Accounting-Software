from rest_framework import viewsets, permissions
from .models import ChartOfAccount, GeneralLedger
from .serializers import ChartOfAccountSerializer, GeneralLedgerSerializer

class ChartOfAccountViewSet(viewsets.ModelViewSet):
    serializer_class = ChartOfAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return ChartOfAccount.objects.filter(company_id=company_id)

class GeneralLedgerViewSet(viewsets.ModelViewSet):
    serializer_class = GeneralLedgerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return GeneralLedger.objects.filter(company_id=company_id)
