import pyodbc

# Connect to the database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=10.100.5.27;'
    'DATABASE=LifelineAccounting;'
    'UID=LLAcct;'
    'PWD=SilverMoon#3'
)

cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sysobjects WHERE xtype = 'U' ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]

print('✅ Connected to LifelineAccounting database!')
print(f'Found {len(tables)} existing tables:')
for table in tables:
    print(f'  - {table}')

# Get column info for a few key tables if they exist
key_tables = ['Users', 'Companies', 'ChartOfAccounts', 'GeneralLedger']
for table_name in key_tables:
    if table_name in tables:
        print(f'\n📋 Columns in {table_name}:')
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' ORDER BY ORDINAL_POSITION")
        columns = [row[0] for row in cursor.fetchall()]
        for col in columns:
            print(f'    - {col}')

conn.close()
print('\n🛡️  SAFETY NOTE: Your existing tables will NOT be modified by Django!')
