<template>
  <div class="dashboard-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading your dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button @click="refreshData" class="retry-btn">Try Again</button>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Welcome Header -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div class="welcome-text">
            <h1 class="welcome-title">
              <span class="greeting">Good {{ timeOfDay }},</span>
              <span class="user-name">{{ displayName }}! 👋</span>
            </h1>
            <p class="welcome-subtitle">Here's what's happening with your finances today</p>
          </div>
          <div class="company-info">
            <div class="company-badge">
              <div class="company-avatar">
                {{ getCompanyInitials(companyName) }}
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
          <div class="metric-icon">💰</div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.revenue.value) }}</div>
            <div class="metric-label">{{ metrics.revenue.label }}</div>
            <div class="metric-change" :class="metrics.revenue.change >= 0 ? 'positive' : 'negative'">
              <span class="change-icon">{{ metrics.revenue.change >= 0 ? '📈' : '📉' }}</span>
              <span class="change-value">{{ formatChange(metrics.revenue.change) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon">👁️</i>
          </div>
        </div>

        <div class="metric-card expense-card" @click="navigateTo('/core/bills')">
          <div class="metric-icon">📊</div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.expenses.value) }}</div>
            <div class="metric-label">{{ metrics.expenses.label }}</div>
            <div class="metric-change" :class="metrics.expenses.change <= 0 ? 'positive' : 'negative'">
              <span class="change-icon">{{ metrics.expenses.change <= 0 ? '📉' : '📈' }}</span>
              <span class="change-value">{{ formatChange(Math.abs(metrics.expenses.change)) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon">👁️</i>
          </div>
        </div>

        <div class="metric-card profit-card">
          <div class="metric-icon">💎</div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.profit.value) }}</div>
            <div class="metric-label">{{ metrics.profit.label }}</div>
            <div class="metric-change" :class="metrics.profit.change >= 0 ? 'positive' : 'negative'">
              <span class="change-icon">{{ metrics.profit.change >= 0 ? '📈' : '📉' }}</span>
              <span class="change-value">{{ formatChange(metrics.profit.change) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon">👁️</i>
          </div>
        </div>

        <div class="metric-card cashflow-card" @click="navigateTo('/reports/cash-flow')">
          <div class="metric-icon">🌊</div>
          <div class="metric-content">
            <div class="metric-value">{{ formatCurrency(metrics.cash_flow.value) }}</div>
            <div class="metric-label">{{ metrics.cash_flow.label }}</div>
            <div class="metric-change" :class="metrics.cash_flow.change >= 0 ? 'positive' : 'negative'">
              <span class="change-icon">{{ metrics.cash_flow.change >= 0 ? '💹' : '⬇️' }}</span>
              <span class="change-value">{{ formatChange(metrics.cash_flow.change) }}</span>
              <span class="change-period">vs last month</span>
            </div>
          </div>
          <div class="metric-action">
            <i class="action-icon">👁️</i>
          </div>
        </div>
      </div>

    <!-- Quick Actions & Recent Activity -->
    <div class="dashboard-grid">
      <!-- Quick Actions Panel -->
      <div class="dashboard-panel quick-actions-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon">⚡</i>
            Quick Actions
          </h3>
        </div>
        <div class="quick-actions">
          <button class="action-btn invoice-btn" @click="navigateTo('/core/invoices')">
            <div class="btn-icon">🧾</div>
            <div class="btn-content">
              <div class="btn-title">Create Invoice</div>
              <div class="btn-subtitle">Send to customers</div>
            </div>
          </button>
          
          <button class="action-btn expense-btn" @click="navigateTo('/core/bills')">
            <div class="btn-icon">💸</div>
            <div class="btn-content">
              <div class="btn-title">Add Expense</div>
              <div class="btn-subtitle">Track spending</div>
            </div>
          </button>
          
          <button class="action-btn customer-btn" @click="navigateTo('/core/customers')">
            <div class="btn-icon">👤</div>
            <div class="btn-content">
              <div class="btn-title">Add Customer</div>
              <div class="btn-subtitle">Grow your base</div>
            </div>
          </button>
          
          <button class="action-btn reconcile-btn" @click="navigateTo('/banking/reconciliations')">
            <div class="btn-icon">⚖️</div>
            <div class="btn-content">
              <div class="btn-title">Reconcile Bank</div>
              <div class="btn-subtitle">Balance accounts</div>
            </div>
          </button>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="dashboard-panel activity-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon">🕒</i>
            Recent Activity
          </h3>
          <button class="panel-action" @click="navigateTo('/core/general-ledger')">
            View All
          </button>
        </div>
        <div class="activity-list">
          <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
            <div class="activity-icon" :class="activity.type">
              {{ activity.icon }}
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-details">{{ activity.details }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
            <div class="activity-amount" :class="activity.amountType">
              {{ activity.amount }}
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Items -->
      <div class="dashboard-panel pending-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon">⏳</i>
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
        </div>
      </div>

      <!-- Financial Health Score -->
      <div class="dashboard-panel health-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon">💊</i>
            Financial Health
          </h3>
        </div>
        <div class="health-content">
          <div class="health-score">
            <div class="score-circle" :class="getHealthScoreClass()">
              <div class="score-value">{{ financialHealth.score }}</div>
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
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-section">
      <!-- Revenue Trend Chart -->
      <div class="chart-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon">📈</i>
            Revenue Trend
          </h3>
          <div class="chart-period">
            <button class="period-btn active">6M</button>
            <button class="period-btn">1Y</button>
            <button class="period-btn">2Y</button>
          </div>
        </div>
        <div class="chart-container">
          <div class="chart-placeholder">
            <div class="chart-bars">
              <div class="chart-bar" style="height: 40%"></div>
              <div class="chart-bar" style="height: 65%"></div>
              <div class="chart-bar" style="height: 55%"></div>
              <div class="chart-bar" style="height: 80%"></div>
              <div class="chart-bar" style="height: 70%"></div>
              <div class="chart-bar" style="height: 90%"></div>
            </div>
            <div class="chart-legend">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Expense Breakdown -->
      <div class="chart-panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <i class="panel-icon">🥧</i>
            Expense Breakdown
          </h3>
        </div>
        <div class="chart-container">
          <div class="expense-breakdown">
            <div class="expense-item">
              <div class="expense-color" style="background: #007bff;"></div>
              <div class="expense-label">Operating</div>
              <div class="expense-value">45%</div>
            </div>
            <div class="expense-item">
              <div class="expense-color" style="background: #28a745;"></div>
              <div class="expense-label">Marketing</div>
              <div class="expense-value">25%</div>
            </div>
            <div class="expense-item">
              <div class="expense-color" style="background: #ffc107;"></div>
              <div class="expense-label">Staff</div>
              <div class="expense-value">20%</div>
            </div>
            <div class="expense-item">
              <div class="expense-color" style="background: #dc3545;"></div>
              <div class="expense-label">Other</div>
              <div class="expense-value">10%</div>
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
      chartData: {
        revenue_trend: [],
        expense_breakdown: []
      },
      currentPeriod: 'month',
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
      const userData = this.user?.user || this.user;
      return userData?.profile_photo || '';
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
        const [metricsRes, activityRes, pendingRes, healthRes, chartsRes] = await Promise.all([
          this.fetchMetrics(),
          this.fetchActivity(),
          this.fetchPending(),
          this.fetchFinancialHealth(),
          this.fetchCharts()
        ]);
        
        this.metrics = metricsRes.data;
        this.recentActivities = activityRes.data.map(activity => ({
          ...activity,
          icon: this.getActivityIcon(activity.type),
          amountType: activity.amount > 0 ? 'positive' : 'negative'
        }));
        this.pendingItems = pendingRes.data.map(item => ({
          ...item,
          icon: this.getPendingIcon(item.type),
          count: '1'
        }));
        this.financialHealth = healthRes.data;
        this.chartData = chartsRes.data;
        
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
    
    async fetchCharts() {
      return await axios.get('/api/accounts/dashboard/charts/');
    },
    
    formatCurrency(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(Math.abs(value));
    },
    
    formatChange(change) {
      const sign = change >= 0 ? '+' : '';
      return `${sign}${change.toFixed(1)}%`;
    },
    
    getActivityIcon(type) {
      const icons = {
        income: '💰',
        expense: '💸',
        invoice: '🧾',
        bank: '🏦'
      };
      return icons[type] || '📊';
    },
    
    getPendingIcon(type) {
      const icons = {
        invoice: '📋',
        bill: '💸',
        payment: '💳',
        reconciliation: '⚖️'
      };
      return icons[type] || '⏰';
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
      const icons = {
        profit_margin: '📈',
        debt_ratio: '⚖️',
        cash_position: '💰',
        revenue_growth: '📊'
      };
      return icons[metric] || '📋';
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
        'create-invoice': '/core/invoices',
        'add-expense': '/core/general-ledger',
        'bank-reconciliation': '/banking/reconciliations',
        'generate-report': '/reports'
      };
      
      if (routes[action]) {
        this.$router.push(routes[action]);
      }
    },
    
    viewAllActivity() {
      this.$router.push('/core/general-ledger');
    },
    
    viewAllPending() {
      this.$router.push('/dashboard/pending');
    },
    
    changePeriod(period) {
      this.currentPeriod = period;
      // Refresh chart data for new period
      this.fetchCharts();
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.greeting {
  font-size: 1.1rem;
  font-weight: 400;
  opacity: 0.9;
}

.user-name {
  background: linear-gradient(45deg, #fff, #e3f2fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  background: linear-gradient(135deg, #fff, #e3f2fd);
  color: #1565c0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
}

.company-details {
  display: flex;
  flex-direction: column;
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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.revenue-card::before {
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
}

.expense-card::before {
  background: linear-gradient(90deg, #FF9800, #FFC107);
}

.profit-card::before {
  background: linear-gradient(90deg, #2196F3, #03A9F4);
}

.cashflow-card::before {
  background: linear-gradient(90deg, #9C27B0, #E91E63);
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.metric-label {
  font-size: 0.95rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}

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
}

.dashboard-panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
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

.btn-icon {
  font-size: 1.8rem;
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
}

.btn-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.btn-subtitle {
  font-size: 0.85rem;
  color: #6c757d;
}

/* Recent Activity */
.activity-list {
  padding: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.activity-icon.income {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
}

.activity-icon.expense {
  background: linear-gradient(135deg, #f8d7da, #f1b0b7);
}

.activity-icon.invoice {
  background: linear-gradient(135deg, #d1ecf1, #bee5eb);
}

.activity-icon.bank {
  background: linear-gradient(135deg, #e2e3e5, #d6d8db);
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
  font-size: 0.8rem;
  color: #adb5bd;
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
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  border-radius: 10px;
  border: 1px solid #f0f0f0;
}

.health-metric-icon {
  font-size: 1.5rem;
  width: 35px;
  text-align: center;
}

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

/* Charts Section */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.chart-panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.chart-period {
  display: flex;
  gap: 0.5rem;
}

.period-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e9ecef;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.period-btn.active,
.period-btn:hover {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.chart-container {
  padding: 1.5rem;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chart-bars {
  display: flex;
  align-items: end;
  gap: 1rem;
  height: 150px;
  padding: 0 1rem;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(0deg, #007bff, #40a9ff);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  transition: all 0.3s ease;
}

.chart-bar:hover {
  background: linear-gradient(0deg, #0056b3, #1890ff);
  transform: scaleY(1.1);
}

.chart-legend {
  display: flex;
  justify-content: space-between;
  padding: 0 1rem;
  font-size: 0.85rem;
  color: #6c757d;
}

.expense-breakdown {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.expense-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  border-radius: 10px;
  border: 1px solid #f0f0f0;
}

.expense-color {
  width: 20px;
  height: 20px;
  border-radius: 4px;
}

.expense-label {
  flex: 1;
  font-weight: 500;
  color: #2c3e50;
}

.expense-value {
  font-weight: 600;
  color: #495057;
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
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .chart-bars {
    gap: 0.5rem;
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
