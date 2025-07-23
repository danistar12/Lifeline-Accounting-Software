from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExchangeRateViewSet, FixedAssetViewSet, BudgetViewSet

router = DefaultRouter()
router.register(r'exchange-rates', ExchangeRateViewSet)
router.register(r'fixed-assets', FixedAssetViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
