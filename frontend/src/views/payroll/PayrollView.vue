<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Payroll Dashboard</h1>
        <p class="page-subtitle">Overview of payroll activities and quick actions.</p>
      </div>
      <div class="toolbar-group">
        <UiButton variant="primary" @click="$router.push('/payroll/employees')">
          Manage Employees
        </UiButton>
        <UiButton variant="outline" @click="$router.push('/payroll/payrolls')">
          Run Payroll
        </UiButton>
      </div>
    </header>

    <div class="dashboard-grid">
      <UiCard title="Quick Actions" class="quick-actions">
        <div class="action-buttons">
          <UiButton variant="primary" @click="$router.push('/payroll/employees')">
            <i class="icon-users"></i>
            Employees
          </UiButton>
          <UiButton variant="primary" @click="$router.push('/payroll/payrolls')">
            <i class="icon-payroll"></i>
            Payroll Runs
          </UiButton>
          <UiButton variant="primary" @click="$router.push('/payroll/paystubs')">
            <i class="icon-paystubs"></i>
            Paystubs
          </UiButton>
          <UiButton variant="primary" @click="$router.push('/payroll/taxes')">
            <i class="icon-taxes"></i>
            Taxes
          </UiButton>
          <UiButton variant="primary" @click="$router.push('/payroll/deductions')">
            <i class="icon-deductions"></i>
            Deductions
          </UiButton>
          <UiButton variant="primary" @click="$router.push('/payroll/benefits')">
            <i class="icon-benefits"></i>
            Benefits
          </UiButton>
        </div>
      </UiCard>

      <UiCard title="Recent Payroll Runs" subtitle="Latest payroll processing activities.">
        <div v-if="recentPayrolls.length" class="recent-list">
          <div v-for="payroll in recentPayrolls" :key="payroll.id" class="recent-item">
            <div class="item-info">
              <div class="item-title">{{ formatDate(payroll.run_date) }}</div>
              <div class="item-meta">{{ payroll.employee_count }} employees</div>
            </div>
            <UiStatusBadge :status="payroll.status === 'completed' ? 'success' : 'info'">
              {{ payroll.status }}
            </UiStatusBadge>
          </div>
        </div>
        <div v-else class="table-empty">No recent payroll runs.</div>
        <template #actions>
          <UiButton size="sm" variant="outline" @click="$router.push('/payroll/payrolls')">
            View All
          </UiButton>
        </template>
      </UiCard>

      <UiCard title="Payroll Summary" subtitle="Current period statistics.">
        <div class="summary-stats">
          <div class="stat-item">
            <div class="stat-value">{{ totalEmployees }}</div>
            <div class="stat-label">Active Employees</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ formatCurrency(totalPayroll) }}</div>
            <div class="stat-label">Total Payroll This Month</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ pendingPayrolls }}</div>
            <div class="stat-label">Pending Runs</div>
          </div>
        </div>
      </UiCard>

      <UiCard title="Upcoming Tasks" subtitle="Payroll tasks requiring attention.">
        <div class="tasks-list">
          <div class="task-item">
            <i class="icon-calendar"></i>
            <div class="task-info">
              <div class="task-title">Next Payroll Run</div>
              <div class="task-meta">Due in 5 days</div>
            </div>
          </div>
          <div class="task-item">
            <i class="icon-tax"></i>
            <div class="task-info">
              <div class="task-title">Tax Filing Deadline</div>
              <div class="task-meta">Quarterly taxes due soon</div>
            </div>
          </div>
          <div class="task-item">
            <i class="icon-compliance"></i>
            <div class="task-info">
              <div class="task-title">Compliance Check</div>
              <div class="task-meta">Review employee records</div>
            </div>
          </div>
        </div>
      </UiCard>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiStatusBadge from '@/components/ui/UiStatusBadge.vue';

export default {
  name: 'PayrollView',
  components: {
    UiButton,
    UiCard,
    UiStatusBadge,
  },
  data() {
    return {
      recentPayrolls: [],
      totalEmployees: 0,
      totalPayroll: 0,
      pendingPayrolls: 0,
    };
  },
  mounted() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      try {
        // Fetch recent payrolls
        const payrollsRes = await axios.get('/api/payroll/payrolls/?limit=5');
        this.recentPayrolls = payrollsRes.data.results || payrollsRes.data || [];

        // Fetch employee count
        const employeesRes = await axios.get('/api/payroll/employees/');
        this.totalEmployees = employeesRes.data.length || 0;

        // Mock data for now - replace with real API calls
        this.totalPayroll = 45000;
        this.pendingPayrolls = 2;
      } catch (error) {
        console.error('Error fetching payroll dashboard data:', error);
      }
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString();
    },
    formatCurrency(amount) {
      if (typeof amount !== 'number') return amount;
      return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
    },
  },
};
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.quick-actions .action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.recent-list .recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
}

.recent-list .recent-item:last-child {
  border-bottom: none;
}

.item-info .item-title {
  font-weight: 600;
  color: #2c3e50;
}

.item-info .item-meta {
  font-size: 0.9rem;
  color: #6c757d;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  text-align: center;
}

.stat-item .stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.stat-item .stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.tasks-list .task-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
}

.tasks-list .task-item:last-child {
  border-bottom: none;
}

.task-info .task-title {
  font-weight: 600;
  color: #2c3e50;
}

.task-info .task-meta {
  font-size: 0.9rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .summary-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>