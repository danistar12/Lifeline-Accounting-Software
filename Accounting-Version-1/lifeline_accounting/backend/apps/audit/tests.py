from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import Company
from .models import AuditLog
from .utils import log_action
from .decorators import audit_view, audit_change

User = get_user_model()


class AuditLogModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            legal_name="Test Company, Inc.",
            currency="USD",
            fiscal_year_end="12-31"
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_audit_log_creation(self):
        """Test that we can create an audit log"""
        log = AuditLog.objects.create(
            company=self.company,
            user=self.user,
            action_type=AuditLog.CREATE,
            action_description="Test log entry"
        )
        
        self.assertEqual(log.action_type, AuditLog.CREATE)
        self.assertEqual(log.action_description, "Test log entry")
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.company, self.company)
        
    def test_audit_log_string_representation(self):
        """Test the string representation of an audit log"""
        log = AuditLog.objects.create(
            company=self.company,
            user=self.user,
            action_type=AuditLog.CREATE,
            action_description="Test log entry"
        )
        
        expected_start = f"{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.user.username}"
        self.assertTrue(str(log).startswith(expected_start))
        self.assertTrue("Test log entry" in str(log))


class AuditLogUtilsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(
            name="Test Company",
            legal_name="Test Company, Inc.",
            currency="USD",
            fiscal_year_end="12-31"
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_log_action_basic(self):
        """Test the log_action utility with basic parameters"""
        request = self.factory.get('/')
        request.user = self.user
        
        log = log_action(
            request=request,
            company=self.company,
            action_type=AuditLog.VIEW,
            action_description="Test view action"
        )
        
        self.assertEqual(log.action_type, AuditLog.VIEW)
        self.assertEqual(log.action_description, "Test view action")
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.company, self.company)
        
    def test_log_action_with_object(self):
        """Test logging with a related object"""
        request = self.factory.get('/')
        request.user = self.user
        
        # Use User as the related object for testing
        another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='testpass123'
        )
        
        log = log_action(
            request=request,
            company=self.company,
            action_type=AuditLog.VIEW,
            action_description="Viewed user profile",
            obj=another_user
        )
        
        self.assertEqual(log.content_type.model, 'user')
        self.assertEqual(log.object_id, str(another_user.pk))
        
    def test_log_action_with_data(self):
        """Test logging with before/after data"""
        request = self.factory.get('/')
        request.user = self.user
        
        data_before = {"name": "Old Name", "age": 30}
        data_after = {"name": "New Name", "age": 31}
        
        log = log_action(
            request=request,
            company=self.company,
            action_type=AuditLog.UPDATE,
            action_description="Updated user profile",
            data_before=data_before,
            data_after=data_after
        )
        
        self.assertEqual(log.data_before, data_before)
        self.assertEqual(log.data_after, data_after)


class AuditViewDecoratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(
            name="Test Company",
            legal_name="Test Company, Inc.",
            currency="USD",
            fiscal_year_end="12-31"
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Define a test view with our decorator
        @audit_view(action_type=AuditLog.VIEW, description_template="Test view {model}")
        def test_view(request, company):
            return "Success"
            
        self.test_view = test_view
        
    def test_decorator_logs_action(self):
        """Test that the decorator logs the action"""
        request = self.factory.get('/')
        request.user = self.user
        
        # Call the decorated view
        self.test_view(request, self.company)
        
        # Check if a log was created
        log = AuditLog.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.action_type, AuditLog.VIEW)
        self.assertTrue("Test view" in log.action_description)
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.company, self.company)


class AuditAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(
            name="Test Company",
            legal_name="Test Company, Inc.",
            currency="USD",
            fiscal_year_end="12-31"
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regular123'
        )
        
        # Create some audit logs
        AuditLog.objects.create(
            company=self.company,
            user=self.admin_user,
            action_type=AuditLog.CREATE,
            action_description="Created something"
        )
        AuditLog.objects.create(
            company=self.company,
            user=self.regular_user,
            action_type=AuditLog.VIEW,
            action_description="Viewed something"
        )
        
    def test_audit_log_list_requires_authentication(self):
        """Test that audit log list view requires authentication"""
        url = reverse('audit:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        
    def test_audit_log_list_with_superuser(self):
        """Test that superuser can see all audit logs"""
        url = reverse('audit:list')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        
    def test_audit_log_detail_with_superuser(self):
        """Test that superuser can see audit log details"""
        log_id = AuditLog.objects.first().id
        url = reverse('audit:detail', kwargs={'pk': log_id})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], log_id)
