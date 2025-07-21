from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from apps.core.models import GeneralLedger


class BalanceSheetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Aggregate net balances (debits - credits) by account type
        companies = request.user.companies.all()
        gl_entries = GeneralLedger.objects.filter(company__in=companies)
        balances = (
            gl_entries
            .annotate(net=ExpressionWrapper(F('debit_amount') - F('credit_amount'), output_field=DecimalField()))
            .values('account__account_type')
            .annotate(total=Sum('net'))
        )
        result = {item['account__account_type']: item['total'] for item in balances}
        return Response(result)


class IncomeStatementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Aggregate net revenue/expense (credits - debits) by account type
        companies = request.user.companies.all()
        gl_entries = GeneralLedger.objects.filter(company__in=companies)
        balances = (
            gl_entries
            .annotate(net=ExpressionWrapper(F('credit_amount') - F('debit_amount'), output_field=DecimalField()))
            .values('account__account_type')
            .annotate(total=Sum('net'))
        )
        result = {item['account__account_type']: item['total'] for item in balances}
        return Response(result)


class CashFlowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Placeholder implementation for cash flow
        # This should aggregate cash-related GL entries in a real implementation
        return Response({'detail': 'Cash flow report not implemented'})
