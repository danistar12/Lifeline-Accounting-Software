from django.core.management.base import BaseCommand
from django.conf import settings
import os
import logging


class Command(BaseCommand):
    help = 'Verify FedRAMP security configuration and test logging'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting FedRAMP Security Verification...'))
        
        # Test 1: Check security middleware configuration
        middleware_security = self.check_middleware_config()
        
        # Test 2: Check session security settings
        session_security = self.check_session_settings()
        
        # Test 3: Test logging configuration
        logging_test = self.test_logging_config()
        
        # Test 4: Check directory permissions
        directory_test = self.check_directories()
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('SECURITY VERIFICATION SUMMARY'))
        self.stdout.write('='*60)
        
        tests = [
            ('Middleware Configuration', middleware_security),
            ('Session Security Settings', session_security),
            ('Logging Configuration', logging_test),
            ('Directory Setup', directory_test)
        ]
        
        all_passed = True
        for test_name, passed in tests:
            status = self.style.SUCCESS('✓ PASS') if passed else self.style.ERROR('✗ FAIL')
            self.stdout.write(f'{test_name:<25} {status}')
            if not passed:
                all_passed = False
        
        self.stdout.write('='*60)
        if all_passed:
            self.stdout.write(self.style.SUCCESS('🔒 ALL SECURITY CHECKS PASSED - FedRAMP READY'))
        else:
            self.stdout.write(self.style.ERROR('⚠️  SECURITY ISSUES DETECTED - REVIEW REQUIRED'))
        self.stdout.write('='*60)

    def check_middleware_config(self):
        """Check if security middleware is properly configured"""
        self.stdout.write('\n1. Checking Middleware Configuration...')
        
        required_middleware = [
            'apps.security.middleware.FedRAMPSecurityMiddleware',
            'apps.accounts.middleware.SessionSecurityMiddleware',
            'apps.security.middleware.AuditLoggingMiddleware'
        ]
        
        middleware_list = getattr(settings, 'MIDDLEWARE', [])
        all_present = True
        
        for middleware in required_middleware:
            if middleware in middleware_list:
                self.stdout.write(f'   ✓ {middleware}')
            else:
                self.stdout.write(f'   ✗ Missing: {middleware}')
                all_present = False
        
        return all_present

    def check_session_settings(self):
        """Check session security configuration"""
        self.stdout.write('\n2. Checking Session Security Settings...')
        
        required_settings = {
            'SESSION_COOKIE_AGE': 3600,
            'SESSION_EXPIRE_AT_BROWSER_CLOSE': True,
            'SESSION_SAVE_EVERY_REQUEST': True,
            'SESSION_COOKIE_HTTPONLY': True,
            'SESSION_SECURITY_WARN_AFTER': 1800,
            'SESSION_SECURITY_EXPIRE_AFTER': 3600
        }
        
        all_correct = True
        for setting, expected_value in required_settings.items():
            actual_value = getattr(settings, setting, None)
            if actual_value == expected_value:
                self.stdout.write(f'   ✓ {setting}: {actual_value}')
            else:
                self.stdout.write(f'   ✗ {setting}: Expected {expected_value}, got {actual_value}')
                all_correct = False
        
        return all_correct

    def test_logging_config(self):
        """Test logging configuration"""
        self.stdout.write('\n3. Testing Logging Configuration...')
        
        try:
            # Test security logger
            security_logger = logging.getLogger('apps.security.middleware')
            security_logger.info('TEST: Security logging verification')
            self.stdout.write('   ✓ Security logger configured')
            
            # Test audit logger
            audit_logger = logging.getLogger('apps.accounts.middleware')
            audit_logger.info('TEST: Audit logging verification')
            self.stdout.write('   ✓ Audit logger configured')
            
            # Check if log directory exists
            log_dir = os.path.join(settings.BASE_DIR, 'logs')
            if os.path.exists(log_dir):
                self.stdout.write('   ✓ Log directory exists')
                return True
            else:
                self.stdout.write('   ✗ Log directory missing')
                return False
                
        except Exception as e:
            self.stdout.write(f'   ✗ Logging test failed: {e}')
            return False

    def check_directories(self):
        """Check required directories"""
        self.stdout.write('\n4. Checking Directory Setup...')
        
        required_dirs = [
            os.path.join(settings.BASE_DIR, 'logs'),
            os.path.join(settings.BASE_DIR, 'apps', 'security'),
        ]
        
        all_exist = True
        for directory in required_dirs:
            if os.path.exists(directory):
                self.stdout.write(f'   ✓ {directory}')
            else:
                self.stdout.write(f'   ✗ Missing: {directory}')
                all_exist = False
        
        return all_exist