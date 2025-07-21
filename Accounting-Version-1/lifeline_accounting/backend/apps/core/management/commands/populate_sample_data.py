from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random

from apps.accounts.models import Company, User, UserCompanyRole
from apps.core.models import ChartOfAccount, GeneralLedger, Customer, Vendor, Invoice, Bill


class Command(BaseCommand):
    help = 'Populate the database with sample financial data for dashboard testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample financial data...')
        
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'is_active': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created test user: {user.username}')
        
        # Get or create a test company
        company, created = Company.objects.get_or_create(
            company_name='Sample Company Inc.',
            defaults={
                'address': '123 Business St',
                'city': 'Business City',
                'state': 'BC',
                'zip_code': '12345',
                'country': 'USA',
                'phone': '555-123-4567',
                'email': 'info@samplecompany.com'
            }
        )
        if created:
            self.stdout.write(f'Created test company: {company.company_name}')
        
        # Create user-company relationship
        role, created = UserCompanyRole.objects.get_or_create(
            user=user,
            company=company,
            defaults={'role': 'owner'}
        )
        
        # Create Chart of Accounts
        accounts_data = [
            {'code': '1000', 'name': 'Cash', 'type': 'asset'},
            {'code': '1200', 'name': 'Accounts Receivable', 'type': 'asset'},
            {'code': '1500', 'name': 'Equipment', 'type': 'asset'},
            {'code': '2000', 'name': 'Accounts Payable', 'type': 'liability'},
            {'code': '2500', 'name': 'Notes Payable', 'type': 'liability'},
            {'code': '3000', 'name': 'Owner Equity', 'type': 'equity'},
            {'code': '4000', 'name': 'Service Revenue', 'type': 'revenue'},
            {'code': '4100', 'name': 'Product Sales', 'type': 'revenue'},
            {'code': '5000', 'name': 'Office Expenses', 'type': 'expense'},
            {'code': '5100', 'name': 'Marketing Expenses', 'type': 'expense'},
            {'code': '5200', 'name': 'Travel Expenses', 'type': 'expense'},
        ]
        
        accounts = {}
        for acc_data in accounts_data:
            account, created = ChartOfAccount.objects.get_or_create(
                company=company,
                account_code=acc_data['code'],
                defaults={
                    'account_name': acc_data['name'],
                    'account_type': acc_data['type']
                }
            )
            accounts[acc_data['code']] = account
            if created:
                self.stdout.write(f'Created account: {account.account_code} - {account.account_name}')
        
        # Create sample customers
        customers_data = [
            'ABC Corporation',
            'XYZ Industries',
            'Tech Solutions LLC',
            'Global Services Inc.',
            'Innovation Partners'
        ]
        
        customers = []
        for customer_name in customers_data:
            customer, created = Customer.objects.get_or_create(
                company=company,
                customer_name=customer_name
            )
            customers.append(customer)
            if created:
                self.stdout.write(f'Created customer: {customer.customer_name}')
        
        # Create sample vendors
        vendors_data = [
            'Office Supply Co.',
            'Marketing Agency Pro',
            'Travel Services LLC',
            'Equipment Rental Inc.',
            'Professional Services'
        ]
        
        vendors = []
        for vendor_name in vendors_data:
            vendor, created = Vendor.objects.get_or_create(
                company=company,
                vendor_name=vendor_name
            )
            vendors.append(vendor)
            if created:
                self.stdout.write(f'Created vendor: {vendor.vendor_name}')
        
        # Create sample invoices
        for i, customer in enumerate(customers):
            invoice, created = Invoice.objects.get_or_create(
                company=company,
                customer=customer,
                defaults={'invoice_id': 1000 + i}
            )
            if created:
                self.stdout.write(f'Created invoice: {invoice.invoice_id}')
        
        # Create sample bills
        for i, vendor in enumerate(vendors):
            bill, created = Bill.objects.get_or_create(
                company=company,
                vendor=vendor,
                defaults={'bill_id': 2000 + i}
            )
            if created:
                self.stdout.write(f'Created bill: {bill.bill_id}')
        
        # Generate sample transactions for the last 6 months
        today = timezone.now().date()
        start_date = today - timedelta(days=180)
        
        # Revenue transactions
        revenue_accounts = [accounts['4000'], accounts['4100']]
        for _ in range(50):  # 50 revenue transactions
            transaction_date = start_date + timedelta(days=random.randint(0, 180))
            amount = Decimal(str(random.uniform(1000, 15000)))
            
            transaction = GeneralLedger.objects.create(
                company=company,
                account=random.choice(revenue_accounts),
                transaction_date=transaction_date,
                description=f'Service revenue from {random.choice(customers).customer_name}',
                credit_amount=amount,
                debit_amount=Decimal('0.00'),
                user=user
            )
        
        # Expense transactions
        expense_accounts = [accounts['5000'], accounts['5100'], accounts['5200']]
        for _ in range(80):  # 80 expense transactions
            transaction_date = start_date + timedelta(days=random.randint(0, 180))
            amount = Decimal(str(random.uniform(100, 3000)))
            
            transaction = GeneralLedger.objects.create(
                company=company,
                account=random.choice(expense_accounts),
                transaction_date=transaction_date,
                description=f'Business expense - {random.choice(vendors).vendor_name}',
                debit_amount=amount,
                credit_amount=Decimal('0.00'),
                user=user
            )
        
        # Asset transactions (cash, equipment, etc.)
        asset_accounts = [accounts['1000'], accounts['1200'], accounts['1500']]
        for _ in range(30):  # 30 asset transactions
            transaction_date = start_date + timedelta(days=random.randint(0, 180))
            amount = Decimal(str(random.uniform(500, 25000)))
            
            # Random debit or credit for assets
            if random.choice([True, False]):
                debit_amount = amount
                credit_amount = Decimal('0.00')
                description = 'Asset purchase or cash receipt'
            else:
                debit_amount = Decimal('0.00')
                credit_amount = amount
                description = 'Asset sale or cash payment'
            
            transaction = GeneralLedger.objects.create(
                company=company,
                account=random.choice(asset_accounts),
                transaction_date=transaction_date,
                description=description,
                debit_amount=debit_amount,
                credit_amount=credit_amount,
                user=user
            )
        
        # Liability transactions
        liability_accounts = [accounts['2000'], accounts['2500']]
        for _ in range(20):  # 20 liability transactions
            transaction_date = start_date + timedelta(days=random.randint(0, 180))
            amount = Decimal(str(random.uniform(500, 10000)))
            
            # Random debit or credit for liabilities
            if random.choice([True, False]):
                debit_amount = amount
                credit_amount = Decimal('0.00')
                description = 'Liability payment'
            else:
                debit_amount = Decimal('0.00')
                credit_amount = amount
                description = 'New liability incurred'
            
            transaction = GeneralLedger.objects.create(
                company=company,
                account=random.choice(liability_accounts),
                transaction_date=transaction_date,
                description=description,
                debit_amount=debit_amount,
                credit_amount=credit_amount,
                user=user
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data!\n'
                f'- User: {user.username}\n'
                f'- Company: {company.company_name}\n'
                f'- Accounts: {len(accounts)}\n'
                f'- Customers: {len(customers)}\n'
                f'- Vendors: {len(vendors)}\n'
                f'- Transactions: {GeneralLedger.objects.filter(company=company).count()}\n\n'
                f'You can now login with:\n'
                f'Username: testuser\n'
                f'Password: testpass123'
            )
        )
