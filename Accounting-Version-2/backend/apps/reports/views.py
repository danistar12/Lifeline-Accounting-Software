from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, Q
from django.db.models.functions import TruncMonth, TruncWeek
from apps.core.permissions import HasCompanyRole
from apps.core.models import ChartOfAccounts, GeneralLedger
from apps.banking.models import BankTransaction, BankAccount
from apps.payroll.models import Employee, Payroll, PayrollDeduction
from apps.contacts.models import Customer, Vendor
from datetime import datetime, timedelta
from django.utils import timezone

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


class PayrollSummaryView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Get payroll data
        qs = Payroll.objects.filter(employee__company__in=companies)
        if start_date:
            qs = qs.filter(pay_period_start__gte=start_date)
        if end_date:
            qs = qs.filter(pay_period_end__lte=end_date)
            
        # Calculate totals
        totals = qs.aggregate(
            total_gross=Sum('gross_pay'),
            total_net=Sum('net_pay'),
            total_taxes=Sum('taxes_withheld'),
            total_records=Count('payroll_id')
        )
        
        # Monthly breakdown
        monthly_data = qs.annotate(
            month=TruncMonth('pay_period_start')
        ).values('month').annotate(
            gross_pay=Sum('gross_pay'),
            net_pay=Sum('net_pay'),
            taxes_withheld=Sum('taxes_withheld'),
            payroll_count=Count('payroll_id')
        ).order_by('month')
        
        # Employee breakdown
        employee_data = qs.values(
            'employee__name', 'employee__email', 'employee__hourly_rate'
        ).annotate(
            total_gross=Sum('gross_pay'),
            total_net=Sum('net_pay'),
            total_taxes=Sum('taxes_withheld'),
            pay_periods=Count('payroll_id')
        ).order_by('-total_gross')
        
        data = {
            'summary': totals,
            'monthly_breakdown': list(monthly_data),
            'employee_breakdown': list(employee_data),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
        return Response(data)


class EmployeeListView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        
        employees = Employee.objects.filter(company__in=companies).values(
            'employee_id', 'name', 'email', 'hourly_rate', 
            'tax_withholding', 'created_date', 'company__company_name'
        )
        
        # Get recent payroll for each employee
        for employee in employees:
            recent_payroll = Payroll.objects.filter(
                employee_id=employee['employee_id']
            ).order_by('-pay_period_end').first()
            
            if recent_payroll:
                employee['last_pay_date'] = recent_payroll.payment_date
                employee['last_gross_pay'] = recent_payroll.gross_pay
                employee['last_net_pay'] = recent_payroll.net_pay
            else:
                employee['last_pay_date'] = None
                employee['last_gross_pay'] = 0
                employee['last_net_pay'] = 0
        
        return Response({'employees': list(employees)})


class FinancialDashboardView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        
        # Current month date range
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Bank account balances
        bank_accounts = BankAccount.objects.filter(company__in=companies).aggregate(
            total_balance=Sum('balance'),
            account_count=Count('bank_account_id')
        )
        
        # Recent transactions (last 30 days)
        recent_transactions = BankTransaction.objects.filter(
            bank_account__company__in=companies,
            transaction_date__gte=now - timedelta(days=30)
        ).aggregate(
            total_inflow=Sum('amount', filter=Q(amount__gt=0)),
            total_outflow=Sum('amount', filter=Q(amount__lt=0)),
            transaction_count=Count('bank_transaction_id')
        )
        
        # Payroll summary (current month)
        payroll_summary = Payroll.objects.filter(
            employee__company__in=companies,
            pay_period_start__gte=start_of_month
        ).aggregate(
            total_gross=Sum('gross_pay'),
            total_net=Sum('net_pay'),
            total_taxes=Sum('taxes_withheld'),
            payroll_count=Count('payroll_id')
        )
        
        # Employee count
        employee_count = Employee.objects.filter(company__in=companies).count()
        
        # Customer/Vendor counts
        customer_count = Customer.objects.filter(company__in=companies).count()
        vendor_count = Vendor.objects.filter(company__in=companies).count()
        
        data = {
            'banking': {
                'total_balance': bank_accounts.get('total_balance') or 0,
                'account_count': bank_accounts.get('account_count') or 0,
                'recent_inflow': recent_transactions.get('total_inflow') or 0,
                'recent_outflow': abs(recent_transactions.get('total_outflow') or 0),
                'recent_transaction_count': recent_transactions.get('transaction_count') or 0
            },
            'payroll': {
                'current_month_gross': payroll_summary.get('total_gross') or 0,
                'current_month_net': payroll_summary.get('total_net') or 0,
                'current_month_taxes': payroll_summary.get('total_taxes') or 0,
                'current_month_payrolls': payroll_summary.get('payroll_count') or 0,
                'employee_count': employee_count
            },
            'business': {
                'customer_count': customer_count,
                'vendor_count': vendor_count
            },
            'period': {
                'current_month': start_of_month.date(),
                'last_30_days': (now - timedelta(days=30)).date()
            }
        }
        return Response(data)


class BankingReportView(APIView):
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Viewer']

    def get(self, request):
        user = request.user
        companies = user.companies.all()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Bank accounts with balances
        bank_accounts = BankAccount.objects.filter(company__in=companies).values(
            'bank_account_id', 'bank_name', 'account_number', 
            'account_type', 'balance', 'currency_code'
        )
        
        # Transactions
        qs = BankTransaction.objects.filter(bank_account__company__in=companies)
        if start_date:
            qs = qs.filter(transaction_date__gte=start_date)
        if end_date:
            qs = qs.filter(transaction_date__lte=end_date)
            
        # Transaction summary
        transaction_summary = qs.aggregate(
            total_inflow=Sum('amount', filter=Q(amount__gt=0)),
            total_outflow=Sum('amount', filter=Q(amount__lt=0)),
            transaction_count=Count('bank_transaction_id'),
            reconciled_count=Count('bank_transaction_id', filter=Q(reconciled=True))
        )
        
        # Daily transaction breakdown
        daily_transactions = qs.annotate(
            date=TruncWeek('transaction_date')
        ).values('date').annotate(
            inflow=Sum('amount', filter=Q(amount__gt=0)),
            outflow=Sum('amount', filter=Q(amount__lt=0)),
            count=Count('bank_transaction_id')
        ).order_by('date')
        
        # Recent transactions
        recent_transactions = qs.select_related('bank_account').order_by('-transaction_date')[:20].values(
            'transaction_date', 'description', 'amount', 'transaction_type',
            'reconciled', 'bank_account__bank_name', 'bank_account__account_number'
        )
        
        data = {
            'accounts': list(bank_accounts),
            'summary': transaction_summary,
            'weekly_breakdown': list(daily_transactions),
            'recent_transactions': list(recent_transactions),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
        return Response(data)
