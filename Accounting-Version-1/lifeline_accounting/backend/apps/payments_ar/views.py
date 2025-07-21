from rest_framework import viewsets, permissions
from .models import ARPayment
from .serializers import ARPaymentSerializer

class ARPaymentViewSet(viewsets.ModelViewSet):
    queryset = ARPayment.objects.all()
    serializer_class = ARPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return ARPayment.objects.filter(company_id=company_id)
