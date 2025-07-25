from django.core.management.base import BaseCommand
from apps.accounts.models import User, UserCompanyRole
from apps.core.models import Company, ChartOfAccounts
from apps.contacts.models import Customer, Vendor
from apps.banking.models import BankAccount, BankTransaction
from apps.payroll.models import Employee, Payroll
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Clear all test data from SQLite database (keeps Django system tables)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion of all test data',
        )

    def handle(self, *args, **options):
        """Clear all test data safely"""
        
        if not options['confirm']:
            self.stdout.write(self.style.ERROR('⚠️  This will delete ALL test data!'))
            self.stdout.write('To confirm, run: python manage.py clear_test_data --confirm')
            return
            
        self.stdout.write(self.style.WARNING('🗑️  Clearing all test data...'))
        
        try:
            # Clear in reverse order to handle foreign keys
            self.stdout.write('Clearing payroll records...')
            Payroll.objects.all().delete()
            
            self.stdout.write('Clearing bank transactions...')
            BankTransaction.objects.all().delete()
            
            self.stdout.write('Clearing bank accounts...')
            BankAccount.objects.all().delete()
            
            self.stdout.write('Clearing employees...')
            Employee.objects.all().delete()
            
            self.stdout.write('Clearing customers and vendors...')
            Customer.objects.all().delete()
            Vendor.objects.all().delete()
            
            self.stdout.write('Clearing chart of accounts...')
            ChartOfAccounts.objects.all().delete()
            
            self.stdout.write('Clearing user-company relationships...')
            UserCompanyRole.objects.all().delete()
            
            self.stdout.write('Clearing companies...')
            Company.objects.all().delete()
            
            self.stdout.write('Clearing test users (keeping superusers)...')
            test_users = ['admin', 'accountant', 'bookkeeper']
            User.objects.filter(username__in=test_users).delete()
            
            self.stdout.write(self.style.SUCCESS('✅ Test data cleared successfully!'))
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('💡 Run "python manage.py create_test_data" to recreate test data'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error clearing test data: {e}'))
            import traceback
            traceback.print_exc()
