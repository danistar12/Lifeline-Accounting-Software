from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserCompanyRoleViewSet, ChartOfAccountsViewSet, GeneralLedgerViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', UserCompanyRoleViewSet, basename='usercompanyrole')
router.register(r'chart-of-accounts', ChartOfAccountsViewSet, basename='chartofaccounts')
router.register(r'ledger', GeneralLedgerViewSet, basename='generalledger')

urlpatterns = [
    path('', include(router.urls)),
]
