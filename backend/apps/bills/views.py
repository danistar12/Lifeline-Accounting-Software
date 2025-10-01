from rest_framework import viewsets
from .models import Bill
from .serializers import BillSerializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    def get_queryset(self):
        """
        Filter bills by user's companies
        """
        user = self.request.user
        return Bill.objects.filter(CompanyID__usercompanyrole__UserID=user)

    def perform_create(self, serializer):
        """
        Set the user when creating a bill
        """
        serializer.save(UserID=self.request.user)
