from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Status', 'CustomerID', 'CompanyID']
    search_fields = ['InvoiceNumber', 'CustomerID__Name']
    ordering_fields = ['InvoiceDate', 'DueDate', 'TotalAmount', 'CreatedDate']
    ordering = ['-CreatedDate']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by user's company if needed
        user = self.request.user
        if hasattr(user, 'company'):
            queryset = queryset.filter(CompanyID=user.company)
        return queryset

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        invoice = self.get_object()
        invoice.Status = 'Paid'
        invoice.save()
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_overdue(self, request, pk=None):
        invoice = self.get_object()
        invoice.Status = 'Overdue'
        invoice.save()
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)
