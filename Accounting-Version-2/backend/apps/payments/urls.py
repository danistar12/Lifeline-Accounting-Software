from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Register your viewsets here
# Example: router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]
