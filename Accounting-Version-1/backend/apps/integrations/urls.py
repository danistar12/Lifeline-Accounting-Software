from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'integrations', views.IntegrationViewSet, basename='integrations')

urlpatterns = [
    path('', include(router.urls)),
]
