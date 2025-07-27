<template>
  <div class="dashboard">
    <!-- Loading State -->
    <div v-if="loading" class="dashboard-loading">
      <div class="loading-spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="dashboard-error">
      <span class="error-icon">⚠️</span>
      <p>{{ error }}</p>
      <button @click="fetchDashboardData" class="retry-button">
        Try Again
      </button>
    </div>

    <!-- Main Content -->
    <div v-else class="dashboard-content">
      <!-- Header -->
      <div class="dashboard-header">
        <h1 class="dashboard-title">Dashboard Overview</h1>
        <p class="dashboard-subtitle">Welcome back! Here's what's happening with your business today.</p>
      </div>

      <!-- Key Metrics Cards -->
      <div class="metrics-grid">
        <div v-for="metric in keyMetrics" :key="metric.label" class="metric-card">
          <div class="metric-icon" :class="metric.trend">
            <span>{{ metric.icon }}</span>
          </div>
          <div class="metric-content">
            <h3 class="metric-label">{{ metric.label }}</h3>
            <div class="metric-value">{{ formatCurrency(metric.value) }}</div>
            <div class="metric-trend" :class="metric.trend">
              {{ metric.trendValue }}
              <span class="trend-icon">{{ metric.trend === 'up' ? '↑' : '↓' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="charts-grid">
        <!-- Revenue Chart -->
        <div class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">Revenue & Expenses</h2>
            <div class="period-selector">
              <button 
                v-for="period in periods" 
                :key="period.value"
                :class="{ active: selectedPeriod === period.value }"
                @click="changePeriod(period.value)"
                class="period-btn"
              >
                {{ period.label }}
              </button>
            </div>
          </div>
          <div class="chart-container">
            <LineChart v-if="revenueData" :chart-data="revenueData" />
            <div v-else class="chart-placeholder">Loading chart...</div>
          </div>
        </div>

        <!-- Cash Flow Chart -->
        <div class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">Cash Flow</h2>
          </div>
          <div class="chart-container">
            <BarChart v-if="cashFlowData" :chart-data="cashFlowData" />
            <div v-else class="chart-placeholder">Loading chart...</div>
          </div>
        </div>

        <!-- Account Balances -->
        <div class="chart-card">
          <div class="chart-header">
            <h2 class="chart-title">Account Balances</h2>
          </div>
          <div class="chart-container">
            <DoughnutChart v-if="accountData" :chart-data="accountData" />
            <div v-else class="chart-placeholder">Loading chart...</div>
          </div>
        </div>
      </div>

      <!-- Data Tables -->
      <div class="tables-grid">
        <!-- Recent Transactions -->
        <div class="table-card">
          <h2 class="table-title">Recent Transactions</h2>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Type</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="transaction in recentTransactions" :key="transaction.id">
                  <td>{{ formatDate(transaction.date) }}</td>
                  <td>{{ transaction.description }}</td>
                  <td>
                    <span class="transaction-type" :class="transaction.type">
                      {{ transaction.type }}
                    </span>
                  </td>
                  <td class="amount" :class="transaction.type">
                    {{ formatCurrency(transaction.amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Invoice Status -->
        <div class="table-card">
          <h2 class="table-title">Invoice Status</h2>
          <div class="invoice-summary">
            <div class="invoice-stat">
              <span class="stat-label">Outstanding</span>
              <span class="stat-value">{{ formatCurrency(invoiceStatus.outstanding) }}</span>
            </div>
            <div class="invoice-stat">
              <span class="stat-label">Overdue</span>
              <span class="stat-value overdue">{{ formatCurrency(invoiceStatus.overdue) }}</span>
            </div>
            <div class="invoice-stat">
              <span class="stat-label">Paid This Month</span>
              <span class="stat-value">{{ formatCurrency(invoiceStatus.paid) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import LineChart from '@/components/charts/LineChart.vue'
import BarChart from '@/components/charts/BarChart.vue'
import DoughnutChart from '@/components/charts/DoughnutChart.vue'
import { formatCurrency, formatDate } from '@/utils/formatters'
import axios from 'axios'

// State
const loading = ref(true)
const error = ref(null)
const selectedPeriod = ref('month')

// Data
const dashboardData = ref(null)
const revenueData = ref(null)
const cashFlowData = ref(null)
const accountData = ref(null)
const recentTransactions = ref([])
const invoiceStatus = ref({
  outstanding: 0,
  overdue: 0,
  paid: 0
})

// Period options
const periods = [
  { label: '7D', value: 'week' },
  { label: '1M', value: 'month' },
  { label: '3M', value: 'quarter' },
  { label: '1Y', value: 'year' }
]

// Computed
const keyMetrics = computed(() => {
  if (!dashboardData.value) return []
  
  const data = dashboardData.value
  return [
    {
      label: 'Total Revenue',
      value: data.total_revenue || 0,
      icon: '💰',
      trend: 'up',
      trendValue: '+12.5%'
    },
    {
      label: 'Net Profit',
      value: data.net_profit || 0,
      icon: '📈',
      trend: 'up',
      trendValue: '+8.2%'
    },
    {
      label: 'Outstanding Invoices',
      value: data.outstanding_invoices || 0,
      icon: '📋',
      trend: 'down',
      trendValue: '-3.1%'
    },
    {
      label: 'Cash Balance',
      value: data.cash_balance || 0,
      icon: '🏦',
      trend: 'up',
      trendValue: '+5.7%'
    }
  ]
})

// Methods
const fetchDashboardData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get('/api/reports/dashboard/')
    dashboardData.value = response.data
    
    // Create chart data
    createChartData()
    
    // Mock some additional data for now
    recentTransactions.value = [
      { id: 1, date: '2025-07-25', description: 'Client Payment', type: 'income', amount: 2500 },
      { id: 2, date: '2025-07-24', description: 'Office Supplies', type: 'expense', amount: -150 },
      { id: 3, date: '2025-07-23', description: 'Service Fee', type: 'income', amount: 800 },
      { id: 4, date: '2025-07-22', description: 'Utilities', type: 'expense', amount: -200 }
    ]
    
    invoiceStatus.value = {
      outstanding: 15000,
      overdue: 3200,
      paid: 45000
    }
    
  } catch (err) {
    error.value = 'Failed to load dashboard data: ' + err.message
    console.error('Dashboard error:', err)
  } finally {
    loading.value = false
  }
}

const createChartData = () => {
  // Revenue chart
  revenueData.value = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    datasets: [
      {
        label: 'Revenue',
        data: [12000, 15000, 13000, 17000, 16000, 19000, 21000],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4
      },
      {
        label: 'Expenses',
        data: [8000, 9000, 8500, 10000, 9500, 11000, 12000],
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4
      }
    ]
  }
  
  // Cash flow chart
  cashFlowData.value = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [{
      label: 'Cash Flow',
      data: [5000, -2000, 8000, 3000],
      backgroundColor: [
        'rgba(34, 197, 94, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(34, 197, 94, 0.8)',
        'rgba(34, 197, 94, 0.8)'
      ]
    }]
  }
  
  // Account balances chart
  accountData.value = {
    labels: ['Checking', 'Savings', 'Credit Card', 'Loans'],
    datasets: [{
      data: [25000, 45000, -5000, -15000],
      backgroundColor: [
        'rgba(59, 130, 246, 0.8)',
        'rgba(34, 197, 94, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(245, 158, 11, 0.8)'
      ]
    }]
  }
}

const changePeriod = (period) => {
  selectedPeriod.value = period
  // Here you would typically refetch data for the new period
  fetchDashboardData()
}

// Initialize
onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background-color: #f8fafc;
  min-height: 100vh;
  color: #1e293b;
}

.dashboard-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #64748b;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.dashboard-error {
  text-align: center;
  padding: 40px;
  color: #dc2626;
}

.retry-button {
  margin-top: 16px;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.dashboard-subtitle {
  font-size: 16px;
  color: #64748b;
  margin: 0;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.metric-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.metric-icon.up {
  background: rgba(34, 197, 94, 0.1);
}

.metric-icon.down {
  background: rgba(239, 68, 68, 0.1);
}

.metric-content {
  flex: 1;
}

.metric-label {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 4px 0;
  font-weight: 500;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 4px 0;
}

.metric-trend {
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.metric-trend.up {
  color: #22c55e;
}

.metric-trend.down {
  color: #ef4444;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.period-selector {
  display: flex;
  gap: 4px;
}

.period-btn {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.period-btn:hover {
  background: #f1f5f9;
}

.period-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.chart-container {
  padding: 24px;
  height: 300px;
}

.chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #64748b;
}

.tables-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.table-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-title {
  padding: 20px 24px;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  border-bottom: 1px solid #e2e8f0;
}

.table-container {
  max-height: 300px;
  overflow-y: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f8fafc;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  color: #1f2937;
}

.transaction-type {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.transaction-type.income {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.transaction-type.expense {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.amount.income {
  color: #22c55e;
  font-weight: 600;
}

.amount.expense {
  color: #ef4444;
  font-weight: 600;
}

.invoice-summary {
  padding: 24px;
}

.invoice-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.invoice-stat:last-child {
  border-bottom: none;
}

.stat-label {
  color: #64748b;
  font-size: 14px;
}

.stat-value {
  font-weight: 600;
  color: #0f172a;
}

.stat-value.overdue {
  color: #ef4444;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .tables-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    padding: 16px;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>
