import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Set up logging directories and ensure proper permissions for FedRAMP compliance'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up logging infrastructure...'))
        
        # Create logs directory
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        
        try:
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir, mode=0o755)
                self.stdout.write(f'✓ Created logs directory: {logs_dir}')
            else:
                self.stdout.write(f'✓ Logs directory already exists: {logs_dir}')
            
            # Create individual log files with proper permissions
            log_files = [
                'lifeline.log',
                'security.log', 
                'audit.log'
            ]
            
            for log_file in log_files:
                log_path = os.path.join(logs_dir, log_file)
                if not os.path.exists(log_path):
                    # Create empty log file
                    open(log_path, 'a').close()
                    # Set permissions (owner: read/write, group: read, others: none)
                    os.chmod(log_path, 0o640)
                    self.stdout.write(f'✓ Created log file: {log_path}')
                else:
                    self.stdout.write(f'✓ Log file already exists: {log_path}')
            
            # Set directory permissions
            os.chmod(logs_dir, 0o755)
            
            self.stdout.write(self.style.SUCCESS('\n🔒 Logging infrastructure setup complete!'))
            self.stdout.write('Log files created with secure permissions (640)')
            self.stdout.write('Directory permissions set to 755')
            
        except PermissionError as e:
            self.stdout.write(
                self.style.ERROR(f'Permission denied: {e}')
            )
            self.stdout.write(
                self.style.WARNING('You may need to run this command with appropriate permissions')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up logging: {e}')
            )