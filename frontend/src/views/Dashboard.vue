<template>
  <div class="dashboard-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading your dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon" aria-hidden="true"></div>
      <p>{{ error }}</p>
      <button @click="refreshData" class="retry-btn">Try Again</button>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Welcome Header (refreshed styling) -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div class="welcome-text">
            <div class="welcome-title-row">
              <div class="title-copy">
                <div class="greeting">Good {{ timeOfDay }},</div>
                <div class="user-line">
                  <h1 class="user-name">{{ displayName }}</h1>
                </div>
                <p class="welcome-subtitle">Here's what's happening with your finances today</p>
              </div>
            </div>
          </div>

          <div class="company-info">
            <div class="company-badge">
              <div class="company-avatar">
                <img v-if="profilePhotoUrl" 
                     :src="profilePhotoUrl" 
                     :alt="displayName"
                     class="avatar-image" 
                     @error="$event.target.style.display='none'; $event.target.nextElementSibling.style.display='flex'" />
                <span class="avatar-initials" :style="profilePhotoUrl ? 'display: none' : ''">{{ userInitials }}</span>
              </div>
              <div class="company-details">
                <span class="company-name">{{ companyName }}</span>
                <span class="company-role">{{ userRole }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Metrics Cards -->
      <div class="metrics-grid">
        <div class="metric-card revenue-card" @click="navigateTo('/reports/income-statement')">
          <div class="metric-icon" aria-hidden="true"></div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.revenue.value) }}</div>
            <div class="metric-label">{{ metrics.revenue.label }}</div>
              <div class="metric-change" :class="metrics.revenue.change >= 0 ? 'positive' : 'negative'">
              <span class="change-icon" aria-hidden="true">{{ metrics.revenue.change >= 0 ? '\u25B2' : '\u25BC' }}</span>
              <span class="change-value">{{ formatChange(metrics.revenue.change) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
        </div>

        <div class="metric-card expense-card" @click="navigateTo('/reports/expense-report')">
          <div class="metric-icon" aria-hidden="true"></div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.expenses.value) }}</div>
            <div class="metric-label">{{ metrics.expenses.label }}</div>
              <div class="metric-change" :class="metrics.expenses.change <= 0 ? 'positive' : 'negative'">
              <span class="change-icon" aria-hidden="true">{{ metrics.expenses.change <= 0 ? '\u25BC' : '\u25B2' }}</span>
              <span class="change-value">{{ formatChange(Math.abs(metrics.expenses.change)) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon" aria-hidden="true"></i>
          </div>
        </div>

        <div class="metric-card profit-card" @click="navigateTo('/reports/profit-loss')">
          <div class="metric-icon" aria-hidden="true"></div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.profit.value) }}</div>
            <div class="metric-label">{{ metrics.profit.label }}</div>
              <div class="metric-change" :class="metrics.profit.change >= 0 ? 'positive' : 'negative'">
              <span class="change-icon" aria-hidden="true">{{ metrics.profit.change >= 0 ? '\u25B2' : '\u25BC' }}</span>
              <span class="change-value">{{ formatChange(metrics.profit.change) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon" aria-hidden="true"></i>
          </div>
        </div>

        <div class="metric-card cashflow-card" @click="navigateTo('/reports/cash-flow')">
          <div class="metric-icon" aria-hidden="true"></div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.cash_flow.value) }}</div>
            <div class="metric-label">{{ metrics.cash_flow.label }}</div>
              <div class="metric-change" :class="metrics.cash_flow.change >= 0 ? 'positive' : 'negative'">
              <span class="change-icon" aria-hidden="true">{{ metrics.cash_flow.change >= 0 ? '\u25B2' : '\u25BC' }}</span>
              <span class="change-value">{{ formatChange(metrics.cash_flow.change) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon" aria-hidden="true"></i>
          </div>
        </div>
      </div>

    <!-- Quick Actions & Recent Activity -->
    <div class="dashboard-grid">
      <!-- Quick Actions Panel -->
      <div class="dashboard-panel quick-actions-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon" aria-hidden="true"></i>
            Quick Actions
          </h3>
        </div>
        <div class="quick-actions">
          <button class="action-btn invoice-btn" @click="navigateTo('/payments/invoices')">
            <div class="action-star" aria-hidden="true">⭐</div>
            <div class="btn-content">
              <div class="btn-title">Create Invoice</div>
              <div class="btn-subtitle">Send to customers</div>
            </div>
          </button>
          
          <button class="action-btn expense-btn" @click="navigateTo('/payments/bills')">
            <div class="action-star" aria-hidden="true">⭐</div>
            <div class="btn-content">
              <div class="btn-title">Add Expense</div>
              <div class="btn-subtitle">Track spending</div>
            </div>
          </button>
          
          <button class="action-btn customer-btn" @click="navigateTo('/accounts/customers')">
            <div class="action-star" aria-hidden="true">⭐</div>
            <div class="btn-content">
              <div class="btn-title">Add Customer</div>
              <div class="btn-subtitle">Grow your base</div>
            </div>
          </button>
          
          <button class="action-btn reconcile-btn" @click="navigateTo('/banking/reconciliations')">
            <div class="action-star" aria-hidden="true">⭐</div>
            <div class="btn-content">
              <div class="btn-title">Reconcile Bank</div>
              <div class="btn-subtitle">Balance accounts</div>
            </div>
          </button>
          
          <button class="action-btn report-btn" @click="navigateTo('/reports')">
            <div class="action-star" aria-hidden="true">⭐</div>
            <div class="btn-content">
              <div class="btn-title">Generate Report</div>
              <div class="btn-subtitle">View insights</div>
            </div>
          </button>
          
          <button class="action-btn payroll-btn" @click="navigateTo('/payroll')">
            <div class="action-star" aria-hidden="true">⭐</div>
            <div class="btn-content">
              <div class="btn-title">Run Payroll</div>
              <div class="btn-subtitle">Pay employees</div>
            </div>
          </button>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="dashboard-panel activity-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon" aria-hidden="true"></i>
            Recent Activity
          </h3>
          <button class="panel-action" @click="navigateTo('/reports/general-ledger')">
            View All
          </button>
        </div>
        <div class="activity-list">
          <div class="activity-item" v-for="activity in recentActivities" :key="activity.id" :class="activity.amountType">
            <div class="activity-icon" :class="activity.type" aria-hidden="true"></div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-details">{{ activity.details }}</div>
              <div class="activity-time">{{ formatActivityDate(activity.time) }}</div>
            </div>
            <div class="activity-amount" :class="activity.amountType">
              {{ formatSignedCurrency(activity.amount) }}
            </div>
          </div>
          
          <!-- Add sample activity when no data -->
          <div v-if="recentActivities.length === 0" class="sample-activities">
            <div class="activity-item positive">
              <div class="activity-icon income" aria-hidden="true"></div>
              <div class="activity-content">
                <div class="activity-title">Office supplies purchase</div>
                <div class="activity-details">Account: Office Supplies</div>
                <div class="activity-time">Sep 29, 2025</div>
              </div>
              <div class="activity-amount positive">+$50</div>
            </div>
            
            <div class="activity-item positive">
              <div class="activity-icon income" aria-hidden="true"></div>
              <div class="activity-content">
                <div class="activity-title">Product sale</div>
                <div class="activity-details">Account: Sales Revenue</div>
                <div class="activity-time">Sep 29, 2025</div>
              </div>
              <div class="activity-amount positive">+$500</div>
            </div>
            
            <div class="activity-item positive">
              <div class="activity-icon income" aria-hidden="true"></div>
              <div class="activity-content">
                <div class="activity-title">Initial cash deposit</div>
                <div class="activity-details">Account: Cash</div>
                <div class="activity-time">Sep 28, 2025</div>
              </div>
              <div class="activity-amount positive">+$1,000</div>
            </div>
            
            <div class="activity-item negative">
              <div class="activity-icon expense" aria-hidden="true"></div>
              <div class="activity-content">
                <div class="activity-title">Monthly rent payment</div>
                <div class="activity-details">Account: Rent Expense</div>
                <div class="activity-time">Sep 28, 2025</div>
              </div>
              <div class="activity-amount negative">-$1,200</div>
            </div>
            
            <div class="activity-item negative">
              <div class="activity-content">
                <div class="activity-title">Utility bill payment</div>
                <div class="activity-details">Account: Utilities</div>
                <div class="activity-time">Sep 27, 2025</div>
              </div>
              <div class="activity-amount negative">-$150</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Items -->
      <div class="dashboard-panel pending-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon" aria-hidden="true"></i>
            Pending Items
          </h3>
        </div>
        <div class="pending-list">
          <div class="pending-item" v-for="item in pendingItems" :key="item.id" @click="navigateTo(item.link)">
            <div class="pending-icon" :class="item.type">
              {{ item.icon }}
            </div>
            <div class="pending-content">
              <div class="pending-title">{{ item.title }}</div>
              <div class="pending-subtitle">{{ item.subtitle }}</div>
            </div>
            <div class="pending-badge">
              {{ item.count }}
            </div>
          </div>
          
          <!-- Add some sample pending items when no data -->
          <div v-if="pendingItems.length === 0" class="sample-pending-items">
            <div class="pending-item" @click="navigateTo('/payments/invoices')">
              <div class="pending-icon invoice">INV</div>
              <div class="pending-content">
                <div class="pending-title">Overdue Invoices</div>
                <div class="pending-subtitle">Require follow-up</div>
              </div>
              <div class="pending-badge">3</div>
            </div>
            
            <div class="pending-item" @click="navigateTo('/payments/bills')">
              <div class="pending-icon bill">BIL</div>
              <div class="pending-content">
                <div class="pending-title">Pending Bills</div>
                <div class="pending-subtitle">Ready for payment</div>
              </div>
              <div class="pending-badge">7</div>
            </div>
            
            <div class="pending-item" @click="navigateTo('/banking/reconciliations')">
              <div class="pending-icon reconciliation">REC</div>
              <div class="pending-content">
                <div class="pending-title">Bank Reconciliation</div>
                <div class="pending-subtitle">Needs attention</div>
              </div>
              <div class="pending-badge">2</div>
            </div>
            
            <div class="pending-item" @click="navigateTo('/reports/general-ledger')">
              <div class="pending-icon expense">EXP</div>
              <div class="pending-content">
                <div class="pending-title">Expense Reports</div>
                <div class="pending-subtitle">Awaiting approval</div>
              </div>
              <div class="pending-badge">5</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Financial Health Score -->
      <div class="dashboard-panel health-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon" aria-hidden="true"></i>
            Financial Health
          </h3>
        </div>
        <div class="health-content">
          <div class="health-score">
            <div class="score-circle" :class="getHealthScoreClass()">
              <div class="score-value">{{ financialHealth.score || 100 }}</div>
              <div class="score-label">Score</div>
            </div>
          </div>
          <div class="health-metrics">
            <div 
              v-for="(value, key) in financialHealth.metrics" 
              :key="key"
              class="health-metric"
            >
              <div class="health-metric-icon">{{ getHealthMetricIcon(key) }}</div>
              <div class="health-metric-content">
                <div class="health-metric-label">{{ getHealthMetricLabel(key) }}</div>
                <div class="health-metric-value">{{ formatHealthMetric(key, value) }}</div>
              </div>
            </div>
            
            <!-- Add sample metrics when no data -->
            <div v-if="Object.keys(financialHealth.metrics).length === 0" class="sample-metrics">
              <div class="health-metric">
                <div class="health-metric-content">
                  <div class="health-metric-label">Profit Margin</div>
                  <div class="health-metric-value">90%</div>
                </div>
              </div>
              
              <div class="health-metric">
                <div class="health-metric-content">
                  <div class="health-metric-label">Debt Ratio</div>
                  <div class="health-metric-value">0%</div>
                </div>
              </div>
              
              <div class="health-metric">
                <div class="health-metric-content">
                  <div class="health-metric-label">Cash Position</div>
                  <div class="health-metric-value">$1,000</div>
                </div>
              </div>
              
              <div class="health-metric">
                <div class="health-metric-content">
                  <div class="health-metric-label">Revenue Growth</div>
                  <div class="health-metric-value">12.5%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    </div> <!-- End of Dashboard Content (v-else) -->
  </div> <!-- End of dashboard-container -->
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import axios from 'axios';

export default {
  name: 'DashboardView',
  data() {
    return {
      loading: true,
      error: null,
      metrics: {
        revenue: { value: 0, change: 0, label: 'Monthly Revenue' },
        expenses: { value: 0, change: 0, label: 'Monthly Expenses' },
        profit: { value: 0, change: 0, label: 'Net Profit' },
        cash_flow: { value: 0, change: 0, label: 'YTD Cash Flow' }
      },
      recentActivities: [],
      pendingItems: [],
      financialHealth: {
        score: 0,
        status: 'good',
        metrics: {
          profit_margin: 0,
          debt_ratio: 0,
          cash_position: 0,
          revenue_growth: 0
        }
      },
      activeCompany: null,
      userRole: 'Administrator'
    };
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['isLoggedIn']),
    displayName() {
      if (!this.user) return 'User';
      const userData = this.user.user || this.user;
      if (userData.first_name && userData.last_name) {
        return `${userData.first_name} ${userData.last_name}`;
      } else if (userData.first_name) {
        return userData.first_name;
      } else {
        return userData.username || 'User';
      }
    },
    profilePhotoUrl() {
      return this.user?.profile_photo || this.user?.user?.profile_photo || '';
    },
    userInitials() {
      const userData = this.user?.user || this.user;
      if (userData?.first_name && userData?.last_name) {
        return `${userData.first_name.charAt(0)}${userData.last_name.charAt(0)}`.toUpperCase();
      } else if (userData?.first_name) {
        return userData.first_name.charAt(0).toUpperCase();
      } else if (userData?.username) {
        return userData.username.charAt(0).toUpperCase();
      } else {
        return 'U';
      }
    },
    timeOfDay() {
      const hour = new Date().getHours();
      if (hour < 12) return 'morning';
      if (hour < 17) return 'afternoon';
      return 'evening';
    },
    companyName() {
      if (this.user && this.user.company_roles && this.user.company_roles.length > 0) {
        return this.user.company_roles[0].company.name
      }
      return 'Your Company'
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true;
        
        // Load all dashboard data in parallel
        const [metricsRes, activityRes, pendingRes, healthRes] = await Promise.all([
          this.fetchMetrics(),
          this.fetchActivity(),
          this.fetchPending(),
          this.fetchFinancialHealth()
        ]);
        
        this.metrics = metricsRes.data;
        this.recentActivities = activityRes.data.map(activity => ({
          ...activity,
          // normalize amount to number
          amount: Number(activity.amount) || 0,
          amountType: Number(activity.amount) > 0 ? 'positive' : (Number(activity.amount) < 0 ? 'negative' : 'neutral')
        }));
        this.pendingItems = pendingRes.data.map(item => ({
          ...item,
          icon: this.getPendingIcon(item.type),
          count: '1'
        }));
        this.financialHealth = healthRes.data;
        
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        this.error = 'Failed to load dashboard data. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    
    async fetchMetrics() {
      return await axios.get('/api/accounts/dashboard/metrics/');
    },
    
    async fetchActivity() {
      return await axios.get('/api/accounts/dashboard/activity/');
    },
    
    async fetchPending() {
      return await axios.get('/api/accounts/dashboard/pending/');
    },
    
    async fetchFinancialHealth() {
      return await axios.get('/api/accounts/dashboard/health/');
    },
    
    formatCurrency(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(Math.abs(value));
    },

    formatSignedCurrency(value) {
      const num = Number(value) || 0;
      const sign = num > 0 ? '+' : (num < 0 ? '-' : '');
      const abs = Math.abs(num);
      return `${sign}${new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(abs)}`;
    },

    formatActivityDate(datetime) {
      // If datetime is already a Date or ISO string, try to parse and format like 'May 5, 2025'
      const d = datetime ? new Date(datetime) : null;
      if (!d || isNaN(d.getTime())) return '';
      return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    },
    
    formatChange(change) {
      const sign = change >= 0 ? '+' : '';
      return `${sign}${change.toFixed(1)}%`;
    },
    
    getActivityIcon(type) {
      const labels = {
        income: 'INC',
        expense: 'EXP',
        invoice: 'INV',
        bank: 'BNK'
      };
      return labels[type] || 'ACT';
    },
    
    getPendingIcon(type) {
      const labels = {
        invoice: 'INV',
        bill: 'BIL',
        payment: 'PAY',
        reconciliation: 'REC'
      };
      return labels[type] || 'PND';
    },
    
    getCompanyInitials(name) {
      if (!name) return 'C';
      return name.split(' ')
        .map(word => word.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2);
    },
    
    getHealthScoreClass(score = this.financialHealth.score) {
      if (score >= 80) return 'excellent';
      if (score >= 60) return 'good';
      if (score >= 40) return 'fair';
      return 'poor';
    },
    
    getHealthMetricIcon(metric) {
      const labels = {
        profit_margin: 'PM',
        debt_ratio: 'DR',
        cash_position: 'CP',
        revenue_growth: 'RG'
      };
      return labels[metric] || 'HM';
    },
    
    getHealthMetricLabel(metric) {
      const labels = {
        profit_margin: 'Profit Margin',
        debt_ratio: 'Debt Ratio',
        cash_position: 'Cash Position',
        revenue_growth: 'Revenue Growth'
      };
      return labels[metric] || metric;
    },
    
    formatHealthMetric(key, value) {
      switch (key) {
        case 'profit_margin':
        case 'debt_ratio':
        case 'revenue_growth':
          return `${value}%`;
        case 'cash_position':
          return this.formatCurrency(value);
        default:
          return value;
      }
    },
    
    navigateTo(path) {
      this.$router.push(path);
    },
    
    navigateToAction(action) {
      const routes = {
        'create-invoice': '/payments/invoices',
        'add-expense': '/reports/general-ledger',
        'bank-reconciliation': '/banking/reconciliations',
        'generate-report': '/reports'
      };
      
      if (routes[action]) {
        this.$router.push(routes[action]);
      }
    },
    
    viewAllActivity() {
      this.$router.push('/reports/general-ledger');
    },
    
    viewAllPending() {
      this.$router.push('/dashboard/pending');
    },
    
    async refreshData() {
      await this.loadDashboardData();
    }
  },
  
  async mounted() {
    await this.loadDashboardData();
  }
};
</script>

<style scoped>
/* Dashboard Container */
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #6c757d;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #dc3545;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.3s ease;
}

.retry-btn:hover {
  background: #0056b3;
}

/* Welcome Section */
.welcome-section {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.welcome-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
  width: 100%;
  flex-wrap: wrap;
  gap: 1rem;
}

.welcome-text {
  flex: 1;
  min-width: 0;
  max-width: none;
}

.welcome-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  width: 100%;
}

