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
    
    UserID = UserMinSerializer(read_only=True)
    ContentType = ContentTypeSerializer(read_only=True)
    model_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'AuditID', 'UserID', 'CompanyID', 'ActionType', 'ActionDescription',
            'ActionDate', 'ContentType', 'ObjectID', 'IPAddress',
            'model_name', 'user_name'
        ]
    
    def get_model_name(self, obj):
        """Get the human-readable model name."""
        if obj.ContentType:
            return obj.ContentType.model.replace('_', ' ').title()
        return None
    
    def get_user_name(self, obj):
        """Get the full name of the user."""
        if obj.UserID:
            if obj.UserID.first_name or obj.UserID.last_name:
                return f"{obj.UserID.first_name} {obj.UserID.last_name}".strip()
            return obj.UserID.username
        return "System"


class AuditLogDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for a single audit log."""
    
    UserID = UserMinSerializer(read_only=True)
    ContentType = ContentTypeSerializer(read_only=True)
    model_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    changes = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'AuditID', 'UserID', 'user_name', 'CompanyID', 'ActionType', 
            'ActionDescription', 'ActionDate', 'ContentType', 
            'ObjectID', 'DataBefore', 'DataAfter', 'Details', 
            'IPAddress', 'UserAgent', 'model_name', 'changes'
        ]
    
    def get_model_name(self, obj):
        """Get the human-readable model name."""
        if obj.ContentType:
            return obj.ContentType.model.replace('_', ' ').title()
        return None
    
    def get_user_name(self, obj):
        """Get the full name of the user."""
        if obj.UserID:
            if obj.UserID.first_name or obj.UserID.last_name:
                return f"{obj.UserID.first_name} {obj.UserID.last_name}".strip()
            return obj.UserID.username
        return "System"
    
    def get_changes(self, obj):
        """
        Format the changes for display.
        Returns a list of dictionaries with field, before, and after values.
        """
        changes = []
        
        if not obj.DataBefore or not obj.DataAfter:
            return changes
            
        # Find all keys that are in either DataBefore or DataAfter
        all_keys = set(obj.DataBefore.keys()) | set(obj.DataAfter.keys())
        
        for key in all_keys:
            before_value = obj.DataBefore.get(key, None)
            after_value = obj.DataAfter.get(key, None)
            
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
