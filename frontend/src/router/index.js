import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ReportsView from '../views/reports/ReportsView.vue'
import Login from '../components/Login.vue'
import Profile from '../views/Profile.vue'
import Settings from '../views/Settings.vue'
import PayrollView from '../views/payroll/PayrollView.vue'
import AuditLogList from '../views/AuditLogList.vue'
import Companies from '../views/accounts/Companies.vue'
import UserRoles from '../views/accounts/UserRoles.vue'
import GeneralLedger from '../views/reports/GeneralLedger.vue'
import Documents from '../views/documents/Documents.vue'
import ImportFiles from '../views/importer/ImportFiles.vue'
import Subscriptions from '../views/subscriptions/Subscriptions.vue'
import Employees from '../views/payroll/Employees.vue'
import Payrolls from '../views/payroll/Payrolls.vue'
import Paystubs from '../views/payroll/Paystubs.vue'
import Taxes from '../views/payroll/Taxes.vue'
import Deductions from '../views/payroll/Deductions.vue'
import Benefits from '../views/payroll/Benefits.vue'
import BankAccounts from '../views/banking/BankAccounts.vue'
import BankStatementLines from '../views/banking/BankStatementLines.vue'
import Reconciliations from '../views/banking/Reconciliations.vue'
import Invoices from '../views/payments/Invoices.vue'
import Bills from '../views/payments/Bills.vue'
import BalanceSheet from '../views/reports/BalanceSheet.vue'
import IncomeStatement from '../views/reports/IncomeStatement.vue'
import CashFlow from '../views/reports/CashFlow.vue'
import ProjectsView from '../views/projects/ProjectsView.vue'
import store from '../store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: ReportsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/payroll',
    name: 'Payroll',
    component: PayrollView,
    meta: { requiresAuth: true }
  },
  { path: '/accounts/companies', name: 'Companies', component: Companies, meta: { requiresAuth: true } },
  { path: '/accounts/user-roles', name: 'UserRoles', component: UserRoles, meta: { requiresAuth: true } },
  { path: '/reports/general-ledger', name: 'GeneralLedger', component: GeneralLedger, meta: { requiresAuth: true } },
  { path: '/documents', name: 'Documents', component: Documents, meta: { requiresAuth: true } },
  { path: '/importer', name: 'ImportFiles', component: ImportFiles, meta: { requiresAuth: true } },
  { path: '/subscriptions', name: 'Subscriptions', component: Subscriptions, meta: { requiresAuth: true } },
  { path: '/projects', name: 'Projects', component: ProjectsView, meta: { requiresAuth: true } },
  { path: '/payroll/employees', name: 'Employees', component: Employees, meta: { requiresAuth: true } },
  { path: '/payroll/payrolls', name: 'Payrolls', component: Payrolls, meta: { requiresAuth: true } },
  { path: '/payroll/paystubs', name: 'Paystubs', component: Paystubs, meta: { requiresAuth: true } },
  { path: '/payroll/taxes', name: 'Taxes', component: Taxes, meta: { requiresAuth: true } },
  { path: '/payroll/deductions', name: 'Deductions', component: Deductions, meta: { requiresAuth: true } },
  { path: '/payroll/benefits', name: 'Benefits', component: Benefits, meta: { requiresAuth: true } },
  { path: '/banking/accounts', name: 'BankAccounts', component: BankAccounts, meta: { requiresAuth: true } },
  { path: '/banking/statement-lines', name: 'BankStatementLines', component: BankStatementLines, meta: { requiresAuth: true } },
  { path: '/banking/reconciliations', name: 'Reconciliations', component: Reconciliations, meta: { requiresAuth: true } },
  { path: '/payments/invoices', name: 'Invoices', component: Invoices, meta: { requiresAuth: true } },
  { path: '/payments/bills', name: 'Bills', component: Bills, meta: { requiresAuth: true } },
  { path: '/reports/balance-sheet', name: 'BalanceSheet', component: BalanceSheet, meta: { requiresAuth: true } },
  { path: '/reports/income-statement', name: 'IncomeStatement', component: IncomeStatement, meta: { requiresAuth: true } },
  { path: '/reports/cash-flow', name: 'CashFlow', component: CashFlow, meta: { requiresAuth: true } },
  { path: '/audit-logs', name: 'AuditLogs', component: AuditLogList, meta: { requiresAuth: true, adminOnly: true } }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters.isLoggedIn
  const user = store.state.user
  
  // If route requires auth and user isn't logged in, redirect to login
  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next('/login')
  }
  // If going to login and already logged in, redirect to dashboard
  else if (to.path === '/login' && isLoggedIn) {
    next('/')
  }
  // Check if route is admin-only and user is not an admin
  else if (to.matched.some(record => record.meta.adminOnly) && !(user && (user.is_superuser || user.is_staff || user.role === 'admin'))) {
    // Redirect to dashboard if user doesn't have admin privileges
    next('/')
  }
  else {
    next()
  }
})

export default router