.welcome-title-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-line {
  display: flex;
  align-items: center;
  gap: 12px;
}

.greeting {
  font-size: 1.1rem;
  font-weight: 400;
  opacity: 0.9;
}

.user-name {
  color: white;
  white-space: nowrap;
  overflow: visible;
  text-overflow: unset;
  display: inline-block;
  max-width: none;
  width: auto;
}

.welcome-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

.company-badge {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.company-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  overflow: hidden;
  position: relative;
}

.company-avatar .avatar-image {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.company-avatar .avatar-initials {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  color: white;
}

.company-details {
  display: flex;
  flex-direction: column;
  color: white;
}

.company-name {
  font-weight: 600;
  font-size: 1.1rem;
}

.company-role {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
  align-items: start;
}

.metric-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  transition: transform 220ms ease, box-shadow 220ms ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border: 1px solid #f0f0f0;
  /* subtle blue left accent matching the logo color (#007bff) */
  border-left: 4px solid rgba(0, 123, 255, 0.693);
  padding-left: calc(1rem + 8px);
  box-shadow: 0 6px 18px rgba(15,23,42,0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.metric-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 40px rgba(15,23,42,0.2);
}


/* Remove colored top bars and simplify metric cards to centered wording */
.metric-card::before {
  display: none;
}


.metric-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-align: center;
  justify-content: center;
}

