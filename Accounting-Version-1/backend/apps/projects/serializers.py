from rest_framework import serializers
from .models import Project, TimeEntry

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    time_entries = TimeEntrySerializer(many=True, read_only=True, source='timeentry_set')
    
    class Meta:
        model = Project
        fields = '__all__'
