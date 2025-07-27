from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('overview/', views.DashboardOverviewView.as_view(), name='overview'),
    path('revenue/', views.RevenueView.as_view(), name='revenue'),
    path('expenses/', views.ExpensesView.as_view(), name='expenses'),
    path('transactions/', views.RecentTransactionsView.as_view(), name='transactions'),
    path('cash-flow/', views.CashFlowView.as_view(), name='cash-flow'),
    path('account-balances/', views.AccountBalancesView.as_view(), name='account-balances'),
    path('key-metrics/', views.KeyMetricsView.as_view(), name='key-metrics'),
    path('invoice-status/', views.InvoiceStatusView.as_view(), name='invoice-status'),
    path('budget-comparison/', views.BudgetComparisonView.as_view(), name='budget-comparison'),
    path('accounting-health/', views.AccountingHealthView.as_view(), name='accounting-health'),
]
