import os
import django
import sys

# Add the backend directory to Python path
sys.path.append('.')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lifeline_backend.settings')
django.setup()

from django.db import connection

# Get list of tables in SQLite
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]

print('📊 Django SQLite Tables Created by Migrations:')
print(f'Total tables: {len(tables)}')
print()

# Group by app/purpose
django_system_tables = [t for t in tables if t.startswith(('auth_', 'django_', 'sqlite_'))]
business_tables = [t for t in tables if not t.startswith(('auth_', 'django_', 'sqlite_'))]

print('🔧 Django System Tables:')
for table in django_system_tables:
    print(f'  - {table}')

print('\n💼 Business Logic Tables:')
for table in business_tables:
    print(f'  - {table}')

print(f'\n📝 Summary:')
print(f'  - Django System Tables: {len(django_system_tables)}')
print(f'  - Business Tables: {len(business_tables)}')
print(f'  - Total: {len(tables)}')
