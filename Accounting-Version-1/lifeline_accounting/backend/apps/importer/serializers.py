from rest_framework import serializers
from .models import ImportFile

class ImportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportFile
        fields = ['id', 'company', 'file_type', 'file', 'uploaded_at', 'status']
        read_only_fields = ['uploaded_at', 'status']
