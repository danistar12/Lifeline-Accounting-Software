from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from apps.accounts.models import User, UserCompanyRole, AuditLog
from apps.core.models import *
from apps.banking.models import *
from apps.payroll.models import *
from apps.inventory.models import *
from apps.payments.models import *
from apps.subscriptions.models import *
from apps.documents.models import *

class Command(BaseCommand):
    help = 'Reset all business data in SQLite (keeps Django system tables)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm you want to delete all business data',
        )

    def handle(self, *args, **options):
        """Reset all business data for fresh development start"""
        
        if not options['confirm']:
            self.stdout.write(self.style.ERROR('⚠️  This will delete ALL business data!'))
            self.stdout.write('Use --confirm flag if you really want to proceed')
            self.stdout.write('Example: python manage.py reset_test_data --confirm')
            return
            
        self.stdout.write(self.style.WARNING('🗑️  Resetting all business data...'))
        
        try:
            # Count before deletion
            companies_count = Company.objects.count()
            users_count = User.objects.count() 
            accounts_count = ChartOfAccounts.objects.count()
            
            # Delete all business data (keeps Django auth system intact)
            models_to_clear = [
                # Core models
                AuditLog, UserCompanyRole, ChartOfAccounts, GeneralLedger, 
                Customer, Vendor, Company, FixedAssets, Budgets, Projects,
                CustomFieldValues, CustomFields,
                
                # Banking
                BankTransaction, BankAccount,
                
                # Payroll
                Employee, Payroll,
                
                # Inventory  
                Inventory, InventoryLocation,
                
                # Payments
                Payment,
                
                # Subscriptions
                Subscription,
                
                # Documents
                Document,
                
                # Custom User model (but keep Django's auth tables)
                User,
            ]
            
            total_deleted = 0
            for model in models_to_clear:
                count = model.objects.count()
                if count > 0:
                    model.objects.all().delete()
                    total_deleted += count
                    self.stdout.write(f'  - Cleared {count} {model.__name__} records')
            
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted {total_deleted} total records'))
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('🧹 Database reset complete!'))
            self.stdout.write('Django system tables (auth, sessions, etc.) are preserved')
            self.stdout.write('Run "python manage.py create_test_data" to populate with fresh test data')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error resetting data: {e}'))
            return
