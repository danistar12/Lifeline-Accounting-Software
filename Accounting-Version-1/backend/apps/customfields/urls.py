from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomFieldViewSet, CustomFieldValueViewSet

router = DefaultRouter()
router.register(r'fields', CustomFieldViewSet)
router.register(r'values', CustomFieldValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]