from django.urls import path
from .views import ProfitLossView, BalanceSheetView, CashFlowView

urlpatterns = [
    path('profit-loss/', ProfitLossView.as_view(), name='profit-loss'),
    path('balance-sheet/', BalanceSheetView.as_view(), name='balance-sheet'),
    path('cash-flow/', CashFlowView.as_view(), name='cash-flow'),
]
