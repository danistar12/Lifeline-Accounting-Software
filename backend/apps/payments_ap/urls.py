from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Placeholder for Accounts Payable specific endpoints
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]