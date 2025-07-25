from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.accounts.models import User, UserCompanyRole
from apps.core.models import Company, ChartOfAccounts
from apps.contacts.models import Customer, Vendor
from apps.banking.models import BankAccount, BankTransaction
from apps.payroll.models import Employee, Payroll
from decimal import Decimal
import random
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate SQLite database with comprehensive test data for robust accounting reports'

    def handle(self, *args, **options):
        """Create comprehensive test data for development and reporting"""
        
        self.stdout.write(self.style.WARNING('🏗️  Creating comprehensive test data for accounting reports...'))
        
        try:
            # 1. Create Test Companies
            self.stdout.write('📊 Creating test companies...')
            companies = self.create_companies()
            
            # 2. Create Test Users
            self.stdout.write('👥 Creating test users...')
            users = self.create_users(companies)
            
            # 3. Create Chart of Accounts
            self.stdout.write('📈 Creating chart of accounts...')
            accounts = self.create_chart_of_accounts(companies[0])
            
            # 4. Create Customers & Vendors
            self.stdout.write('🤝 Creating customers and vendors...')
            customers = self.create_customers(companies[0])
            vendors = self.create_vendors(companies[0])
            
            # 5. Create Bank Accounts
            self.stdout.write('🏦 Creating bank accounts...')
            bank_accounts = self.create_bank_accounts(companies[0])
            
            # 6. Create Employees
            self.stdout.write('👨‍💼 Creating employees...')
            employees = self.create_employees(companies[0])
            
            # 7. Create Bank Transactions
            self.stdout.write('🏧 Creating bank transactions...')
            self.create_bank_transactions(bank_accounts)
            
            # 8. Create Payroll
            self.stdout.write('💵 Creating payroll records...')
            self.create_payroll(employees)
            
            self.stdout.write(self.style.SUCCESS('✅ Test data created successfully!'))
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('📈 Test Data Summary:'))
            self.stdout.write(f'  • Companies: {len(companies)}')
            self.stdout.write(f'  • Users: {len(users)}')
            self.stdout.write(f'  • Chart of Accounts: {len(accounts)} accounts')
            self.stdout.write(f'  • Customers: {len(customers)}')
            self.stdout.write(f'  • Vendors: {len(vendors)}')
            self.stdout.write(f'  • Bank Accounts: {len(bank_accounts)}')
            self.stdout.write(f'  • Employees: {len(employees)}')
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('🎯 Ready for comprehensive reporting and testing!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating test data: {e}'))
            import traceback
            traceback.print_exc()

    def create_companies(self):
        """Create test companies"""
        companies_data = [
            {
                'company_name': 'Acme Corporation',
                'company_notes': 'Main test company for comprehensive accounting testing'
            },
            {
                'company_name': 'Tech Innovations LLC', 
                'company_notes': 'Secondary company for multi-company testing'
            }
        ]
        
        companies = []
        for data in companies_data:
            company, created = Company.objects.get_or_create(
                company_name=data['company_name'],
                defaults=data
            )
            companies.append(company)
            
        return companies

    def create_users(self, companies):
        """Create test users with different roles"""
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@acme.com',
                'password': 'admin123',
                'role': 'Admin'
            },
            {
                'username': 'accountant',
                'email': 'accountant@acme.com', 
                'password': 'accountant123',
                'role': 'Accountant'
            },
            {
                'username': 'bookkeeper',
                'email': 'bookkeeper@acme.com',
                'password': 'bookkeeper123', 
                'role': 'Bookkeeper'
            }
        ]
        
        users = []
        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'password_hash': make_password(data['password'])
                }
            )
            
            # Create user-company relationship
            UserCompanyRole.objects.get_or_create(
                user=user,
                company=companies[0],
                defaults={'role': data['role']}
            )
            users.append(user)
            
        return users

    def create_chart_of_accounts(self, company):
        """Create comprehensive chart of accounts"""
        accounts_data = [
            # Assets
            {'code': '1000', 'name': 'Cash and Cash Equivalents', 'type': 'Asset'},
            {'code': '1100', 'name': 'Checking Account', 'type': 'Asset'},
            {'code': '1200', 'name': 'Savings Account', 'type': 'Asset'},
            {'code': '1300', 'name': 'Accounts Receivable', 'type': 'Asset'},
            {'code': '1400', 'name': 'Inventory', 'type': 'Asset'},
            {'code': '1500', 'name': 'Office Equipment', 'type': 'Asset'},
            {'code': '1600', 'name': 'Computer Equipment', 'type': 'Asset'},
            
            # Liabilities  
            {'code': '2000', 'name': 'Accounts Payable', 'type': 'Liability'},
            {'code': '2100', 'name': 'Credit Cards Payable', 'type': 'Liability'},
            {'code': '2200', 'name': 'Accrued Expenses', 'type': 'Liability'},
            {'code': '2300', 'name': 'Payroll Liabilities', 'type': 'Liability'},
            {'code': '2400', 'name': 'Sales Tax Payable', 'type': 'Liability'},
            
            # Equity
            {'code': '3000', 'name': 'Owner Equity', 'type': 'Equity'},
            {'code': '3100', 'name': 'Retained Earnings', 'type': 'Equity'},
            
            # Revenue
            {'code': '4000', 'name': 'Sales Revenue', 'type': 'Revenue'},
            {'code': '4100', 'name': 'Service Revenue', 'type': 'Revenue'},
            {'code': '4200', 'name': 'Consulting Revenue', 'type': 'Revenue'},
            {'code': '4300', 'name': 'Interest Income', 'type': 'Revenue'},
            
            # Expenses
            {'code': '5000', 'name': 'Cost of Goods Sold', 'type': 'Expense'},
            {'code': '6000', 'name': 'Salaries and Wages', 'type': 'Expense'},
            {'code': '6100', 'name': 'Rent Expense', 'type': 'Expense'},
            {'code': '6200', 'name': 'Office Supplies', 'type': 'Expense'},
            {'code': '6300', 'name': 'Utilities', 'type': 'Expense'},
            {'code': '6400', 'name': 'Insurance', 'type': 'Expense'},
            {'code': '6500', 'name': 'Marketing & Advertising', 'type': 'Expense'},
            {'code': '6600', 'name': 'Professional Services', 'type': 'Expense'},
            {'code': '6700', 'name': 'Travel & Entertainment', 'type': 'Expense'},
            {'code': '6800', 'name': 'Telecommunications', 'type': 'Expense'},
        ]
        
        accounts = []
        for data in accounts_data:
            account, created = ChartOfAccounts.objects.get_or_create(
                company=company,
                account_code=data['code'],
                defaults={
                    'account_name': data['name'],
                    'account_type': data['type']
                }
            )
            accounts.append(account)
            
        return accounts

    def create_customers(self, company):
        """Create test customers"""
        customers_data = [
            {
                'name': 'ABC Manufacturing Co.',
                'email': 'orders@abcmfg.com',
                'phone': '555-0101',
                'address': '123 Industrial Blvd, Manufacturing City, ST 12345',
                'payment_terms': 'Net 30'
            },
            {
                'name': 'XYZ Retail Chain',
                'email': 'accounting@xyzretail.com',
                'phone': '555-0102', 
                'address': '456 Commerce St, Retail Town, ST 12346',
                'payment_terms': 'Net 15'
            },
            {
                'name': 'Global Tech Solutions',
                'email': 'billing@globaltech.com',
                'phone': '555-0103',
                'address': '789 Technology Dr, Tech Park, ST 12347', 
                'payment_terms': 'Net 45'
            },
            {
                'name': 'Local Services LLC',
                'email': 'payments@localservices.com',
                'phone': '555-0104',
                'address': '321 Service Ave, Service City, ST 12348',
                'payment_terms': 'Due on Receipt'
            },
            {
                'name': 'Enterprise Solutions Inc',
                'email': 'finance@enterprise.com',
                'phone': '555-0105',
                'address': '654 Enterprise Way, Business District, ST 12349',
                'payment_terms': 'Net 30'
            }
        ]
        
        customers = []
        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                company=company,
                name=data['name'],
                defaults=data
            )
            customers.append(customer)
            
        return customers

    def create_vendors(self, company):
        """Create test vendors"""
        vendors_data = [
            {
                'name': 'Office Supply Depot',
                'email': 'accounts@officesupply.com',
                'phone': '555-0201',
                'address': '111 Supply St, Supply Town, ST 12350',
                'payment_terms': 'Net 30'
            },
            {
                'name': 'Tech Equipment Corp',
                'email': 'billing@techequip.com',
                'phone': '555-0202',
                'address': '222 Equipment Rd, Tech Valley, ST 12351', 
                'payment_terms': 'Net 15'
            },
            {
                'name': 'Utility Services Inc',
                'email': 'payments@utilityservices.com',
                'phone': '555-0203',
                'address': '333 Utility Blvd, Service Center, ST 12352',
                'payment_terms': 'Due on Receipt'
            },
            {
                'name': 'Professional Consulting',
                'email': 'invoices@profconsulting.com',
                'phone': '555-0204',
                'address': '444 Consulting Ave, Professional Plaza, ST 12353',
                'payment_terms': 'Net 30'
            },
            {
                'name': 'Marketing Solutions LLC',
                'email': 'accounting@marketing.com',
                'phone': '555-0205',
                'address': '555 Marketing Way, Creative District, ST 12354',
                'payment_terms': 'Net 45'
            }
        ]
        
        vendors = []
        for data in vendors_data:
            vendor, created = Vendor.objects.get_or_create(
                company=company,
                name=data['name'],
                defaults=data
            )
            vendors.append(vendor)
            
        return vendors

    def create_bank_accounts(self, company):
        """Create test bank accounts"""
        bank_accounts_data = [
            {
                'bank_name': 'First National Bank',
                'account_number': '****1234',
                'account_type': 'Checking',
                'balance': Decimal('50000.00')
            },
            {
                'bank_name': 'Credit Union Savings',
                'account_number': '****5678',
                'account_type': 'Savings',
                'balance': Decimal('25000.00')
            },
            {
                'bank_name': 'Business Credit Line',
                'account_number': '****9012',
                'account_type': 'Credit',
                'balance': Decimal('-5000.00')
            }
        ]
        
        bank_accounts = []
        for data in bank_accounts_data:
            account, created = BankAccount.objects.get_or_create(
                company=company,
                bank_name=data['bank_name'],
                account_number=data['account_number'],
                defaults=data
            )
            bank_accounts.append(account)
            
        return bank_accounts

    def create_employees(self, company):
        """Create test employees based on schema"""
        employees_data = [
            {
                'name': 'John Smith',
                'email': 'john.smith@acme.com',
                'hourly_rate': Decimal('32.50'),
                'tax_withholding': Decimal('0.25')
            },
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@acme.com',
                'hourly_rate': Decimal('38.75'),
                'tax_withholding': Decimal('0.28')
            },
            {
                'name': 'Mike Davis',
                'email': 'mike.davis@acme.com',
                'hourly_rate': Decimal('22.50'),
                'tax_withholding': Decimal('0.20')
            },
            {
                'name': 'Lisa Chen',
                'email': 'lisa.chen@acme.com',
                'hourly_rate': Decimal('35.00'),
                'tax_withholding': Decimal('0.26')
            },
            {
                'name': 'Robert Wilson',
                'email': 'robert.wilson@acme.com',
                'hourly_rate': Decimal('28.00'),
                'tax_withholding': Decimal('0.22')
            }
        ]
        
        employees = []
        for data in employees_data:
            # Create employee directly without user relationship
            employee, created = Employee.objects.get_or_create(
                company=company,
                email=data['email'],
                defaults={
                    'name': data['name'],
                    'hourly_rate': data['hourly_rate'],
                    'tax_withholding': data['tax_withholding'],
                    'employee_notes': f"Test employee: {data['name']}"
                }
            )
            employees.append(employee)
            
        return employees
            
        return employees

    def create_bank_transactions(self, bank_accounts):
        """Create realistic bank transactions"""
        transaction_types = [
            ('Deposit', 'Customer Payment'),
            ('Deposit', 'Bank Interest'),
            ('Withdrawal', 'Office Rent'),
            ('Withdrawal', 'Utilities Payment'),
            ('Withdrawal', 'Supplier Payment'),
            ('Withdrawal', 'Payroll'),
            ('Deposit', 'Service Revenue'),
            ('Withdrawal', 'Equipment Purchase'),
        ]
        
        # Create transactions for the last 3 months
        start_date = timezone.now() - timedelta(days=90)
        
        for bank_account in bank_accounts[:1]:  # Just checking account for now
            for i in range(30):  # 30 transactions
                transaction_date = start_date + timedelta(days=random.randint(0, 90))
                trans_type, description = random.choice(transaction_types)
                
                if trans_type == 'Deposit':
                    amount = Decimal(str(random.uniform(500, 5000))).quantize(Decimal('0.01'))
                else:
                    amount = -Decimal(str(random.uniform(100, 3000))).quantize(Decimal('0.01'))
                
                BankTransaction.objects.create(
                    bank_account=bank_account,
                    transaction_date=transaction_date,
                    description=description,
                    amount=amount,
                    transaction_type=trans_type,
                    transaction_number=f"TXN{random.randint(1000, 9999)}",
                    reconciled=random.choice([True, False]),
                    is_imported=False
                )

    def create_payroll(self, employees):
        """Create payroll records"""
        # Create payroll for last 3 months
        start_date = timezone.now() - timedelta(days=90)
        
        for i in range(6):  # Bi-weekly payroll for 3 months
            pay_date = start_date + timedelta(days=i * 14)
            pay_period_start = pay_date - timedelta(days=13)
            pay_period_end = pay_date
            
            for employee in employees:
                # Calculate pay based on hourly rate (bi-weekly, 80 hours)
                hours_worked = Decimal('80.00')  # Standard bi-weekly hours
                gross_pay = employee.hourly_rate * hours_worked
                taxes = gross_pay * employee.tax_withholding
                net_pay = gross_pay - taxes
                
                Payroll.objects.get_or_create(
                    employee=employee,
                    pay_period_start=pay_period_start.date(),
                    pay_period_end=pay_period_end.date(),
                    defaults={
                        'gross_pay': gross_pay,
                        'net_pay': net_pay,
                        'taxes_withheld': taxes,
                        'payment_date': pay_date.date()
                    }
                )
