from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_queryset(self):
        """
        Filter vendors by user's companies
        """
        user = self.request.user
        return Vendor.objects.filter(CompanyID__usercompanyrole__UserID=user)
