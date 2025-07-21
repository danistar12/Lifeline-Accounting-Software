from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet, BankTransactionViewSet, BankReconciliationViewSet

router = DefaultRouter()
router.register(r'accounts', BankAccountViewSet)
router.register(r'transactions', BankTransactionViewSet)
router.register(r'reconciliations', BankReconciliationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
