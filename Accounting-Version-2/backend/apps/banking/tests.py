from django.urls import reverse
from rest_framework.test import APITestCase
from apps.core.models import Company
from apps.accounts.models import User, UserCompanyRole, ChartOfAccounts
from .models import BankAccount, BankTransaction, BankReconciliation

class BankingAPITest(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='pass')
        # Create a company and assign role
        self.company = Company.objects.create(name='TestCo', admin_user=self.user)
        UserCompanyRole.objects.create(user=self.user, company=self.company, role='Admin')
        # Create a Chart of Accounts entry for linking
        self.coa = ChartOfAccounts.objects.create(
            company=self.company,
            account_code='1000',
            account_name='Cash',
            account_type='Asset',
            balance=0
        )
        self.client.force_authenticate(self.user)
        # Include company header for RBAC
        self.client.credentials(HTTP_X_COMPANY_ID=str(self.company.company_id))
        # Create a bank account
        self.bank_account = BankAccount.objects.create(
            company=self.company,
            account_name='Main Checking',
            account_number='123',
            bank_name='TestBank',
            chart_of_accounts_link=self.coa
        )
        # Create transactions
        BankTransaction.objects.create(
            bank_account=self.bank_account,
            transaction_date='2025-01-01',
            description='Deposit',
            amount=1000,
            transaction_type='Credit'
        )
        BankTransaction.objects.create(
            bank_account=self.bank_account,
            transaction_date='2025-01-05',
            description='Withdrawal',
            amount=-200,
            transaction_type='Debit'
        )

    def test_list_bank_accounts(self):
        response = self.client.get('/api/banking/accounts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['account_name'], 'Main Checking')

    def test_list_transactions(self):
        response = self.client.get('/api/banking/transactions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_reconciliations_empty(self):
        response = self.client.get('/api/banking/reconciliations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
