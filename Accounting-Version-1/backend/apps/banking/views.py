from rest_framework import viewsets, permissions
from .models import BankAccount, BankStatementLine, ReconciliationEntry
from .serializers import BankAccountSerializer, BankStatementLineSerializer, ReconciliationEntrySerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return BankAccount.objects.filter(company_id=company_id)

class BankStatementLineViewSet(viewsets.ModelViewSet):
    queryset = BankStatementLine.objects.all()
    serializer_class = BankStatementLineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return BankStatementLine.objects.filter(bank_account__company_id=company_id)

class ReconciliationEntryViewSet(viewsets.ModelViewSet):
    queryset = ReconciliationEntry.objects.all()
    serializer_class = ReconciliationEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return ReconciliationEntry.objects.filter(statement_line__bank_account__company_id=company_id)
