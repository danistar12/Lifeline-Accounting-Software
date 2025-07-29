from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Integration
from .serializers import IntegrationSerializer

class IntegrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = IntegrationSerializer
    
    def get_queryset(self):
        return Integration.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
