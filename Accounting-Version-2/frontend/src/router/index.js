import { createRouter, createWebHistory } from 'vue-router';
import authService from '@/services/authService';

// Authentication views
import LoginView from '../views/auth/LoginView.vue';
import ProfileView from '../views/ProfileView.vue';

// Import views
import DashboardView from '../views/DashboardView.vue';

// Core data management
import CustomersView from '../views/customers/CustomersView.vue';
import VendorsView from '../views/vendors/VendorsView.vue';

// Payments management
import PaymentsView from '../views/payments/PaymentsView.vue';

// Accounts receivable
import InvoicesView from '../views/invoicing/InvoicesView.vue';
import PaymentsARView from '../views/invoicing/PaymentsARView.vue';

// Accounts payable
import BillsView from '../views/bills/BillsView.vue';
import PaymentsAPView from '../views/bills/PaymentsAPView.vue';

// Financial management
import BankingView from '../views/banking/BankingView.vue';
import InventoryView from '../views/inventory/InventoryView.vue';
import PayrollView from '../views/payroll/PayrollView.vue';

// Projects management
import ProjectsView from '../views/projects/ProjectsView.vue';

// Support functions
import ReportsView from '../views/reports/ReportsView.vue';
import DocumentsView from '../views/admin/DocumentsView.vue';
import SubscriptionsView from '../views/settings/SubscriptionsView.vue';

const routes = [
  // Authentication routes (no auth required)
  { 
    path: '/login', 
    name: 'login', 
    component: LoginView,
    meta: { requiresAuth: false }
  },

  // User profile route
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  
  // Protected routes
  { 
    path: '/', 
    name: 'dashboard', 
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/dashboard', 
    redirect: '/',
    meta: { requiresAuth: true }
  },
  
  // User profile
  { 
    path: '/profile', 
    name: 'profile', 
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  
  // Core data management
  { 
    path: '/customers', 
    name: 'customers', 
    component: CustomersView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/vendors', 
    name: 'vendors', 
    component: VendorsView,
    meta: { requiresAuth: true }
  },
  
  // Payments management
  { 
    path: '/payments', 
    name: 'payments', 
    component: PaymentsView,
    meta: { requiresAuth: true }
  },
  
  // Accounts receivable
  { 
    path: '/invoices', 
    name: 'invoices', 
    component: InvoicesView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/payments-ar', 
    name: 'payments-ar', 
    component: PaymentsARView,
    meta: { requiresAuth: true }
  },
  
  // Accounts payable
  { 
    path: '/bills', 
    name: 'bills', 
    component: BillsView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/payments-ap', 
    name: 'payments-ap', 
    component: PaymentsAPView,
    meta: { requiresAuth: true }
  },
  
  // Financial management
  { 
    path: '/banking', 
    name: 'banking', 
    component: BankingView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/inventory', 
    name: 'inventory', 
    component: InventoryView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/payroll', 
    name: 'payroll', 
    component: PayrollView,
    meta: { requiresAuth: true }
  },
  
  // Projects management
  { 
    path: '/projects', 
    name: 'projects', 
    component: ProjectsView,
    meta: { requiresAuth: true }
  },
  
  // Support functions
  { 
    path: '/reports', 
    name: 'reports', 
    component: ReportsView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/documents', 
    name: 'documents', 
    component: DocumentsView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/subscriptions', 
    name: 'subscriptions', 
    component: SubscriptionsView,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false);
  const isAuthenticated = authService.isAuthenticated();

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login page with return url
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    });
  } else if (to.name === 'login' && isAuthenticated) {
    // If user is already logged in and tries to access login, redirect to dashboard
    next({ name: 'dashboard' });
  } else {
    next();
  }
});

export default router;
