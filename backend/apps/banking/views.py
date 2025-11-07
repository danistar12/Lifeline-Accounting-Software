from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework import permissions, viewsets

from .models import BankAccount, BankStatementLine, ReconciliationEntry
from .serializers import (
    BankAccountSerializer,
    BankStatementLineSerializer,
    ReconciliationEntrySerializer,
)


def _clean_company_id(raw_value):
    if raw_value is None:
        return None
    text = str(raw_value).strip()
    if text.lower() in {'', 'none', 'null', 'undefined'}:
        return None
    try:
        company_id = int(text)
    except (TypeError, ValueError):
        return None
    return company_id if company_id > 0 else None


class CompanyScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _allowed_company_ids(self):
        return list(self.request.user.companies.values_list('CompanyID', flat=True))

    def _active_company_id(self):
        header_value = self.request.headers.get('X-Company-ID')
        query_value = self.request.query_params.get('company') or self.request.query_params.get('company_id')
        body_value = None
        if hasattr(self.request, 'data') and isinstance(self.request.data, dict):
            body_value = self.request.data.get('CompanyID')
        for raw in (header_value, query_value, body_value):
            company_id = _clean_company_id(raw)
            if company_id:
                return company_id
        return None


class BankAccountViewSet(CompanyScopedViewSet):
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        allowed_company_ids = self._allowed_company_ids()
        if not allowed_company_ids:
            return BankAccount.objects.none()

        active_company_id = self._active_company_id()
        if active_company_id and active_company_id not in allowed_company_ids:
            return BankAccount.objects.none()

        queryset = (
            BankAccount.objects.filter(CompanyID__in=allowed_company_ids)
            .select_related('CompanyID')
        )

        if active_company_id:
            queryset = queryset.filter(CompanyID=active_company_id)

        queryset = queryset.exclude(BankName__isnull=True).exclude(BankName__exact='')
        queryset = queryset.exclude(
            Q(BankName__iexact='account')
            & (Q(AccountNumber__isnull=True) | Q(AccountNumber__exact=''))
            & (Q(Balance__isnull=True) | Q(Balance=0))
        )

        return queryset.order_by('BankName', 'BankAccountID')


class BankStatementLineViewSet(CompanyScopedViewSet):
    serializer_class = BankStatementLineSerializer

    def get_queryset(self):
        allowed_company_ids = self._allowed_company_ids()
        if not allowed_company_ids:
            return BankStatementLine.objects.none()

        active_company_id = self._active_company_id()
        if active_company_id and active_company_id not in allowed_company_ids:
            return BankStatementLine.objects.none()

        queryset = BankStatementLine.objects.select_related('BankAccountID')
        queryset = queryset.filter(
            BankAccountID__CompanyID__in=allowed_company_ids,
            IsImported=True,
        )

        if active_company_id:
            queryset = queryset.filter(BankAccountID__CompanyID=active_company_id)

        account_filter = _clean_company_id(self.request.query_params.get('account'))
        if account_filter:
            queryset = queryset.filter(BankAccountID=account_filter)

        since_date = self.request.query_params.get('since_date')
        parsed_date = parse_date(since_date) if since_date else None
        if parsed_date:
            queryset = queryset.filter(TransactionDate__date__gte=parsed_date)

        queryset = queryset.exclude(Description__isnull=True).exclude(Description__exact='')

        return queryset.order_by('-TransactionDate', '-BankStatementLineID')


class ReconciliationEntryViewSet(CompanyScopedViewSet):
    serializer_class = ReconciliationEntrySerializer

    def get_queryset(self):
        allowed_company_ids = self._allowed_company_ids()
        if not allowed_company_ids:
            return ReconciliationEntry.objects.none()

        active_company_id = self._active_company_id()
        if active_company_id and active_company_id not in allowed_company_ids:
            return ReconciliationEntry.objects.none()

        queryset = (
            ReconciliationEntry.objects.select_related(
                'BankStatementLineID',
                'BankStatementLineID__BankAccountID',
                'GeneralLedgerID',
            )
            .filter(
                BankStatementLineID__BankAccountID__CompanyID__in=allowed_company_ids,
                BankStatementLineID__IsImported=True,
            )
        )

        if active_company_id:
            queryset = queryset.filter(BankStatementLineID__BankAccountID__CompanyID=active_company_id)

        account_filter = _clean_company_id(self.request.query_params.get('account'))
        if account_filter:
            queryset = queryset.filter(BankStatementLineID__BankAccountID=account_filter)

        since_date = self.request.query_params.get('since_date')
        parsed_date = parse_date(since_date) if since_date else None
        if parsed_date:
            queryset = queryset.filter(ReconciledDate__date__gte=parsed_date)

        return queryset.order_by('-ReconciledDate', '-ReconciliationEntryID')
