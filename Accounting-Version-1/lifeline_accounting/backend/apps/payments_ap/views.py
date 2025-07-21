from rest_framework import viewsets, permissions
from .models import APPayment
from .serializers import APPaymentSerializer

class APPaymentViewSet(viewsets.ModelViewSet):
    queryset = APPayment.objects.all()
    serializer_class = APPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return APPayment.objects.filter(company_id=company_id)
