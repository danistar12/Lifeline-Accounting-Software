from django.core.management.base import BaseCommand
from apps.audit.models import AuditLog
from django.utils import timezone
from django.db.models import Count
import json
from collections import Counter


class Command(BaseCommand):
    help = 'Generates summary statistics of audit logs for reporting'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30,
                            help='Analyze logs from the last N days')
        parser.add_argument('--company', type=int,
                            help='Only analyze logs for a specific company ID')
        parser.add_argument('--output', type=str,
                            help='Output file path for JSON report (optional)')

    def handle(self, *args, **options):
        days_back = options['days']
        company_id = options['company']
        output_file = options.get('output')
        
        start_date = timezone.now() - timezone.timedelta(days=days_back)
        
        # Build base query
        query = AuditLog.objects.filter(timestamp__gte=start_date)
        if company_id:
            query = query.filter(company_id=company_id)
            company_name = query.first().company.name if query.exists() else f"Company #{company_id}"
        else:
            company_name = "All Companies"
            
        # Generate statistics
        self.stdout.write(f"Audit Log Statistics for {company_name} (Last {days_back} days)")
        self.stdout.write("=" * 60)
        
        # Total count
        total_count = query.count()
        self.stdout.write(f"Total audit log entries: {total_count}")
        
        # Action type breakdown
        action_counts = query.values('action_type').annotate(count=Count('id')).order_by('-count')
        self.stdout.write("\nBreakdown by Action Type:")
        for item in action_counts:
            percentage = (item['count'] / total_count) * 100 if total_count else 0
            self.stdout.write(f"  {item['action_type']:10} : {item['count']:5} ({percentage:.1f}%)")
            
        # User activity (top 10)
        user_counts = query.exclude(user__isnull=True).values(
            'user__username', 'user__first_name', 'user__last_name'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        
        self.stdout.write("\nTop 10 Users by Activity:")
        for item in user_counts:
            name = f"{item['user__first_name']} {item['user__last_name']}".strip() or item['user__username']
            self.stdout.write(f"  {name[:20]:20} : {item['count']:5} logs")
            
        # IP address statistics
        ip_counts = Counter(
            query.exclude(ip_address__isnull=True).values_list('ip_address', flat=True)
        ).most_common(10)
        
        self.stdout.write("\nTop 10 IP Addresses:")
        for ip, count in ip_counts:
            self.stdout.write(f"  {ip:15} : {count:5} logs")
            
        # Save to JSON if requested
        if output_file:
            report = {
                'generated_at': timezone.now().isoformat(),
                'period_days': days_back,
                'company_id': company_id,
                'company_name': company_name,
                'total_logs': total_count,
                'action_breakdown': [
                    {'action': item['action_type'], 'count': item['count']} 
                    for item in action_counts
                ],
                'top_users': [
                    {
                        'username': item['user__username'],
                        'name': f"{item['user__first_name']} {item['user__last_name']}".strip(),
                        'count': item['count']
                    } 
                    for item in user_counts
                ],
                'top_ips': [{'ip': ip, 'count': count} for ip, count in ip_counts]
            }
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
                
            self.stdout.write(self.style.SUCCESS(f"\nReport saved to {output_file}"))
        
        self.stdout.write(self.style.SUCCESS("Analysis complete!"))
