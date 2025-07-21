from django.shortcuts import render
from rest_framework import viewsets

from .models import Subscription
from .serializers import SubscriptionSerializer
from apps.core.permissions import HasCompanyRole

# Create your views here.

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Subscription.objects.filter(company_id=company_id)

    def perform_create(self, serializer):
        company_id = self.request.headers.get('X-Company-ID')
        serializer.save(company_id=company_id)
