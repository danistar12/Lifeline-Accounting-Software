from rest_framework import viewsets
from .models import Customer, Invoice, InvoicePayment
from .serializers import CustomerSerializer, InvoiceSerializer, InvoicePaymentSerializer
from apps.core.permissions import HasCompanyRole

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Sales']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Customer.objects.filter(company_id=company_id)

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant', 'Sales']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Invoice.objects.filter(company_id=company_id)

class InvoicePaymentViewSet(viewsets.ModelViewSet):
    serializer_class = InvoicePaymentSerializer
    permission_classes = [HasCompanyRole]
    allowed_roles = ['Admin', 'Accountant']

    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return InvoicePayment.objects.filter(company_id=company_id)
