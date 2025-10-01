# populate_fake_data.py
"""
Populate the database with one fake record for each main model.
Run with: python manage.py shell < populate_fake_data.py
"""
from django.utils import timezone
from decimal import Decimal

from apps.accounts.models import User, Company, UserCompanyRole
from apps.banking.models import BankAccount, BankTransaction
from apps.payroll.models import Employee, Payroll, PayrollDeduction, TimeEntry as PayrollTimeEntry
from apps.subscriptions.models import Subscription
from apps.taxes.models import TaxRate, TaxTransaction
from apps.inventory.models import Inventory, InventoryLocation, InvoiceLineItem, BillLineItem
from apps.payments.models import Payment
from apps.projects.models import Project
from apps.customers.models import Customer
from apps.vendors.models import Vendor
from apps.invoices.models import Invoice
from apps.bills.models import Bill
from apps.documents.models import Document

# --- ACCOUNTS ---
user, _ = User.objects.get_or_create(username='testuser', defaults={
    'email': 'testuser@example.com',
    'password': 'pbkdf2_sha256$260000$dummy$dummy',
})
company, _ = Company.objects.get_or_create(CompanyName='Test Company', defaults={
    'AdminUserID': user,
})
UserCompanyRole.objects.get_or_create(UserID=user, CompanyID=company, defaults={'Role': 'Admin'})

# Add the user 'dlloyd' as a real user and admin
dlloyd, _ = User.objects.get_or_create(username='dlloyd', defaults={
    'email': 'dlloyd@example.com',
    'password': 'pbkdf2_sha256$260000$dummy$dummy',
    'is_superuser': True,
    'is_staff': True,
})
company2, _ = Company.objects.get_or_create(CompanyName='Lifeline Accounting', defaults={
    'AdminUserID': dlloyd,
})
UserCompanyRole.objects.get_or_create(UserID=dlloyd, CompanyID=company2, defaults={'Role': 'Admin'})

# --- CUSTOMERS ---
customer, _ = Customer.objects.get_or_create(CompanyID=company, Name='Test Customer')

# --- VENDORS ---
vendor, _ = Vendor.objects.get_or_create(CompanyID=company, Name='Test Vendor')

# --- INVOICES ---
invoice, _ = Invoice.objects.get_or_create(CompanyID=company, CustomerID=customer, InvoiceNumber='INV-001', defaults={
    'InvoiceDate': timezone.now().date(),
    'DueDate': timezone.now().date(),
    'TotalAmount': Decimal('100.00'),
    'Status': 'Open',
})

# --- BILLS ---
bill, _ = Bill.objects.get_or_create(CompanyID=company, VendorID=vendor, BillNumber='BILL-001', defaults={
    'BillDate': timezone.now().date(),
    'DueDate': timezone.now().date(),
    'TotalAmount': Decimal('50.00'),
    'Status': 'Unpaid',
})

# --- BANKING ---
bank_account, _ = BankAccount.objects.get_or_create(CompanyID=company, AccountNumber='123456', defaults={
    'BankName': 'Test Bank',
    'AccountType': 'Checking',
    'Balance': Decimal('1000.00'),
})
BankTransaction.objects.get_or_create(BankAccountID=bank_account, TransactionDate=timezone.now(), defaults={
    'Description': 'Initial Deposit',
    'Amount': Decimal('1000.00'),
    'TransactionType': 'Deposit',
})

# --- PAYROLL ---
# --- PROJECTS ---
project, _ = Project.objects.get_or_create(CompanyID=company, ProjectName='Test Project', defaults={
    'Status': 'Active',
})

# --- PAYROLL ---
employee, _ = Employee.objects.get_or_create(CompanyID=company, Name='Test Employee')
payroll, _ = Payroll.objects.get_or_create(EmployeeID=employee, PayPeriodStart=timezone.now().date(), PayPeriodEnd=timezone.now().date(), defaults={
    'GrossPay': Decimal('2000.00'),
    'NetPay': Decimal('1800.00'),
    'TaxesWithheld': Decimal('200.00'),
    'PaymentDate': timezone.now().date(),
})
PayrollDeduction.objects.get_or_create(PayrollID=payroll, EmployeeID=employee, DeductionType='Tax', defaults={
    'Amount': Decimal('100.00'),
})
PayrollTimeEntry.objects.get_or_create(ProjectID=project, EmployeeID=employee, WorkDate=timezone.now().date(), defaults={
    'Hours': Decimal('8.0'),
})

# --- SUBSCRIPTIONS ---
subscription, _ = Subscription.objects.get_or_create(CompanyID=company, CustomerID=customer, PlanName='Basic', defaults={
    'BillingCycle': 'Monthly',
    'RenewalDate': timezone.now().date(),
})

# --- TAXES ---
tax_rate, _ = TaxRate.objects.get_or_create(CompanyID=company, TaxName='VAT', defaults={
    'Rate': Decimal('0.1000'),
    'EffectiveDate': timezone.now().date(),
})
TaxTransaction.objects.get_or_create(CompanyID=company, TaxRateID=tax_rate, TaxAmount=Decimal('10.00'), TransactionDate=timezone.now(), defaults={})

# --- INVENTORY ---
location, _ = InventoryLocation.objects.get_or_create(CompanyID=company, LocationName='Main Warehouse')
inventory, _ = Inventory.objects.get_or_create(CompanyID=company, ProductCode='SKU-001', defaults={
    'ProductName': 'Test Product',
    'Quantity': Decimal('10.0'),
    'UnitPrice': Decimal('5.00'),
    'LocationID': location,
})
InvoiceLineItem.objects.get_or_create(InvoiceID=invoice, InventoryID=inventory, Description='Test Item', defaults={
    'Quantity': Decimal('2.0'),
    'UnitPrice': Decimal('5.00'),
    'TotalAmount': Decimal('10.00'),
})
BillLineItem.objects.get_or_create(BillID=bill, InventoryID=inventory, Description='Test Item', defaults={
    'Quantity': Decimal('1.0'),
    'UnitPrice': Decimal('5.00'),
    'TotalAmount': Decimal('5.00'),
})

# --- PAYMENTS ---
from apps.accounting.models import ChartOfAccount
account, _ = ChartOfAccount.objects.get_or_create(CompanyID=company, AccountName='Cash', defaults={'AccountType': 'Asset'})
Payment.objects.get_or_create(CompanyID=company, PaymentType='AR', CustomerID=customer, PaymentDate=timezone.now().date(), Amount=Decimal('100.00'), AccountID=account)

# --- PROJECTS ---
project, _ = Project.objects.get_or_create(CompanyID=company, ProjectName='Test Project', defaults={
    'Status': 'Active',
})

# --- DOCUMENTS ---
Document.objects.get_or_create(CompanyID=company, FilePath='/tmp/test.pdf', FileName='test.pdf')

print('Fake data populated!')
