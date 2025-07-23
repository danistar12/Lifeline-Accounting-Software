from django.shortcuts import render
from rest_framework import viewsets
from .models import BankAccount, BankTransaction
from .serializers import BankAccountSerializer, BankTransactionSerializer
from apps.core.permissions import HasCompanyRole

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get_queryset(self):
        user = self.request.user
        return BankAccount.objects.filter(company__in=user.companies.all())

class BankTransactionViewSet(viewsets.ModelViewSet):
    queryset = BankTransaction.objects.all()
    serializer_class = BankTransactionSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get_queryset(self):
        user = self.request.user
        return BankTransaction.objects.filter(bank_account__company__in=user.companies.all())
