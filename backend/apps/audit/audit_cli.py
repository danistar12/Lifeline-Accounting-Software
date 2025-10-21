#!/usr/bin/env python
"""
Command-line utility for working with audit logs.

This script provides direct access to audit logs for administrative purposes.
It can be used for viewing, filtering, and exporting audit logs outside of the 
Django admin interface.

Usage:
  python audit_cli.py list [--days=30] [--company=1] [--user=admin] [--action=login]
  python audit_cli.py view <log_id>
  python audit_cli.py export <output_csv> [--days=30] [--company=1]
  python audit_cli.py stats [--days=30] [--company=1]
  python audit_cli.py prune [--days=90] [--company=1] [--dry-run]
"""

import os
import sys
import django
import argparse
from datetime import datetime, timedelta
import csv
import json

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lifeline_backend.settings_production')
django.setup()

from apps.audit.models import AuditLog
from apps.accounts.models import User, Company
from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator


def format_log_entry(log):
    """Format a log entry for display"""
    user_str = log.user.username if log.user else 'System'
    model_str = log.content_type.model if log.content_type else 'None'
    
    return (
        f"ID: {log.id}\n"
        f"Timestamp: {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"User: {user_str}\n"
        f"Company: {log.company.name}\n"
        f"Action: {log.action_type} - {log.action_description}\n"
        f"Model: {model_str}\n"
        f"Object ID: {log.object_id or 'None'}\n"
        f"IP: {log.ip_address or 'Unknown'}\n"
    )


def list_logs(args):
    """List audit logs with optional filters"""
    # Build query
    query = AuditLog.objects
    
    # Apply filters
    if args.days:
        start_date = timezone.now() - timedelta(days=args.days)
        query = query.filter(timestamp__gte=start_date)
        
    if args.company:
        query = query.filter(company_id=args.company)
        
    if args.user:
        try:
            user = User.objects.get(username=args.user)
            query = query.filter(user=user)
        except User.DoesNotExist:
            print(f"User {args.user} not found")
            return
            
    if args.action:
        query = query.filter(action_type=args.action)
        
    # Get results with pagination
    total = query.count()
    query = query.order_by('-timestamp')
    
    paginator = Paginator(query, args.page_size)
    page = paginator.page(args.page)
    
    # Print header
    print(f"Audit Logs ({page.start_index()}-{page.end_index()} of {total})")
    print("=" * 60)
    
    # Print logs
    for log in page.object_list:
        print(format_log_entry(log))
        print("-" * 60)
        
    # Print pagination info
    if paginator.num_pages > 1:
        print(f"Page {args.page} of {paginator.num_pages}")
        print(f"Use --page=N to view other pages")


def view_log(args):
    """View a single log entry in detail"""
    try:
        log = AuditLog.objects.get(id=args.log_id)
    except AuditLog.DoesNotExist:
        print(f"Log ID {args.log_id} not found")
        return
        
    print(format_log_entry(log))
    
    # Print details
    if log.details:
        print("Details:")
        print(log.details)
        
    # Print data before/after if available
    if log.data_before or log.data_after:
        print("\nChanges:")
        
        all_keys = set()
        if log.data_before:
            all_keys.update(log.data_before.keys())
        if log.data_after:
            all_keys.update(log.data_after.keys())
            
        for key in sorted(all_keys):
            before = log.data_before.get(key, "N/A") if log.data_before else "N/A"
            after = log.data_after.get(key, "N/A") if log.data_after else "N/A"
            
            if before != after:
                print(f"  {key}:")
                print(f"    Before: {before}")
                print(f"    After:  {after}")


