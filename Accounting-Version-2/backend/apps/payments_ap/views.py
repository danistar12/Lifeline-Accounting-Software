from rest_framework import viewsets
from .models import Vendor, Bill, BillPayment
from .serializers import VendorSerializer, BillSerializer, BillPaymentSerializer
from apps.core.permissions import HasCompanyRole

class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Vendor.objects.filter(company_id=company_id)

class BillViewSet(viewsets.ModelViewSet):
    serializer_class = BillSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Bill.objects.filter(company_id=company_id)

class BillPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = BillPaymentSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return BillPayment.objects.filter(company_id=company_id)
