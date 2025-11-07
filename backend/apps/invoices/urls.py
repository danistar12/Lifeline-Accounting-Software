from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, InvoiceDebugView

router = DefaultRouter()
router.register(r'', InvoiceViewSet, basename='invoices')  # Empty string so it's just /api/invoices/

urlpatterns = [
    path('debug/', InvoiceDebugView.as_view()),
    path('', include(router.urls)),
]