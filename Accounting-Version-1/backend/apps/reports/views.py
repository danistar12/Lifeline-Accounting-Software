from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q, Value, CharField
from django.db.models.functions import Coalesce
from django.utils import timezone
from apps.accounting.models import GeneralLedger, ChartOfAccount
from decimal import Decimal
from .serializers import (
    ReportPeriodSerializer, 
    BalanceSheetSerializer, 
    IncomeStatementSerializer, 
    CashFlowSerializer,
    FinancialReportItemSerializer
)
from datetime import datetime


class BalanceSheetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get date parameters or use current date
        end_date = request.query_params.get('end_date', timezone.now().date().isoformat())
        
        try:
            end_date = datetime.fromisoformat(end_date).date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use ISO format (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        company = request.user.company
        
        # Get asset accounts
        asset_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type__in=['ASSET', 'CURRENT_ASSET', 'FIXED_ASSET']
        )
        
        # Get liability accounts
        liability_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type__in=['LIABILITY', 'CURRENT_LIABILITY', 'LONG_TERM_LIABILITY']
        )
        
        # Get equity accounts
        equity_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type__in=['EQUITY', 'RETAINED_EARNINGS']
        )
        
        # Calculate balances for each account type
        asset_items = []
        liability_items = []
        equity_items = []
        
        total_assets = Decimal('0')
        total_liabilities = Decimal('0')
        total_equity = Decimal('0')
        
        # Process asset accounts
        for account in asset_accounts:
            balance = self._calculate_account_balance(account, end_date)
            asset_items.append({
                'account_type': account.account_type,
                'account_name': account.account_name,
                'balance': balance
            })
            total_assets += balance
            
        # Process liability accounts
        for account in liability_accounts:
            balance = self._calculate_account_balance(account, end_date)
            liability_items.append({
                'account_type': account.account_type,
                'account_name': account.account_name,
                'balance': balance
            })
            total_liabilities += balance
            
        # Process equity accounts
        for account in equity_accounts:
            balance = self._calculate_account_balance(account, end_date)
            equity_items.append({
                'account_type': account.account_type,
                'account_name': account.account_name,
                'balance': balance
            })
            total_equity += balance
            
        # Prepare response data
        data = {
            'assets': asset_items,
            'liabilities': liability_items,
            'equity': equity_items,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'total_equity': total_equity
        }
        
        serializer = BalanceSheetSerializer(data)
        return Response(serializer.data)
    
    def _calculate_account_balance(self, account, end_date):
        """Helper method to calculate account balance up to a specific date"""
        gl_entries = GeneralLedger.objects.filter(
            account=account,
            transaction_date__lte=end_date
        )
        
        debits = gl_entries.aggregate(total=Coalesce(Sum('debit_amount'), Value(0)))['total']
        credits = gl_entries.aggregate(total=Coalesce(Sum('credit_amount'), Value(0)))['total']
        
        if account.account_type in ['ASSET', 'CURRENT_ASSET', 'FIXED_ASSET', 'EXPENSE']:
            # Debit accounts: debit increases, credit decreases
            balance = debits - credits
        else:
            # Credit accounts: credit increases, debit decreases
            balance = credits - debits
            
        return balance


class IncomeStatementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get date parameters
        serializer = ReportPeriodSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        company = request.user.company
        
        # Get revenue accounts
        revenue_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type='REVENUE'
        )
        
        # Get expense accounts
        expense_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type='EXPENSE'
        )
        
        # Calculate balances for each account type
        revenue_items = []
        expense_items = []
        
        total_revenue = Decimal('0')
        total_expenses = Decimal('0')
        
        # Process revenue accounts
        for account in revenue_accounts:
            balance = self._calculate_account_balance(account, start_date, end_date)
            revenue_items.append({
                'account_type': account.account_type,
                'account_name': account.account_name,
                'balance': balance
            })
            total_revenue += balance
            
        # Process expense accounts
        for account in expense_accounts:
            balance = self._calculate_account_balance(account, start_date, end_date)
            expense_items.append({
                'account_type': account.account_type,
                'account_name': account.account_name,
                'balance': balance
            })
            total_expenses += balance
            
        # Calculate net income
        net_income = total_revenue - total_expenses
            
        # Prepare response data
        data = {
            'revenue': revenue_items,
            'expenses': expense_items,
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income
        }
        
        serializer = IncomeStatementSerializer(data)
        return Response(serializer.data)
    
    def _calculate_account_balance(self, account, start_date, end_date):
        """Helper method to calculate account balance between dates"""
        gl_entries = GeneralLedger.objects.filter(
            account=account,
            transaction_date__gte=start_date,
            transaction_date__lte=end_date
        )
        
        debits = gl_entries.aggregate(total=Coalesce(Sum('debit_amount'), Value(0)))['total']
        credits = gl_entries.aggregate(total=Coalesce(Sum('credit_amount'), Value(0)))['total']
        
        if account.account_type == 'REVENUE':
            # Revenue is a credit account
            balance = credits - debits
        else:
            # Expense is a debit account
            balance = debits - credits
            
        return balance


class CashFlowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get date parameters
        serializer = ReportPeriodSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        company = request.user.company
        
        # Get cash accounts
        cash_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type='CURRENT_ASSET',
            account_name__icontains='cash'
        )
        
        if not cash_accounts.exists():
            return Response(
                {"error": "No cash accounts found for cash flow analysis"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Calculate beginning cash balance
        beginning_cash_balance = Decimal('0')
        for account in cash_accounts:
            beginning_balance = self._calculate_account_balance(account, None, start_date - timezone.timedelta(days=1))
            beginning_cash_balance += beginning_balance
            
        # Simplified cash flow categories
        operating_activities = [
            {
                'account_type': 'Operating',
                'account_name': 'Net Income from Operations',
                'balance': self._calculate_net_income(company, start_date, end_date)
            }
        ]
        
        # For a real application, we would need more detailed analysis of cash flow components
        investing_activities = []
        financing_activities = []
        
        # Calculate ending cash balance
        ending_cash_balance = Decimal('0')
        for account in cash_accounts:
            ending_balance = self._calculate_account_balance(account, None, end_date)
            ending_cash_balance += ending_balance
            
        # Net cash change
        net_cash_change = ending_cash_balance - beginning_cash_balance
            
        # Prepare response data
        data = {
            'operating_activities': operating_activities,
            'investing_activities': investing_activities,
            'financing_activities': financing_activities,
            'net_cash_change': net_cash_change,
            'beginning_cash_balance': beginning_cash_balance,
            'ending_cash_balance': ending_cash_balance
        }
        
        serializer = CashFlowSerializer(data)
        return Response(serializer.data)
    
    def _calculate_account_balance(self, account, start_date=None, end_date=None):
        """Helper method to calculate account balance between dates"""
        gl_entries = GeneralLedger.objects.filter(account=account)
        
        if start_date:
            gl_entries = gl_entries.filter(transaction_date__gte=start_date)
            
        if end_date:
            gl_entries = gl_entries.filter(transaction_date__lte=end_date)
        
        debits = gl_entries.aggregate(total=Coalesce(Sum('debit_amount'), Value(0)))['total']
        credits = gl_entries.aggregate(total=Coalesce(Sum('credit_amount'), Value(0)))['total']
        
        # Cash is an asset account
        balance = debits - credits
        return balance
    
    def _calculate_net_income(self, company, start_date, end_date):
        """Helper method to calculate net income for the period"""
        # Get revenue entries
        revenue_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type='REVENUE'
        )
        
        revenue_entries = GeneralLedger.objects.filter(
            account__in=revenue_accounts,
            transaction_date__gte=start_date,
            transaction_date__lte=end_date
        )
        
        # Get expense entries
        expense_accounts = ChartOfAccount.objects.filter(
            company=company,
            account_type='EXPENSE'
        )
        
        expense_entries = GeneralLedger.objects.filter(
            account__in=expense_accounts,
            transaction_date__gte=start_date,
            transaction_date__lte=end_date
        )
        
        # Calculate net income
        revenue = revenue_entries.aggregate(
            total=Coalesce(Sum(F('credit_amount') - F('debit_amount')), Value(0))
        )['total']
        
        expenses = expense_entries.aggregate(
            total=Coalesce(Sum(F('debit_amount') - F('credit_amount')), Value(0))
        )['total']
        
        return revenue - expenses
