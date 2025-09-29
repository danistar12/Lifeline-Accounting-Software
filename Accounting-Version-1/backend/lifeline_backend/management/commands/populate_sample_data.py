
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import date

from apps.accounts.models import User, Company, UserCompanyRole
from apps.accounting.models import ChartOfAccount, GeneralLedger
from apps.customers.models import Customer
from apps.vendors.models import Vendor
from apps.invoices.models import Invoice
from apps.bills.models import Bill
from apps.payments.models import Payment
from apps.inventory.models import Inventory, InventoryLocation, InvoiceLineItem, BillLineItem
from apps.payroll.models import Employee, Payroll, PayrollDeduction, TimeEntry
from apps.subscriptions.models import Subscription
from apps.banking.models import BankAccount

class Command(BaseCommand):
    help = 'Populate database with minimal sample data for testing'

    def handle(self, *args, **options):
        # Clear all data
        self.stdout.write('Clearing all data...')
        TimeEntry.objects.all().delete()
        PayrollDeduction.objects.all().delete()
        Payroll.objects.all().delete()
        Employee.objects.all().delete()
        InvoiceLineItem.objects.all().delete()
        BillLineItem.objects.all().delete()
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        Bill.objects.all().delete()
        Subscription.objects.all().delete()
        GeneralLedger.objects.all().delete()
        ChartOfAccount.objects.all().delete()
        Customer.objects.all().delete()
        Vendor.objects.all().delete()
        Inventory.objects.all().delete()
        InventoryLocation.objects.all().delete()
        UserCompanyRole.objects.all().delete()
        Company.objects.all().delete()
        BankAccount.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create minimal user
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            UserNotes='Minimal test user.'
        )

        # Create minimal company
        company = Company.objects.create(
            CompanyName='Test Company',
            CompanyNotes='Minimal test company.',
            AdminUserID=user
        )

        # Assign user to company
        UserCompanyRole.objects.create(
            UserID=user,
            CompanyID=company,
            Role='Admin'
        )

        # Create minimal customer
        customer = Customer.objects.create(
            CompanyID=company,
            Name='Test Customer',
            Email='customer@example.com',
            Phone='555-1234',
            Address='123 Test St',
            PaymentTerms='Net 30',
            CustomerNotes='Minimal test customer.'
        )

        # Create minimal vendor
        vendor = Vendor.objects.create(
            CompanyID=company,
            Name='Test Vendor',
            Email='vendor@example.com',
            Phone='555-5678',
            Address='456 Vendor Ave',
            PaymentTerms='Net 30',
            VendorNotes='Minimal test vendor.'
        )

        # Create minimal inventory location
        location = InventoryLocation.objects.create(
            CompanyID=company,
            LocationName='Main Warehouse'
        )

        # Create minimal inventory item
        inventory = Inventory.objects.create(
            CompanyID=company,
            ProductCode='PROD1000',
            ProductName='Test Product',
            Quantity=Decimal('100'),
            UnitPrice=Decimal('10.00'),
            CostPrice=Decimal('8.00'),
            InventoryNotes='Minimal test inventory.',
            ValuationMethod='FIFO',
            LocationID=location
        )

        # Create minimal chart of account (including cash account)
        cash_account = ChartOfAccount.objects.create(
            CompanyID=company,
            AccountCode='1000',
            AccountName='Cash',
            AccountType='CURRENT_ASSET',
            AccountNotes='Cash account for testing.',
            IsActive=True
        )
        revenue_account = ChartOfAccount.objects.create(
            CompanyID=company,
            AccountCode='4000',
            AccountName='Sales Revenue',
            AccountType='REVENUE',
            AccountNotes='Revenue account for testing.',
            IsActive=True
        )
        expense_account = ChartOfAccount.objects.create(
            CompanyID=company,
            AccountCode='5000',
            AccountName='Office Supplies',
            AccountType='EXPENSE',
            AccountNotes='Expense account for testing.',
            IsActive=True
        )

        # Create minimal general ledger entries
        GeneralLedger.objects.create(
            CompanyID=company,
            AccountID=cash_account,
            TransactionDate=date.today(),
            Description='Initial cash deposit',
            DebitAmount=Decimal('1000.00'),
            CreditAmount=Decimal('0.00'),
            GLNotes='Initial deposit.',
            CurrencyCode='USD',
            ExchangeRate=Decimal('1.000000'),
            UserID=user
        )
        GeneralLedger.objects.create(
            CompanyID=company,
            AccountID=revenue_account,
            TransactionDate=date.today(),
            Description='Product sale',
            DebitAmount=Decimal('0.00'),
            CreditAmount=Decimal('500.00'),
            GLNotes='Sale of product.',
            CurrencyCode='USD',
            ExchangeRate=Decimal('1.000000'),
            UserID=user
        )
        GeneralLedger.objects.create(
            CompanyID=company,
            AccountID=expense_account,
            TransactionDate=date.today(),
            Description='Office supplies purchase',
            DebitAmount=Decimal('50.00'),
            CreditAmount=Decimal('0.00'),
            GLNotes='Bought office supplies.',
            CurrencyCode='USD',
            ExchangeRate=Decimal('1.000000'),
            UserID=user
        )

        # Create minimal invoice
        invoice = Invoice.objects.create(
            CompanyID=company,
            CustomerID=customer,
            InvoiceNumber='INV-10001',
            InvoiceDate=date.today(),
            DueDate=date.today(),
            TotalAmount=Decimal('500.00'),
            Status='Sent',
            InvoiceNotes='Minimal test invoice.',
            CurrencyCode='USD',
            UserID=user
        )

        # Create minimal invoice line item
        InvoiceLineItem.objects.create(
            InvoiceID=invoice,
            InventoryID=inventory,
            Description='Test product sale',
            Quantity=Decimal('50'),
            UnitPrice=Decimal('10.00'),
            TotalAmount=Decimal('500.00')
        )

        # Create minimal bill
        bill = Bill.objects.create(
            CompanyID=company,
            VendorID=vendor,
            BillNumber='BILL-10001',
            BillDate=date.today(),
            DueDate=date.today(),
            TotalAmount=Decimal('50.00'),
            Status='Sent',
            BillNotes='Minimal test bill.',
            CurrencyCode='USD',
            UserID=user
        )

        # Create minimal bill line item
        BillLineItem.objects.create(
            BillID=bill,
            InventoryID=inventory,
            Description='Office supplies',
            Quantity=Decimal('5'),
            UnitPrice=Decimal('10.00'),
            TotalAmount=Decimal('50.00')
        )

        # Create minimal payment for invoice
        Payment.objects.create(
            CompanyID=company,
            InvoiceID=invoice,
            PaymentDate=date.today(),
            Amount=Decimal('500.00'),
            PaymentMethod='Cash',
            PaymentNotes='Minimal test payment.',
            CurrencyCode='USD',
            UserID=user
        )

        # Create minimal payment for bill
        Payment.objects.create(
            CompanyID=company,
            BillID=bill,
            PaymentDate=date.today(),
            Amount=Decimal('50.00'),
            PaymentMethod='Cash',
            PaymentNotes='Minimal test payment.',
            CurrencyCode='USD',
            UserID=user
        )

        # Create minimal bank account
        bank_account = BankAccount.objects.create(
            CompanyID=company,
            AccountNumber='123456789',
            BankName='Test Bank',
            AccountType='Checking',
            BankAcctNotes='Minimal test bank account.',
            CurrencyCode='USD',
            Balance=Decimal('1000.00')
        )

        # Create minimal employee
        employee = Employee.objects.create(
            CompanyID=company,
            Name='Test Employee',
            Email='employee@example.com',
            HourlyRate=Decimal('20.00'),
            TaxWithholding=Decimal('5.00'),
            EmployeeNotes='Minimal test employee.'
        )

        # Create minimal payroll
        payroll = Payroll.objects.create(
            EmployeeID=employee,
            PayPeriodStart=date.today(),
            PayPeriodEnd=date.today(),
            GrossPay=Decimal('2000.00'),
            NetPay=Decimal('1500.00'),
            TaxesWithheld=Decimal('500.00'),
            PaymentDate=date.today()
        )

        # Create minimal payroll deduction
        PayrollDeduction.objects.create(
            PayrollID=payroll,
            EmployeeID=employee,
            DeductionType='Health Insurance',
            Amount=Decimal('100.00')
        )

        # Create minimal project
        from apps.projects.models import Project
        project = Project.objects.create(
            CompanyID=company,
            ProjectName='Test Project',
            CustomerID=customer,
            Status='Active'
        )

        # Create minimal time entry
        TimeEntry.objects.create(
            ProjectID=project,
            EmployeeID=employee,
            WorkDate=date.today(),
            Hours=Decimal('8.00'),
            TimeEntryNotes='Minimal test time entry.',
            Billable=True,
            Rate=Decimal('20.00')
        )

        # Create minimal subscription
        Subscription.objects.create(
            CompanyID=company,
            CustomerID=customer,
            PlanName='Basic',
            BillingCycle='Monthly',
            RenewalDate=date.today(),
            Status='Active'
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with minimal sample data!'))