from django.shortcuts import render
from rest_framework import viewsets, parsers
from .models import Document
from .serializers import DocumentSerializer
from apps.core.permissions import HasCompanyRole

class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows documents to be viewed or uploaded.
    """
    serializer_class = DocumentSerializer
    permission_classes = [HasCompanyRole]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    allowed_roles = ['Admin', 'Accountant', 'Customer']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Document.objects.filter(company_id=company_id)

    def perform_create(self, serializer):
        company_id = self.request.headers.get('X-Company-ID')
        serializer.save(company_id=company_id, uploaded_by=self.request.user)
