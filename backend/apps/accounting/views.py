from rest_framework import viewsets
from .models import ChartOfAccount, GeneralLedger
from .serializers import ChartOfAccountSerializer, GeneralLedgerSerializer

class ChartOfAccountViewSet(viewsets.ModelViewSet):
    queryset = ChartOfAccount.objects.all()
    serializer_class = ChartOfAccountSerializer

    def get_queryset(self):
        """
        Filter accounts by user's companies
        """
        user = self.request.user
        return ChartOfAccount.objects.filter(CompanyID__usercompanyrole__UserID=user)

class GeneralLedgerViewSet(viewsets.ModelViewSet):
    queryset = GeneralLedger.objects.all()
    serializer_class = GeneralLedgerSerializer

    def get_queryset(self):
        """
        Filter transactions by user's companies
        """
        user = self.request.user
        return GeneralLedger.objects.filter(CompanyID__usercompanyrole__UserID=user)

    def perform_create(self, serializer):
        """
        Set the user when creating a transaction
        """
        serializer.save(UserID=self.request.user)
