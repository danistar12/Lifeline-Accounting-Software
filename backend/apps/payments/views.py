from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """
        Filter payments by user's companies
        """
        user = self.request.user
        return Payment.objects.filter(CompanyID__usercompanyrole__UserID=user)

    def perform_create(self, serializer):
        """
        Set the user when creating a payment
        """
        serializer.save(UserID=self.request.user)
