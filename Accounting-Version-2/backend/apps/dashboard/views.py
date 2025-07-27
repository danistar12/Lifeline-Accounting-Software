from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncMonth, TruncDay
from datetime import datetime, timedelta
from decimal import Decimal

from apps.core.models import Company
from apps.accounts.models import Account, Transaction
from apps.banking.models import BankAccount
from apps.payments.models import Invoice
from apps.payments.models import Bill
from apps.core.permissions import HasCompanyAccess

class BaseDashboardView(APIView):
    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get_company(self, request):
        company_id = request.headers.get('X-Company-ID')
        return Company.objects.get(id=company_id)

    def get_date_range(self, period='month'):
        today = datetime.now()
        if period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        elif period == 'quarter':
            start_date = today - timedelta(days=90)
        elif period == 'year':
            start_date = today - timedelta(days=365)
        else:
            start_date = today - timedelta(days=30)
        return start_date, today

class DashboardOverviewView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        period = request.query_params.get('period', 'month')
        start_date, end_date = self.get_date_range(period)

        # Get key metrics
        invoices = Invoice.objects.filter(company=company, date__range=[start_date, end_date])
        bills = Bill.objects.filter(company=company, date__range=[start_date, end_date])
        
        total_revenue = invoices.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        total_expenses = bills.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        pending_invoices = invoices.filter(status='pending').count()
        pending_bills = bills.filter(status='pending').count()
        
        # Get cash position
        bank_accounts = BankAccount.objects.filter(company=company)
        total_cash = bank_accounts.aggregate(total=Sum('current_balance'))['total'] or Decimal('0')

        return Response({
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': total_revenue - total_expenses,
            'cash_position': total_cash,
            'pending_invoices': pending_invoices,
            'pending_bills': pending_bills,
            'period': period
        })

class RevenueView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')

        revenue_data = (
            Invoice.objects
            .filter(company=company, date__range=[start_date, end_date])
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(
                total=Sum('total_amount'),
                count=Count('id')
            )
            .order_by('month')
        )

        return Response(revenue_data)

class ExpensesView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        categories = request.query_params.getlist('categories', [])

        query = Bill.objects.filter(company=company, date__range=[start_date, end_date])
        if categories:
            query = query.filter(category__in=categories)

        expenses_data = (
            query
            .annotate(month=TruncMonth('date'))
            .values('month', 'category')
            .annotate(
                total=Sum('total_amount'),
                count=Count('id')
            )
            .order_by('month', 'category')
        )

        return Response(expenses_data)

class RecentTransactionsView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        limit = int(request.query_params.get('limit', 10))
        type_filter = request.query_params.get('type', 'all')

        query = Transaction.objects.filter(company=company)
        if type_filter != 'all':
            query = query.filter(type=type_filter)

        transactions = (
            query
            .select_related('account')
            .order_by('-date')[:limit]
        )

        return Response([{
            'id': t.id,
            'date': t.date,
            'description': t.description,
            'amount': t.amount,
            'type': t.type,
            'account': t.account.name
        } for t in transactions])

class CashFlowView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        period = request.query_params.get('period', 'month')
        include_projection = request.query_params.get('projection', 'true') == 'true'
        
        start_date, end_date = self.get_date_range(period)
        
        # Actual cash flow
        cash_flow = (
            Transaction.objects
            .filter(company=company, date__range=[start_date, end_date])
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(
                inflow=Sum('amount', filter=Q(type='credit')),
                outflow=Sum('amount', filter=Q(type='debit')),
                net=Sum('amount')
            )
            .order_by('day')
        )

        # Add projections if requested
        if include_projection:
            future_inflow = (
                Invoice.objects
                .filter(company=company, due_date__gt=end_date, status='pending')
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
            )
            
            future_outflow = (
                Bill.objects
                .filter(company=company, due_date__gt=end_date, status='pending')
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
            )
            
            projection = {
                'future_inflow': future_inflow,
                'future_outflow': future_outflow,
                'net_projection': future_inflow - future_outflow
            }
            
            return Response({
                'historical': list(cash_flow),
                'projection': projection
            })
            
        return Response(list(cash_flow))

class AccountBalancesView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        account_types = request.query_params.getlist('accountTypes', [])
        
        query = Account.objects.filter(company=company)
        if account_types:
            query = query.filter(type__in=account_types)
            
        balances = query.annotate(
            balance=Sum('transactions__amount')
        ).values('id', 'name', 'type', 'balance')
        
        return Response(balances)

