from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, ChartOfAccountsViewSet, GeneralLedgerViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'chart-of-accounts', ChartOfAccountsViewSet, basename='chart-of-accounts')
router.register(r'general-ledger', GeneralLedgerViewSet, basename='general-ledger')

urlpatterns = [
    path('', include(router.urls)),
]
