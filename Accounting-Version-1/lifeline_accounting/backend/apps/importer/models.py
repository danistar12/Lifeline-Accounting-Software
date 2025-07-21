from django.db import models
from ..accounts.models import Company

class ImportFile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Type of data being imported
    FILE_TYPE_CHOICES = [
        ('coa', 'Chart of Accounts'),
        ('customers', 'Customers'),
        ('vendors', 'Vendors'),
        ('invoices', 'Invoices'),
        ('bills', 'Bills'),
    ]
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to='import_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed, failed

    def __str__(self):
        return f'{self.file.name} ({self.status})'
  
class ImportError(models.Model):
    """
    Row-level errors for a given import file.
    """
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE, related_name='errors')
    row_number = models.IntegerField(null=True)
    error_message = models.TextField()

    class Meta:
        db_table = 'ImportErrors'
        verbose_name = 'Import Error'
        verbose_name_plural = 'Import Errors'
    
    def __str__(self):
        return f'Row {self.row_number}: {self.error_message}'
