from rest_framework import serializers
from .models import FixedAsset

class FixedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAsset
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company_name'] = instance.company.company_name if instance.company else None
        return representation
