import csv, os
from .models import ImportFile
from apps.accounting.models import ChartOfAccount
from apps.customers.models import Customer
from apps.vendors.models import Vendor
from apps.invoices.models import Invoice
from apps.bills.models import Bill
from django.conf import settings

def process_import_file(import_file: ImportFile):
    """
    Process the uploaded import file synchronously.
    Determine file type and parse accordingly.
    Update import_file.status to 'completed' or 'failed'.
    """
    path = import_file.file.path
    name = os.path.basename(path)
    errors = []
    from .models import ImportError
    # Clear previous errors
    import_file.errors.all().delete()
    try:
        if not name.lower().endswith('.csv'):
            raise ValueError('Unsupported file type')
        # Choose handler based on declared file_type
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if import_file.file_type == 'coa':
                errors = _import_coa(reader, import_file.company)
            elif import_file.file_type == 'customers':
                errors = _import_customers(reader, import_file.company)
            elif import_file.file_type == 'vendors':
                errors = _import_vendors(reader, import_file.company)
            elif import_file.file_type == 'invoices':
                errors = _import_invoices(reader, import_file.company)
            elif import_file.file_type == 'bills':
                errors = _import_bills(reader, import_file.company)
            else:
                raise ValueError(f'Unknown file_type {import_file.file_type}')
        import_file.status = 'completed'
    except Exception as e:
        import_file.status = 'failed'
        errors.append({'row': None, 'error': str(e)})
    # TODO: save or log errors for user review
    import_file.save()
    # Persist row-level errors
    for err in errors:
        ImportError.objects.create(
            import_file=import_file,
            row_number=err.get('row'),
            error_message=err.get('error')
        )
    return errors

def _import_coa(reader, company):
    errors = []
    for idx, row in enumerate(reader, start=2):
        try:
            ChartOfAccount.objects.update_or_create(
                company=company,
                account_code=row['account_code'],
                defaults={
                    'account_name': row.get('account_name', ''),
                    'account_type': row.get('account_type', ''),
                }
            )
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})
    return errors

def _import_customers(reader, company):
    errors = []
    for idx, row in enumerate(reader, start=2):
        try:
            Customer.objects.update_or_create(
                company=company,
                customer_name=row.get('customer_name', ''),
            )
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})
    return errors

def _import_vendors(reader, company):
    errors = []
    for idx, row in enumerate(reader, start=2):
        try:
            Vendor.objects.update_or_create(
                company=company,
                vendor_name=row.get('vendor_name', ''),
            )
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})
    return errors

def _import_invoices(reader, company):
    errors = []
    for idx, row in enumerate(reader, start=2):
        try:
            # Expecting column 'customer_id' referring to existing Customer
            cust = Customer.objects.get(company=company, pk=row.get('customer_id'))
            Invoice.objects.create(company=company, customer=cust)
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})
    return errors

def _import_bills(reader, company):
    errors = []
    for idx, row in enumerate(reader, start=2):
        try:
            vend = Vendor.objects.get(company=company, pk=row.get('vendor_id'))
            Bill.objects.create(company=company, vendor=vend)
        except Exception as e:
            errors.append({'row': idx, 'error': str(e)})
    return errors
