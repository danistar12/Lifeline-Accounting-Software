from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')
router.register(r'time-entries', views.TimeEntryViewSet, basename='time-entries')

urlpatterns = [
    path('', include(router.urls)),
]
