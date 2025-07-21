from rest_framework import serializers
from .models import ARPayment

class ARPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARPayment
        fields = '__all__'
