from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet, BankStatementLineViewSet, ReconciliationEntryViewSet

router = DefaultRouter()
router.register(r'accounts', BankAccountViewSet, basename='bank-accounts')
router.register(r'statement-lines', BankStatementLineViewSet, basename='bank-statement-lines')
router.register(r'reconciliations', ReconciliationEntryViewSet, basename='reconciliations')

urlpatterns = [
    path('', include(router.urls)),
]
