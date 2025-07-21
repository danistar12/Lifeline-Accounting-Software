from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog


User = get_user_model()


class UserMinSerializer(serializers.ModelSerializer):
    """Minimal User serializer for audit logs."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ContentTypeSerializer(serializers.ModelSerializer):
    """Serializer for ContentType model."""
    
    class Meta:
        model = ContentType
        fields = ['id', 'app_label', 'model']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for listing audit logs."""
    
    user = UserMinSerializer(read_only=True)
    content_type = ContentTypeSerializer(read_only=True)
    model_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'company', 'action_type', 'action_description',
            'timestamp', 'content_type', 'object_id', 'ip_address',
            'model_name', 'user_name'
        ]
    
    def get_model_name(self, obj):
        """Get the human-readable model name."""
        if obj.content_type:
            return obj.content_type.model.replace('_', ' ').title()
        return None
    
    def get_user_name(self, obj):
        """Get the full name of the user."""
        if obj.user:
            if obj.user.first_name or obj.user.last_name:
                return f"{obj.user.first_name} {obj.user.last_name}".strip()
            return obj.user.username
        return "System"


class AuditLogDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for a single audit log."""
    
    user = UserMinSerializer(read_only=True)
    content_type = ContentTypeSerializer(read_only=True)
    model_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    changes = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_name', 'company', 'action_type', 
            'action_description', 'timestamp', 'content_type', 
            'object_id', 'data_before', 'data_after', 'details', 
            'ip_address', 'user_agent', 'model_name', 'changes'
        ]
    
    def get_model_name(self, obj):
        """Get the human-readable model name."""
        if obj.content_type:
            return obj.content_type.model.replace('_', ' ').title()
        return None
    
    def get_user_name(self, obj):
        """Get the full name of the user."""
        if obj.user:
            if obj.user.first_name or obj.user.last_name:
                return f"{obj.user.first_name} {obj.user.last_name}".strip()
            return obj.user.username
        return "System"
    
    def get_changes(self, obj):
        """
        Format the changes for display.
        Returns a list of dictionaries with field, before, and after values.
        """
        changes = []
        
        if not obj.data_before or not obj.data_after:
            return changes
            
        # Find all keys that are in either data_before or data_after
        all_keys = set(obj.data_before.keys()) | set(obj.data_after.keys())
        
        for key in all_keys:
            before_value = obj.data_before.get(key, None)
            after_value = obj.data_after.get(key, None)
            
            # Only include if there's actually a change
            if before_value != after_value:
                # Format field name for display
                field_name = key.replace('_', ' ').title()
                
                changes.append({
                    'field': field_name,
                    'before': before_value,
                    'after': after_value
                })
                
        return changes
