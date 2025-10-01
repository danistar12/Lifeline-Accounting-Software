from django.db import models
from ..accounts.models import Company

class ImportFile(models.Model):
    CompanyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Type of data being imported
    FILE_TYPE_CHOICES = [
        ('coa', 'Chart of Accounts'),
        ('customers', 'Customers'),
        ('vendors', 'Vendors'),
        ('invoices', 'Invoices'),
        ('bills', 'Bills'),
    ]
    FileType = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    File = models.FileField(upload_to='import_files/')
    UploadedAt = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=20, default='pending')  # pending, processing, completed, failed

    def __str__(self):
        return f'{self.File.name} ({self.Status})'
  
class ImportError(models.Model):
    """
    Row-level errors for a given import file.
    """
    ImportFileID = models.ForeignKey(ImportFile, on_delete=models.CASCADE, related_name='errors')
    RowNumber = models.IntegerField(null=True)
    ErrorMessage = models.TextField()

    class Meta:
        db_table = 'ImportErrors'
        verbose_name = 'Import Error'
        verbose_name_plural = 'Import Errors'
    
    def __str__(self):
        return f'Row {self.RowNumber}: {self.ErrorMessage}'
