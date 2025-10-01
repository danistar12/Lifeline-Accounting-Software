from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImportFileViewSet

router = DefaultRouter()
router.register(r'import-files', ImportFileViewSet, basename='importfile')

urlpatterns = [
    path('', include(router.urls)),
]
