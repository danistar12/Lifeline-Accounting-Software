from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomFieldViewSet, CustomFieldValueViewSet

router = DefaultRouter()
router.register(r'custom-fields', CustomFieldViewSet)
router.register(r'custom-field-values', CustomFieldValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
