from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tax-rates', views.TaxRateViewSet, basename='tax-rates')
router.register(r'tax-transactions', views.TaxTransactionViewSet, basename='tax-transactions')

urlpatterns = [
    path('', include(router.urls)),
]
