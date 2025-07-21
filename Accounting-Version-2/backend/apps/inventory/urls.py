from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryCategoryViewSet, InventoryItemViewSet

router = DefaultRouter()
router.register(r'categories', InventoryCategoryViewSet, basename='inventorycategory')
router.register(r'items', InventoryItemViewSet, basename='inventoryitem')

urlpatterns = [
    path('', include(router.urls)),
]
