from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, TimeEntry
from .serializers import ProjectSerializer, TimeEntrySerializer

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

class TimeEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeEntrySerializer
    
    def get_queryset(self):
        return TimeEntry.objects.filter(project__company=self.request.user.company)
