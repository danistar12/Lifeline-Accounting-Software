from celery import shared_task
from .models import ImportFile
from .services import process_import_file as sync_process_import_file

@shared_task
def process_import_file_task(import_file_id):
    """
    Celery task wrapper for processing an import file.
    """
    try:
        imp = ImportFile.objects.get(pk=import_file_id)
    except ImportFile.DoesNotExist:
        return {'error': 'ImportFile not found'}
    return sync_process_import_file(imp)
