from rest_framework.test import APITestCase
from apps.core.models import Company
from apps.accounts.models import User, UserCompanyRole, ChartOfAccounts, GeneralLedger
from apps.banking.models import BankAccount, BankTransaction
from django.utils import timezone

class ReportsAPITest(APITestCase):
    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(username='reportuser', password='pass')
        self.company = Company.objects.create(name='ReportCo', admin_user=self.user)
        UserCompanyRole.objects.create(user=self.user, company=self.company, role='Admin')
        # Create accounts: Revenue, Expense, Asset
        self.rev_account = ChartOfAccounts.objects.create(
            company=self.company,
            account_code='4000',
            account_name='Service Revenue',
            account_type='Revenue',
            balance=0
        )
        self.exp_account = ChartOfAccounts.objects.create(
            company=self.company,
            account_code='5000',
            account_name='Office Supplies',
            account_type='Expense',
            balance=0
        )
        # Create ledger entries
        GeneralLedger.objects.create(
            company=self.company,
            account=self.rev_account,
            date='2025-06-01',
            description='Consulting fee',
            debit=0,
            credit=2000,
            user=self.user
        )
        GeneralLedger.objects.create(
            company=self.company,
            account=self.exp_account,
            date='2025-06-02',
            description='Buy supplies',
            debit=300,
            credit=0,
            user=self.user
        )
        # Create a bank account and transactions for cash flow
        self.bank_account = BankAccount.objects.create(
            company=self.company,
            account_name='Checking',
            account_number='321',
            bank_name='TestBank',
            chart_of_accounts_link=self.rev_account
        )
        BankTransaction.objects.create(
            bank_account=self.bank_account,
            transaction_date='2025-06-01',
            description='Deposit',
            amount=2000,
            transaction_type='Credit'
        )
        BankTransaction.objects.create(
            bank_account=self.bank_account,
            transaction_date='2025-06-03',
            description='Purchase supplies',
            amount=-300,
            transaction_type='Debit'
        )
        self.client.force_authenticate(self.user)
        # Include company header for RBAC
        self.client.credentials(HTTP_X_COMPANY_ID=str(self.company.company_id))

    def test_profit_loss(self):
        response = self.client.get('/api/reports/profit-loss/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Revenue credit = 2000, Expense debit = 300, net_income = 2000 - 300
        self.assertEqual(data['revenue']['total_credit'], 2000)
        self.assertEqual(data['expense']['total_debit'], 300)
        self.assertEqual(data['net_income'], 1700)

    def test_balance_sheet(self):
        response = self.client.get('/api/reports/balance-sheet/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Asset balance sums chart_of_accounts balance (0)
        self.assertIn('assets', data)
        self.assertIn('liabilities', data)
        self.assertIn('equity', data)

    def test_cash_flow(self):
        response = self.client.get('/api/reports/cash-flow/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['inflow'], 2000)
        self.assertEqual(data['outflow'], -300)
