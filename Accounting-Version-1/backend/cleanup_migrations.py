import os
import shutil

# Define the base directory for the project
base_dir = r'c:\Users\DLloy\OneDrive\Desktop\Data_Centers\Lifeline Accounting Software\Accounting-Version-1\backend'

# Define the paths to the migrations directories and the files to keep
migrations_to_cleanup = [
    {
        'app': 'accounts',
        'keep': ['__init__.py', '0001_initial_squashed_0006_remove_company_address_remove_company_city_and_more.py'],
        'delete': ['0001_initial.py', '0002_company_users_alter_company_admin_user.py', 
                   '0003_alter_company_users.py', '0004_company_address_company_city_company_contact_person_and_more.py',
                   '0005_user_profile_photo.py', '0006_remove_company_address_remove_company_city_and_more.py']
    },
    {
        'app': 'audit',
        'keep': ['__init__.py', '0001_initial_squashed_0003_alter_auditlog_options_and_more.py'],
        'delete': ['0001_initial.py', '0002_auto_20250728_1938.py', '0003_alter_auditlog_options_and_more.py']
    },
    {
        'app': 'payroll',
        'keep': ['__init__.py', '0001_initial_squashed_0002_remove_deduction_paystub_remove_paystub_employee_and_more.py', 
                 '0003_alter_employee_created_date_alter_employee_name_and_more.py'],
        'delete': ['0001_initial.py', '0002_remove_deduction_paystub_remove_paystub_employee_and_more.py']
    },
    {
        'app': 'subscriptions',
        'keep': ['__init__.py', '0001_initial_squashed_0002_alter_subscription_options_and_more.py'],
        'delete': ['0001_initial.py', '0002_alter_subscription_options_and_more.py']
    },
]

def cleanup_migrations():
    """Remove old migration files that have been squashed."""
    print("Starting migration cleanup...")
    
    for migration_info in migrations_to_cleanup:
        app = migration_info['app']
        migrations_dir = os.path.join(base_dir, 'apps', app, 'migrations')
        
        print(f"\nCleaning up migrations for {app} app...")
        
        # Delete old migration files
        for file_to_delete in migration_info['delete']:
            file_path = os.path.join(migrations_dir, file_to_delete)
            if os.path.exists(file_path):
                print(f"Deleting {file_path}")
                os.remove(file_path)
            else:
                print(f"File {file_path} does not exist, skipping...")
                
        # Delete __pycache__ directory
        pycache_dir = os.path.join(migrations_dir, '__pycache__')
        if os.path.exists(pycache_dir):
            print(f"Deleting {pycache_dir} directory")
            shutil.rmtree(pycache_dir)
        
    print("\nMigration cleanup completed!")

if __name__ == "__main__":
    cleanup_migrations()
