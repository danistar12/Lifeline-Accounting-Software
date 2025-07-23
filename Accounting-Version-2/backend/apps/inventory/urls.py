from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryLocationViewSet, InventoryViewSet

router = DefaultRouter()
router.register(r'locations', InventoryLocationViewSet, basename='inventorylocation')
router.register(r'items', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]