class KeyMetricsView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        period = request.query_params.get('period', 'month')
        start_date, end_date = self.get_date_range(period)

        # Calculate various financial metrics
        metrics = {
            'revenue': self._calculate_revenue(company, start_date, end_date),
            'expenses': self._calculate_expenses(company, start_date, end_date),
            'accounts_receivable': self._calculate_ar(company),
            'accounts_payable': self._calculate_ap(company),
            'cash_position': self._calculate_cash_position(company),
            'quick_ratio': self._calculate_quick_ratio(company)
        }
        
        return Response(metrics)

    def _calculate_revenue(self, company, start_date, end_date):
        return (Invoice.objects
                .filter(company=company, date__range=[start_date, end_date])
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))

    def _calculate_expenses(self, company, start_date, end_date):
        return (Bill.objects
                .filter(company=company, date__range=[start_date, end_date])
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))

    def _calculate_ar(self, company):
        return (Invoice.objects
                .filter(company=company, status='pending')
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))

    def _calculate_ap(self, company):
        return (Bill.objects
                .filter(company=company, status='pending')
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))

    def _calculate_cash_position(self, company):
        return (BankAccount.objects
                .filter(company=company)
                .aggregate(total=Sum('current_balance'))['total'] or Decimal('0'))

    def _calculate_quick_ratio(self, company):
        current_assets = self._calculate_cash_position(company) + self._calculate_ar(company)
        current_liabilities = self._calculate_ap(company)
        return current_assets / current_liabilities if current_liabilities else None

class InvoiceStatusView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        
        status_summary = (
            Invoice.objects
            .filter(company=company)
            .values('status')
            .annotate(
                count=Count('id'),
                total_amount=Sum('total_amount')
            )
        )
        
        aging_summary = self._get_aging_summary(company)
        
        return Response({
            'status_summary': status_summary,
            'aging_summary': aging_summary
        })
    
    def _get_aging_summary(self, company):
        today = datetime.now()
        aging_ranges = {
            'current': (0, 30),
            '31-60': (31, 60),
            '61-90': (61, 90),
            'over_90': (91, None)
        }
        
        aging = {}
        for range_name, (min_days, max_days) in aging_ranges.items():
            query = Q(company=company, status='pending')
            if max_days:
                query &= Q(due_date__gte=today - timedelta(days=max_days))
            query &= Q(due_date__lt=today - timedelta(days=min_days))
            
            amount = (Invoice.objects
                     .filter(query)
                     .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))
            aging[range_name] = amount
            
        return aging

class BudgetComparisonView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        # Get actual expenses by category
        actual_expenses = (
            Bill.objects
            .filter(
                company=company,
                date__year=year,
                date__month=month
            )
            .values('category')
            .annotate(
                actual_amount=Sum('total_amount')
            )
        )
        
        # Compare with budgets (assuming you have a Budget model)
        # This is a placeholder - implement according to your budget model
        budget_comparison = {
            item['category']: {
                'actual': item['actual_amount'],
                'budget': Decimal('0'),  # Replace with actual budget data
                'variance': item['actual_amount'] - Decimal('0')  # Calculate variance
            }
            for item in actual_expenses
        }
        
        return Response(budget_comparison)

class AccountingHealthView(BaseDashboardView):
    def get(self, request):
        company = self.get_company(request)
        
        # Calculate various health metrics
        unreconciled_transactions = Transaction.objects.filter(
            company=company,
            reconciled=False
        ).count()
        
        overdue_invoices = Invoice.objects.filter(
            company=company,
            status='pending',
            due_date__lt=datetime.now()
        ).count()
        
        overdue_bills = Bill.objects.filter(
            company=company,
            status='pending',
            due_date__lt=datetime.now()
        ).count()
        
        # Calculate days sales outstanding (DSO)
        ar = self._calculate_ar(company)
        revenue = self._calculate_revenue(company, datetime.now() - timedelta(days=90), datetime.now())
        dso = (ar / (revenue / 90)) if revenue else 0
        
        return Response({
            'unreconciled_transactions': unreconciled_transactions,
            'overdue_invoices': overdue_invoices,
            'overdue_bills': overdue_bills,
            'days_sales_outstanding': dso,
            'last_reconciliation_date': None,  # Implement based on your reconciliation model
            'missing_documentation': False,  # Implement based on your documentation requirements
            'recommendations': self._get_recommendations(
                unreconciled_transactions,
                overdue_invoices,
                overdue_bills,
                dso
            )
        })
    
    def _calculate_ar(self, company):
        return (Invoice.objects
                .filter(company=company, status='pending')
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))
    
    def _calculate_revenue(self, company, start_date, end_date):
        return (Invoice.objects
                .filter(company=company, date__range=[start_date, end_date])
                .aggregate(total=Sum('total_amount'))['total'] or Decimal('0'))
    
    def _get_recommendations(self, unreconciled, overdue_inv, overdue_bills, dso):
        recommendations = []
        
        if unreconciled > 0:
            recommendations.append({
                'type': 'reconciliation',
                'priority': 'high' if unreconciled > 10 else 'medium',
                'message': f'You have {unreconciled} unreconciled transactions'
            })
            
        if overdue_inv > 0:
            recommendations.append({
                'type': 'collection',
                'priority': 'high' if overdue_inv > 5 else 'medium',
                'message': f'You have {overdue_inv} overdue invoices to collect'
            })
            
        if overdue_bills > 0:
            recommendations.append({
                'type': 'payment',
                'priority': 'high' if overdue_bills > 5 else 'medium',
                'message': f'You have {overdue_bills} overdue bills to pay'
            })
            
        if dso > 45:
            recommendations.append({
                'type': 'dso',
                'priority': 'medium',
                'message': 'Your Days Sales Outstanding is high. Consider reviewing your collection processes'
            })
            
        return recommendations