.metric-icon { display: none; }

.metric-content {
  flex: none;
}


.metric-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: #16324a; /* stronger contrast */
  margin: 0 0 6px 0;
}

.metric-label {
  font-size: 0.95rem;
  color: #566474;
  margin-top: 4px;
}

/* subtle accent pill top-left for each metric card to help legibility on white */
.metric-card::after { display: none; }

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
}

.metric-change.positive {
  color: #28a745;
}

.metric-change.negative {
  color: #dc3545;
}

.change-icon {
  font-size: 0.8rem;
}

.change-value {
  font-weight: 600;
}

.change-period {
  color: #6c757d;
}

.metric-action {
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 1.2rem;
  color: #6c757d;
}

.metric-card:hover .metric-action {
  opacity: 1;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  align-items: start; /* Align panels to top but allow natural height growth */
}

.dashboard-panel {
  background: rgba(233, 228, 228, 0.316); /* soft opaque blue tint */
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  background: #007bff;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.panel-icon {
  font-size: 1.2rem;
}

.panel-action {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
}

.panel-action:hover {
  text-decoration: underline;
}

/* Quick Actions */
.quick-actions {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  border: 2px solid transparent;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  border-color: #e3f2fd;
}

/* .btn-icon removed — quick action icons intentionally hidden */
.btn-icon { display: none; }

