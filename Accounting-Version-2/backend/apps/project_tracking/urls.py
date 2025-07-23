from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TimeEntryViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'time-entries', TimeEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
