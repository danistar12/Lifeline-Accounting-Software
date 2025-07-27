from rest_framework import viewsets
from .models import Customer, Vendor
from .serializers import CustomerSerializer, VendorSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Customer.objects.filter(company_id=company_id)
    
    def perform_create(self, serializer):
        company_id = self.request.headers.get('X-Company-ID')
        serializer.save(company_id=company_id)

class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        return Vendor.objects.filter(company_id=company_id)
        
    def perform_create(self, serializer):
        company_id = self.request.headers.get('X-Company-ID')
        serializer.save(company_id=company_id)
