from django.core.management.base import BaseCommand
from apps.audit.models import AuditLog
from apps.accounts.models import User
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import csv


class Command(BaseCommand):
    help = 'Export audit logs to CSV for external analysis'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, required=True,
                            help='Output CSV file path')
        parser.add_argument('--days', type=int, default=30,
                            help='Export logs from the last N days')
        parser.add_argument('--company', type=int,
                            help='Only export logs for a specific company ID')
        parser.add_argument('--user', type=str,
                            help='Only export logs for a specific username')
        parser.add_argument('--action', type=str,
                            help='Only export logs of a specific action type')

    def handle(self, *args, **options):
        output_file = options['output']
        days_back = options['days']
        company_id = options['company']
        username = options['user']
        action_type = options['action']
        
        start_date = timezone.now() - timezone.timedelta(days=days_back)
        
        # Build query
        query = AuditLog.objects.filter(timestamp__gte=start_date)
        
        if company_id:
            query = query.filter(company_id=company_id)
            
        if username:
            try:
                user = User.objects.get(username=username)
                query = query.filter(user=user)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User {username} not found"))
                return
                
        if action_type:
            query = query.filter(action_type=action_type)
            
        # Count and inform
        count = query.count()
        self.stdout.write(f"Exporting {count} audit log entries...")
        
        # Define CSV columns
        fieldnames = [
            'timestamp', 'user', 'user_email', 'company', 'action_type',
            'action_description', 'model', 'object_id', 'details',
            'ip_address', 'user_agent'
        ]
        
        # Export to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Process in chunks to avoid memory issues
            offset = 0
            chunk_size = 1000
            
            while True:
                logs = query.select_related('user', 'company', 'content_type')[offset:offset+chunk_size]
                if not logs:
                    break
                    
                for log in logs:
                    writer.writerow({
                        'timestamp': log.timestamp.isoformat(),
                        'user': log.user.username if log.user else 'System',
                        'user_email': log.user.email if log.user else '',
                        'company': log.company.name,
                        'action_type': log.action_type,
                        'action_description': log.action_description,
                        'model': log.content_type.model if log.content_type else '',
                        'object_id': log.object_id or '',
                        'details': log.details or '',
                        'ip_address': log.ip_address or '',
                        'user_agent': log.user_agent[:100] if log.user_agent else ''
                    })
                    
                offset += chunk_size
                self.stdout.write(f"Exported {min(offset, count)} of {count} entries...")
                
        self.stdout.write(self.style.SUCCESS(f"Successfully exported {count} audit log entries to {output_file}"))
