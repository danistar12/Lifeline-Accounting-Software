from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Placeholder for Accounts Receivable specific endpoints
router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]