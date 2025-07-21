from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import ImportFile
from .serializers import ImportFileSerializer
from .tasks import process_import_file_task

class ImportFileViewSet(viewsets.ModelViewSet):
    queryset = ImportFile.objects.all()
    serializer_class = ImportFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Limit to companies the user belongs to
        return ImportFile.objects.filter(company__in=self.request.user.companies.all())

    def perform_create(self, serializer):
        # Associate and save with pending status
        import_file = serializer.save(
            company_id=self.request.headers.get('X-Company-ID'),
            status='pending'
        )
        # Enqueue background job
        process_import_file_task.delay(import_file.pk)
