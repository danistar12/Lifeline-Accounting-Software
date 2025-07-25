from django.urls import path
from .views import (
    ProfitLossView, BalanceSheetView, CashFlowView,
    PayrollSummaryView, EmployeeListView, FinancialDashboardView,
    BankingReportView
)

urlpatterns = [
    path('profit-loss/', ProfitLossView.as_view(), name='profit-loss'),
    path('balance-sheet/', BalanceSheetView.as_view(), name='balance-sheet'),
    path('cash-flow/', CashFlowView.as_view(), name='cash-flow'),
    path('payroll-summary/', PayrollSummaryView.as_view(), name='payroll-summary'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('dashboard/', FinancialDashboardView.as_view(), name='financial-dashboard'),
    path('banking/', BankingReportView.as_view(), name='banking-report'),
]
