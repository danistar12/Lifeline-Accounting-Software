from django.core.management.base import BaseCommand
import datetime
from apps.audit.models import AuditLog
from django.utils import timezone


class Command(BaseCommand):
    help = 'Deletes old audit log entries to keep the database size manageable'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=90,
                            help='Delete logs older than this many days')
        parser.add_argument('--dry-run', action='store_true',
                            help='Print what would be deleted without actually deleting')
        parser.add_argument('--company', type=int,
                            help='Only delete logs for a specific company ID')

    def handle(self, *args, **options):
        days_old = options['days']
        dry_run = options['dry_run']
        company_id = options['company']
        
        cutoff_date = timezone.now() - datetime.timedelta(days=days_old)
        
        # Build query
        query = AuditLog.objects.filter(timestamp__lt=cutoff_date)
        if company_id:
            query = query.filter(company_id=company_id)
            
        # Count records to be deleted
        count = query.count()
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'Would delete {count} log entries older than {days_old} days'
            ))
            return
            
        # Delete in chunks to avoid memory issues
        deleted_count = 0
        chunk_size = 1000
        
        while True:
            # Get IDs for a chunk
            ids = list(query.values_list('id', flat=True)[:chunk_size])
            if not ids:
                break
                
            # Delete this chunk
            AuditLog.objects.filter(id__in=ids).delete()
            deleted_count += len(ids)
            
            # Report progress
            self.stdout.write(f'Deleted {deleted_count} of {count} log entries...')
            
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {deleted_count} audit log entries older than {days_old} days'
        ))
