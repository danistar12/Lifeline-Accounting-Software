from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
        Filter customers by user's companies
        """
        user = self.request.user
        return Customer.objects.filter(CompanyID__usercompanyrole__UserID=user)
