from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APPaymentViewSet

router = DefaultRouter()
router.register(r'ap-payments', APPaymentViewSet, basename='ap-payments')

urlpatterns = [
    path('', include(router.urls)),
]
