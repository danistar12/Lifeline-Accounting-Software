from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, BillViewSet, BillPaymentViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'bill-payments', BillPaymentViewSet, basename='billpayment')

urlpatterns = [
    path('', include(router.urls)),
]