.btn-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.btn-subtitle {
  font-size: 0.85rem;
  color: #6c757d;
}

/* Star for quick actions */
.action-star {
  font-size: 1.3rem;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}

/* Recent Activity */
.activity-list {
  padding: 1.5rem;
  /* Remove max-height to allow natural expansion */
  overflow-y: visible;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.9rem 0.75rem;
  border-radius: 8px;
  background: linear-gradient(135deg, #ffffff, #fbfdff);
  border: 1px solid #f0f0f0;
  box-shadow: 0 3px 10px rgba(15,23,42,0.03);
}

.activity-item:last-child {
  margin-bottom: 0.25rem;
}

/* Use a plain star emoji as the icon; no colored square behind it */
.activity-icon {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-right: 8px;
  background: transparent !important;
  border-radius: 0 !important;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.activity-details {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.85rem;
  color: #8a9198;
  margin-top: 6px;
}

.activity-amount {
  font-weight: 600;
  font-size: 0.95rem;
}

.activity-amount.positive {
  color: #28a745;
}

.activity-amount.negative {
  color: #dc3545;
}

.activity-amount.neutral {
  color: #6c757d;
}

/* Row highlights for credits (positive) and debits (negative) */
.activity-item.positive {
  border-left: 4px solid rgba(40,167,69,0.9);
}
.activity-item.negative {
  border-left: 4px solid rgba(220,53,69,0.9);
}
.activity-list .activity-item + .activity-item {
  margin-top: 8px;
}

/* Pending Items */
.pending-list {
  padding: 1.5rem;
}

.pending-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #f0f0f0;
  background: linear-gradient(135deg, #ffffff, #fbfdff);
  box-shadow: 0 3px 10px rgba(15,23,42,0.04);
}

.pending-item:hover {
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  transform: translateX(4px);
}

.pending-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
}

.pending-content {
  flex: 1;
}

.pending-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.pending-subtitle {
  font-size: 0.85rem;
  color: #6c757d;
}

.pending-badge {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

/* Financial Health */
.health-content {
  padding: 1.5rem;
}

.health-score {
  text-align: center;
  margin-bottom: 1.5rem;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
  border: 6px solid;
}

.score-circle.excellent {
  border-color: #28a745;
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
}

.score-circle.good {
  border-color: #17a2b8;
  background: linear-gradient(135deg, #d1ecf1, #bee5eb);
}

.score-circle.fair {
  border-color: #ffc107;
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
}

.score-circle.poor {
  border-color: #dc3545;
  background: linear-gradient(135deg, #f8d7da, #f1b0b7);
}

.score-value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.score-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.health-metrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}


.health-metric {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: transparent;
  border-radius: 6px;
  border: none;
  justify-content: center;
  text-align: center;
}

.health-metric-icon { display: none; }

.health-metric-content {
  flex: 1;
}

.health-metric-label {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.health-metric-value {
  font-weight: 600;
  color: #2c3e50;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .welcome-content {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .welcome-title {
    font-size: 1.8rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .action-btn {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}

@media (max-width: 480px) {
  .welcome-section {
    padding: 1.5rem;
  }
  
  .welcome-title {
    font-size: 1.5rem;
  }
  
  .metric-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    /* keep the left accent visible but a bit thinner on very small screens */
    border-left-width: 3px;
    padding-left: calc(1rem + 6px);
  }
  
  .company-badge {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .health-metrics {
    gap: 0.75rem;
  }
  
  .score-circle {
    width: 100px;
    height: 100px;
  }
  
  .score-value {
    font-size: 1.5rem;
  }
}
</style>