def export_logs(args):
    """Export logs to CSV"""
    # Build query
    query = AuditLog.objects
    
    # Apply filters
    if args.days:
        start_date = timezone.now() - timedelta(days=args.days)
        query = query.filter(timestamp__gte=start_date)
        
    if args.company:
        query = query.filter(company_id=args.company)
        
    # Count and inform
    count = query.count()
    print(f"Exporting {count} audit log entries...")
    
    # Define CSV columns
    fieldnames = [
        'id', 'timestamp', 'user', 'user_email', 'company', 'action_type',
        'action_description', 'model', 'object_id', 'details',
        'ip_address', 'user_agent'
    ]
    
    # Export to CSV
    with open(args.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
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
                    'id': log.id,
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
            print(f"Exported {min(offset, count)} of {count} entries...")
            
    print(f"Successfully exported {count} audit log entries to {args.output_csv}")


def generate_stats(args):
    """Generate statistics about audit logs"""
    # Build query
    query = AuditLog.objects
    
    # Apply filters
    if args.days:
        start_date = timezone.now() - timedelta(days=args.days)
        query = query.filter(timestamp__gte=start_date)
        
    if args.company:
        query = query.filter(company_id=args.company)
        company_name = Company.objects.get(id=args.company).name if Company.objects.filter(id=args.company).exists() else f"Company #{args.company}"
    else:
        company_name = "All Companies"
        
    # Generate statistics
    print(f"Audit Log Statistics for {company_name} (Last {args.days} days)")
    print("=" * 60)
    
    # Total count
    total_count = query.count()
    print(f"Total audit log entries: {total_count}")
    
    # Action type breakdown
    action_counts = query.values('action_type').annotate(count=Count('id')).order_by('-count')
    print("\nBreakdown by Action Type:")
    for item in action_counts:
        percentage = (item['count'] / total_count) * 100 if total_count else 0
        print(f"  {item['action_type']:10} : {item['count']:5} ({percentage:.1f}%)")
        
    # User activity (top 10)
    user_counts = query.exclude(user__isnull=True).values(
        'user__username', 'user__email'
    ).annotate(count=Count('id')).order_by('-count')[:10]
    
    print("\nTop 10 Users by Activity:")
    for item in user_counts:
        print(f"  {item['user__username']:15} : {item['count']:5} logs")
        
    # Export to JSON if requested
    if args.output:
        report = {
            'generated_at': timezone.now().isoformat(),
            'period_days': args.days,
            'company_id': args.company,
            'company_name': company_name,
            'total_logs': total_count,
            'action_breakdown': [
                {'action': item['action_type'], 'count': item['count']} 
                for item in action_counts
            ],
            'top_users': [
                {
                    'username': item['user__username'],
                    'email': item['user__email'],
                    'count': item['count']
                } 
                for item in user_counts
            ]
        }
        
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\nReport saved to {args.output}")


def prune_logs(args):
    """Delete old audit logs"""
    # Build query
    cutoff_date = timezone.now() - timedelta(days=args.days)
    query = AuditLog.objects.filter(timestamp__lt=cutoff_date)
    
    if args.company:
        query = query.filter(company_id=args.company)
        
    # Count records to be deleted
    count = query.count()
    
    if args.dry_run:
        print(f"Would delete {count} log entries older than {args.days} days")
        return
        
    if count == 0:
        print("No logs to delete")
        return
        
    # Ask for confirmation
    if not args.force:
        confirm = input(f"Delete {count} log entries? [y/N] ")
        if confirm.lower() != 'y':
            print("Operation cancelled")
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
        print(f"Deleted {deleted_count} of {count} log entries...")
        
    print(f"Successfully deleted {deleted_count} audit log entries older than {args.days} days")


def main():
    # Create parser
    parser = argparse.ArgumentParser(description="Audit Log CLI")
    subparsers = parser.add_subparsers(dest='command')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List audit logs')
    list_parser.add_argument('--days', type=int, default=30, help='List logs from the last N days')
    list_parser.add_argument('--company', type=int, help='Company ID to filter by')
    list_parser.add_argument('--user', type=str, help='Username to filter by')
    list_parser.add_argument('--action', type=str, help='Action type to filter by')
    list_parser.add_argument('--page', type=int, default=1, help='Page number')
    list_parser.add_argument('--page-size', type=int, default=10, help='Items per page')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View a single audit log')
    view_parser.add_argument('log_id', type=int, help='ID of the log to view')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export logs to CSV')
    export_parser.add_argument('output_csv', type=str, help='Output CSV file path')
    export_parser.add_argument('--days', type=int, default=30, help='Export logs from the last N days')
    export_parser.add_argument('--company', type=int, help='Company ID to filter by')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Generate statistics')
    stats_parser.add_argument('--days', type=int, default=30, help='Analyze logs from the last N days')
    stats_parser.add_argument('--company', type=int, help='Company ID to filter by')
    stats_parser.add_argument('--output', type=str, help='Output JSON file path')
    
    # Prune command
    prune_parser = subparsers.add_parser('prune', help='Delete old logs')
    prune_parser.add_argument('--days', type=int, default=90, help='Delete logs older than N days')
    prune_parser.add_argument('--company', type=int, help='Company ID to filter by')
    prune_parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without deleting')
    prune_parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')
    
    # Parse args
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'list':
        list_logs(args)
    elif args.command == 'view':
        view_log(args)
    elif args.command == 'export':
        export_logs(args)
    elif args.command == 'stats':
        generate_stats(args)
    elif args.command == 'prune':
        prune_logs(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
