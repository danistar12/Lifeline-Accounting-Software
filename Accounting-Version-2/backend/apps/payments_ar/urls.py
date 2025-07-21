from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, InvoiceViewSet, InvoicePaymentViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-payments', InvoicePaymentViewSet, basename='invoicepayment')

urlpatterns = [
    path('', include(router.urls)),
]
