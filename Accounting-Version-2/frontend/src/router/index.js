import { createRouter, createWebHistory } from 'vue-router';

import AccountsView from '../views/AccountsView.vue';
import BankingView from '../views/BankingView.vue';
import CoreView from '../views/CoreView.vue';
import DashboardView from '../views/DashboardView.vue';
import DocumentsView from '../views/DocumentsView.vue';
import ImporterView from '../views/ImporterView.vue';
import PaymentsAPView from '../views/PaymentsAPView.vue';
import PaymentsARView from '../views/PaymentsARView.vue';
import PayrollView from '../views/PayrollView.vue';
import ReportsView from '../views/ReportsView.vue';
import SubscriptionsView from '../views/SubscriptionsView.vue';

const routes = [
  { path: '/', name: 'dashboard', component: DashboardView },
  { path: '/accounts', name: 'accounts', component: AccountsView },
  { path: '/banking', name: 'banking', component: BankingView },
  { path: '/core', name: 'core', component: CoreView },
  { path: '/documents', name: 'documents', component: DocumentsView },
  { path: '/importer', name: 'importer', component: ImporterView },
  { path: '/payments-ap', name: 'payments-ap', component: PaymentsAPView },
  { path: '/payments-ar', name: 'payments-ar', component: PaymentsARView },
  { path: '/payroll', name: 'payroll', component: PayrollView },
  { path: '/reports', name: 'reports', component: ReportsView },
  { path: '/subscriptions', name: 'subscriptions', component: SubscriptionsView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
