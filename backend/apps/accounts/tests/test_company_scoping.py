from datetime import date
from decimal import Decimal
from typing import Any, Callable, cast

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from apps.accounts.models import Company, User, UserCompanyRole
from apps.customers.models import Customer
from apps.invoices.models import Invoice
from apps.vendors.models import Vendor


TEST_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


@override_settings(DATABASES=TEST_DATABASES)
class CompanyScopedEndpointTests(APITestCase):
    """Regression-focused tests that exercise company-scoped API endpoints."""

    def setUp(self):  # noqa: D401
        """Create a user with a single company membership and sample data."""
        self.user = User.objects.create_user(
            username="owner",
            password="pass1234",
            email="owner@example.com",
        )
        self.company = Company.objects.create(CompanyName="Acme LLC")
        self.other_company = Company.objects.create(CompanyName="Beta LLC")
        UserCompanyRole.objects.create(UserID=self.user, CompanyID=self.company, Role="owner")

        # Seed customers and vendors for both companies
        self.customer = Customer.objects.create(CompanyID=self.company, Name="Acme Customer")
        self.other_customer = Customer.objects.create(CompanyID=self.other_company, Name="Beta Customer")

        self.vendor = Vendor.objects.create(CompanyID=self.company, Name="Acme Vendor")
        self.other_vendor = Vendor.objects.create(CompanyID=self.other_company, Name="Beta Vendor")

        self.invoice = Invoice.objects.create(
            CompanyID=self.company,
            CustomerID=self.customer,
            InvoiceNumber="INV-1000",
            InvoiceDate=date(2024, 1, 1),
            DueDate=date(2024, 1, 31),
            TotalAmount=Decimal("123.45"),
            Status="Sent",
            UserID=self.user,
        )
        self.other_invoice = Invoice.objects.create(
            CompanyID=self.other_company,
            CustomerID=self.other_customer,
            InvoiceNumber="INV-2000",
            InvoiceDate=date(2024, 2, 1),
            DueDate=date(2024, 2, 29),
            TotalAmount=Decimal("250.00"),
            Status="Sent",
            UserID=self.user,
        )

        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

    def _request(self, method: str, url_name: str, company: Company | None, **kwargs: Any) -> Response:
        if company is not None:
            self.api_client.credentials(HTTP_X_COMPANY_ID=str(company.CompanyID))
        else:
            self.api_client.credentials()

        requester: Callable[..., Any] = getattr(self.api_client, method)
        response = requester(reverse(url_name), **kwargs)
        self.api_client.credentials()
        return cast(Response, response)

    def test_vendor_list_is_scoped_to_authenticated_company(self):
        """The vendor list should only return vendors for the active company."""
        response = self._request("get", "vendor-list", self.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        vendor_ids = {vendor["VendorID"] for vendor in payload}
        self.assertIn(self.vendor.VendorID, vendor_ids)
        self.assertNotIn(self.other_vendor.VendorID, vendor_ids)

    def test_vendor_list_rejects_unowned_company(self):
        """Requesting a company the user is not assigned to should be rejected."""
        response = self._request("get", "vendor-list", self.other_company)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vendor_create_assigns_company_from_header(self):
        """Posting a vendor should attach the active company automatically."""
        payload = {
            "Name": "New Vendor",
            "Email": "vendor@example.com",
            "Phone": "555-0100",
        }
        response = self._request("post", "vendor-list", self.company, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(int(body["CompanyID"]), self.company.CompanyID)

    def test_customer_list_is_scoped_to_authenticated_company(self):
        """Customer endpoint should respect the active company context."""
        response = self._request("get", "customer-list", self.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        customer_ids = {customer["CustomerID"] for customer in payload}
        self.assertIn(self.customer.CustomerID, customer_ids)
        self.assertNotIn(self.other_customer.CustomerID, customer_ids)

    def test_customer_list_rejects_unowned_company(self):
        """Listing customers for an unauthorized company should fail."""
        response = self._request("get", "customer-list", self.other_company)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_create_assigns_company_from_header(self):
        """Customers created via the API should use the active company."""
        payload = {
            "Name": "New Customer",
            "Email": "customer@example.com",
            "Phone": "555-0200",
        }
        response = self._request("post", "customer-list", self.company, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(int(body["CompanyID"]), self.company.CompanyID)

    def test_invoice_list_is_scoped_to_authenticated_company(self):
        """Invoices should only include data for the authenticated company."""
        response = self._request("get", "invoice-list", self.company)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        invoice_ids = {invoice["InvoiceID"] for invoice in payload}
        self.assertIn(self.invoice.InvoiceID, invoice_ids)
        self.assertNotIn(self.other_invoice.InvoiceID, invoice_ids)

    def test_invoice_list_rejects_unowned_company(self):
        """An unauthorized company context should be denied for invoices."""
        response = self._request("get", "invoice-list", self.other_company)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
