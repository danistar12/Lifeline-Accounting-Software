from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardMetricViewSet

router = DefaultRouter()
router.register(r'metrics', DashboardMetricViewSet, basename='dashboard-metrics')

urlpatterns = [
    path('', include(router.urls)),
]
