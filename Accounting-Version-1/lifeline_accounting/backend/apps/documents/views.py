from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Document.objects.filter(company_id=company_id)

    def perform_create(self, serializer):
        company_id = self.request.headers.get('X-Company-ID')
        serializer.save(company_id=company_id, file=self.request.data.get('file'))
