from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'inventory', views.InventoryViewSet, basename='inventory')
router.register(r'inventory-locations', views.InventoryLocationViewSet, basename='inventory-locations')
router.register(r'invoice-line-items', views.InvoiceLineItemViewSet, basename='invoice-line-items')
router.register(r'bill-line-items', views.BillLineItemViewSet, basename='bill-line-items')

urlpatterns = [
    path('', include(router.urls)),
]
