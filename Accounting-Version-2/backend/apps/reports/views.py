from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from apps.core.permissions import HasCompanyRole
from apps.core.models import ChartOfAccounts, GeneralLedger
from apps.banking.models import BankTransaction

class ProfitLossView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        qs = GeneralLedger.objects.filter(company__in=companies)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        revenue = qs.filter(account__account_type='Revenue').aggregate(total_credit=Sum('credit'), total_debit=Sum('debit'))
        expense = qs.filter(account__account_type='Expense').aggregate(total_credit=Sum('credit'), total_debit=Sum('debit'))
        net_income = (revenue.get('total_credit') or 0) - (expense.get('total_debit') or 0)
        data = {
            'revenue': revenue,
            'expense': expense,
            'net_income': net_income,
        }
        return Response(data)

class BalanceSheetView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        accounts = ChartOfAccounts.objects.filter(company__in=companies)
        assets = accounts.filter(account_type='Asset').aggregate(total_balance=Sum('balance'))
        liabilities = accounts.filter(account_type='Liability').aggregate(total_balance=Sum('balance'))
        equity = accounts.filter(account_type='Equity').aggregate(total_balance=Sum('balance'))
        data = {
            'assets': assets,
            'liabilities': liabilities,
            'equity': equity,
        }
        return Response(data)

class CashFlowView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        qs = BankTransaction.objects.filter(bank_account__company__in=companies)
        if start_date:
            qs = qs.filter(transaction_date__gte=start_date)
        if end_date:
            qs = qs.filter(transaction_date__lte=end_date)
        inflow = qs.filter(amount__gt=0).aggregate(total_inflow=Sum('amount'))
        outflow = qs.filter(amount__lt=0).aggregate(total_outflow=Sum('amount'))
        data = {
            'inflow': inflow.get('total_inflow') or 0,
            'outflow': outflow.get('total_outflow') or 0,
        }
        return Response(data)
