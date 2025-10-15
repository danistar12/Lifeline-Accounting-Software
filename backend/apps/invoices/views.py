from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
import traceback

from apps.accounts.models import Company
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.select_related('CompanyID', 'CustomerID')
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['Status', 'CustomerID', 'CompanyID']
    search_fields = ['InvoiceNumber', 'CustomerID__Name']
    ordering_fields = ['InvoiceDate', 'DueDate', 'TotalAmount', 'CreatedDate']
    ordering = ['-CreatedDate']

    def _company_queryset(self):
        return Company.objects.filter(usercompanyrole__UserID=self.request.user)

    def _get_active_company(self):
        companies = self._company_queryset()
        if not companies.exists():
            return None

        query_params = getattr(self.request, 'query_params', {})
        request_data = getattr(self.request, 'data', {})

        company_id = (
            self.request.headers.get('X-Company-ID')
            or query_params.get('CompanyID')
            or request_data.get('CompanyID')
        )

        if company_id:
            try:
                return companies.get(CompanyID=company_id)
            except (Company.DoesNotExist, ValueError):
                raise PermissionDenied("You do not have access to this company.")

        return companies.first()

    def get_queryset(self):
        company = self._get_active_company()
        if not company:
            return Invoice.objects.none()
        return super().get_queryset().filter(CompanyID=company)

    def perform_create(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        serializer.save(CompanyID=company, UserID=self.request.user)

    def perform_update(self, serializer):
        company = self._get_active_company()
        if not company:
            raise PermissionDenied("No company available for this user.")
        serializer.save(CompanyID=company)

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


class InvoiceDebugView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Attempt to evaluate the queryset and serialize first 5 items
            qs = Invoice.objects.all()[:5]
            serializer = InvoiceSerializer(qs, many=True)
            return Response({'ok': True, 'sample': serializer.data})
        except Exception as exc:
            tb = traceback.format_exc()
            return Response({'error': str(exc), 'traceback': tb}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
