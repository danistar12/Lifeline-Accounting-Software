from rest_framework import serializers
from .models import APPayment

class APPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = APPayment
        fields = '__all__'
