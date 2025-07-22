import { createRouter, createWebHistory } from 'vue-router';

// Import views
import DashboardView from '../views/dashboard/DashboardView.vue';

// Core data management
import CustomersView from '../views/customers/CustomersView.vue';
import VendorsView from '../views/vendors/VendorsView.vue';

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
  // Overview
  { path: '/', name: 'dashboard', component: DashboardView },
  
  // Core data management
  { path: '/customers', name: 'customers', component: CustomersView },
  { path: '/vendors', name: 'vendors', component: VendorsView },
  
  // Accounts receivable
  { path: '/invoices', name: 'invoices', component: InvoicesView },
  { path: '/payments-ar', name: 'payments-ar', component: PaymentsARView },
  
  // Accounts payable
  { path: '/bills', name: 'bills', component: BillsView },
  { path: '/payments-ap', name: 'payments-ap', component: PaymentsAPView },
  
  // Financial management
  { path: '/banking', name: 'banking', component: BankingView },
  { path: '/inventory', name: 'inventory', component: InventoryView },
  { path: '/payroll', name: 'payroll', component: PayrollView },
  
  // Projects management
  { path: '/projects', name: 'projects', component: ProjectsView },
  
  // Support functions
  { path: '/reports', name: 'reports', component: ReportsView },
  { path: '/documents', name: 'documents', component: DocumentsView },
  { path: '/subscriptions', name: 'subscriptions', component: SubscriptionsView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
