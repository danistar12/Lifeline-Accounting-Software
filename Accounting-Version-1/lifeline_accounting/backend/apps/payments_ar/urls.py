from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ARPaymentViewSet

router = DefaultRouter()
router.register(r'ar-payments', ARPaymentViewSet, basename='ar-payments')

urlpatterns = [
    path('', include(router.urls)),
]
