from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, InventoryLocation, InvoiceLineItem, BillLineItem
from .serializers import InventorySerializer, InventoryLocationSerializer, InvoiceLineItemSerializer, BillLineItemSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InventorySerializer
    
    def get_queryset(self):
        return Inventory.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

class InventoryLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InventoryLocationSerializer
    
    def get_queryset(self):
        return InventoryLocation.objects.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

class InvoiceLineItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceLineItemSerializer
    
    def get_queryset(self):
        return InvoiceLineItem.objects.filter(invoice__company=self.request.user.company)

class BillLineItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BillLineItemSerializer
    
    def get_queryset(self):
        return BillLineItem.objects.filter(bill__company=self.request.user.company)
