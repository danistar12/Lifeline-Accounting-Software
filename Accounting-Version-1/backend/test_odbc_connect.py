#!/usr/bin/env python3
"""
Small diagnostics script to run on the Linux server to:
- print available ODBC drivers
- try to connect to SQL Server using common drivers (18, 17, others)
- print detailed errors for troubleshooting

Usage: python3 test_odbc_connect.py
"""
import pyodbc
import sys

SERVER = "10.100.5.27"
DATABASE = "LLAcctTemp"
UID = "LLAcct"
PWD = "SilverMoon#3"

print("pyodbc version:", pyodbc.version)
drivers = pyodbc.drivers()
print("Detected ODBC drivers:")
for d in drivers:
    print(" -", d)

candidates = [
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
]
# add any drivers that look like sqlserver drivers from the system list
for d in drivers:
    if 'ODBC Driver' in d and 'SQL Server' in d and d not in candidates:
        candidates.append(d)

if not candidates:
    print("No candidate SQL Server ODBC drivers found. Install msodbcsql17 or msodbcsql18.")
    sys.exit(2)

for drv in candidates:
    conn_str = (
        f"Driver={{{drv}}};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        f"UID={UID};"
        f"PWD={PWD};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    print("\nTrying driver:", drv)
    try:
        cnxn = pyodbc.connect(conn_str, timeout=5)
        print("Connected with:", drv)
        cnxn.close()
        sys.exit(0)
    except Exception as e:
        print("Failed with:", drv)
        print(repr(e))

print("All candidate drivers failed.")
sys.exit(1)
