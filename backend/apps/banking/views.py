from rest_framework import viewsets, permissions
from .models import BankAccount, BankStatementLine, ReconciliationEntry
from .serializers import BankAccountSerializer, BankStatementLineSerializer, ReconciliationEntrySerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return BankAccount.objects.filter(CompanyID=company_id)
        return BankAccount.objects.none()

class BankStatementLineViewSet(viewsets.ModelViewSet):
    queryset = BankStatementLine.objects.all()
    serializer_class = BankStatementLineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return BankStatementLine.objects.filter(BankAccountID__CompanyID=company_id)
        return BankStatementLine.objects.none()

class ReconciliationEntryViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationEntry.objects.all()
    serializer_class = ReconciliationEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return ReconciliationEntry.objects.filter(BankStatementLineID__BankAccountID__CompanyID=company_id)
        return ReconciliationEntry.objects.none()
