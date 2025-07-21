from django.urls import path
from .views import BalanceSheetView, IncomeStatementView, CashFlowView

urlpatterns = [
    path('balance-sheet/', BalanceSheetView.as_view(), name='balance-sheet'),
    path('income-statement/', IncomeStatementView.as_view(), name='income-statement'),
    path('cash-flow/', CashFlowView.as_view(), name='cash-flow'),
]
