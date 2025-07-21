from rest_framework import viewsets, permissions
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Subscription.objects.filter(company_id=company_id)
