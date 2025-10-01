from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChartOfAccountViewSet, GeneralLedgerViewSet

router = DefaultRouter()
router.register(r'chart-of-accounts', ChartOfAccountViewSet)
router.register(r'general-ledger', GeneralLedgerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]