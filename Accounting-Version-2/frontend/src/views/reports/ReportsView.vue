<template>
  <div class="view-container">
    <h2 class="view-title">Financial Reports & Analytics</h2>
    
    <!-- Dashboard Summary Cards -->
    <div class="dashboard-grid" v-if="dashboardData">
      <div class="summary-card banking">
        <h3>Banking Overview</h3>
        <div class="metric-group">
          <div class="metric">
            <span class="label">Total Balance</span>
            <span class="value">${{ formatCurrency(dashboardData.banking.total_balance) }}</span>
          </div>
          <div class="metric">
            <span class="label">Accounts</span>
            <span class="value">{{ dashboardData.banking.account_count }}</span>
          </div>
          <div class="metric">
            <span class="label">Recent Inflow</span>
            <span class="value positive">${{ formatCurrency(dashboardData.banking.recent_inflow) }}</span>
          </div>
          <div class="metric">
            <span class="label">Recent Outflow</span>
            <span class="value negative">${{ formatCurrency(dashboardData.banking.recent_outflow) }}</span>
          </div>
        </div>
      </div>

      <div class="summary-card payroll">
        <h3>Payroll Summary</h3>
        <div class="metric-group">
          <div class="metric">
            <span class="label">Employees</span>
            <span class="value">{{ dashboardData.payroll.employee_count }}</span>
          </div>
          <div class="metric">
            <span class="label">Current Month Gross</span>
            <span class="value">${{ formatCurrency(dashboardData.payroll.current_month_gross) }}</span>
          </div>
          <div class="metric">
            <span class="label">Current Month Net</span>
            <span class="value">${{ formatCurrency(dashboardData.payroll.current_month_net) }}</span>
          </div>
          <div class="metric">
            <span class="label">Taxes Withheld</span>
            <span class="value">${{ formatCurrency(dashboardData.payroll.current_month_taxes) }}</span>
          </div>
        </div>
      </div>

      <div class="summary-card business">
        <h3>Business Metrics</h3>
        <div class="metric-group">
          <div class="metric">
            <span class="label">Customers</span>
            <span class="value">{{ dashboardData.business.customer_count }}</span>
          </div>
          <div class="metric">
            <span class="label">Vendors</span>
            <span class="value">{{ dashboardData.business.vendor_count }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Report Sections -->
    <div class="report-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Payroll Report -->
    <div v-if="activeTab === 'payroll'" class="report-section">
      <h3>Payroll Analysis</h3>
      
      <div class="date-controls">
        <input type="date" v-model="payrollStartDate" @change="loadPayrollReport">
        <input type="date" v-model="payrollEndDate" @change="loadPayrollReport">
        <button @click="loadPayrollReport" class="refresh-btn">Refresh</button>
      </div>

      <div v-if="payrollReport" class="report-content">
        <div class="summary-stats">
          <div class="stat">
            <h4>Total Gross Pay</h4>
            <p class="amount">${{ formatCurrency(payrollReport.summary.total_gross) }}</p>
          </div>
          <div class="stat">
            <h4>Total Net Pay</h4>
            <p class="amount">${{ formatCurrency(payrollReport.summary.total_net) }}</p>
          </div>
          <div class="stat">
            <h4>Total Taxes</h4>
            <p class="amount">${{ formatCurrency(payrollReport.summary.total_taxes) }}</p>
          </div>
          <div class="stat">
            <h4>Pay Periods</h4>
            <p class="amount">{{ payrollReport.summary.total_records }}</p>
          </div>
        </div>

        <div class="data-table">
          <h4>Employee Breakdown</h4>
          <table>
            <thead>
              <tr>
                <th>Employee</th>
                <th>Email</th>
                <th>Hourly Rate</th>
                <th>Total Gross</th>
                <th>Total Net</th>
                <th>Total Taxes</th>
                <th>Pay Periods</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="emp in payrollReport.employee_breakdown" :key="emp.employee__email">
                <td>{{ emp.employee__name }}</td>
                <td>{{ emp.employee__email }}</td>
                <td>${{ formatCurrency(emp.employee__hourly_rate) }}</td>
                <td>${{ formatCurrency(emp.total_gross) }}</td>
                <td>${{ formatCurrency(emp.total_net) }}</td>
                <td>${{ formatCurrency(emp.total_taxes) }}</td>
                <td>{{ emp.pay_periods }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="data-table" v-if="payrollReport.monthly_breakdown.length">
          <h4>Monthly Breakdown</h4>
          <table>
            <thead>
              <tr>
                <th>Month</th>
                <th>Gross Pay</th>
                <th>Net Pay</th>
                <th>Taxes Withheld</th>
                <th>Payroll Count</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="month in payrollReport.monthly_breakdown" :key="month.month">
                <td>{{ formatDate(month.month) }}</td>
                <td>${{ formatCurrency(month.gross_pay) }}</td>
                <td>${{ formatCurrency(month.net_pay) }}</td>
                <td>${{ formatCurrency(month.taxes_withheld) }}</td>
                <td>{{ month.payroll_count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Employee List -->
    <div v-if="activeTab === 'employees'" class="report-section">
      <h3>Employee Directory</h3>
      
      <button @click="loadEmployees" class="refresh-btn">Refresh</button>

      <div v-if="employees" class="data-table">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Hourly Rate</th>
              <th>Tax Withholding</th>
              <th>Company</th>
              <th>Last Pay Date</th>
              <th>Last Gross Pay</th>
              <th>Last Net Pay</th>
              <th>Hire Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="emp in employees.employees" :key="emp.employee_id">
              <td>{{ emp.name }}</td>
              <td>{{ emp.email }}</td>
              <td>${{ formatCurrency(emp.hourly_rate) }}</td>
              <td>{{ formatPercent(emp.tax_withholding) }}</td>
              <td>{{ emp.company__company_name }}</td>
              <td>{{ emp.last_pay_date ? formatDate(emp.last_pay_date) : 'N/A' }}</td>
              <td>${{ formatCurrency(emp.last_gross_pay) }}</td>
              <td>${{ formatCurrency(emp.last_net_pay) }}</td>
              <td>{{ formatDate(emp.created_date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Banking Report -->
    <div v-if="activeTab === 'banking'" class="report-section">
      <h3>Banking Analysis</h3>
      
      <div class="date-controls">
        <input type="date" v-model="bankingStartDate" @change="loadBankingReport">
        <input type="date" v-model="bankingEndDate" @change="loadBankingReport">
        <button @click="loadBankingReport" class="refresh-btn">Refresh</button>
      </div>

      <div v-if="bankingReport" class="report-content">
        <div class="summary-stats">
          <div class="stat">
            <h4>Total Inflow</h4>
            <p class="amount positive">${{ formatCurrency(bankingReport.summary.total_inflow) }}</p>
          </div>
          <div class="stat">
            <h4>Total Outflow</h4>
            <p class="amount negative">${{ formatCurrency(Math.abs(bankingReport.summary.total_outflow)) }}</p>
          </div>
          <div class="stat">
            <h4>Transactions</h4>
            <p class="amount">{{ bankingReport.summary.transaction_count }}</p>
          </div>
          <div class="stat">
            <h4>Reconciled</h4>
            <p class="amount">{{ bankingReport.summary.reconciled_count }}</p>
          </div>
        </div>

        <div class="data-table">
          <h4>Bank Accounts</h4>
          <table>
            <thead>
              <tr>
                <th>Bank</th>
                <th>Account Number</th>
                <th>Type</th>
                <th>Balance</th>
                <th>Currency</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="account in bankingReport.accounts" :key="account.bank_account_id">
                <td>{{ account.bank_name }}</td>
                <td>{{ account.account_number }}</td>
                <td>{{ account.account_type }}</td>
                <td>${{ formatCurrency(account.balance) }}</td>
                <td>{{ account.currency_code }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="data-table">
          <h4>Recent Transactions</h4>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Amount</th>
                <th>Type</th>
                <th>Bank</th>
                <th>Reconciled</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="txn in bankingReport.recent_transactions" :key="txn.transaction_date + txn.description">
                <td>{{ formatDate(txn.transaction_date) }}</td>
                <td>{{ txn.description }}</td>
                <td :class="txn.amount >= 0 ? 'positive' : 'negative'">${{ formatCurrency(Math.abs(txn.amount)) }}</td>
                <td>{{ txn.transaction_type }}</td>
                <td>{{ txn.bank_account__bank_name }}</td>
                <td>{{ txn.reconciled ? '✓' : '✗' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api'

// Reactive data
const dashboardData = ref(null)
const payrollReport = ref(null)
const employees = ref(null)
const bankingReport = ref(null)
const loading = ref(false)
const error = ref('')

// Active tab
const activeTab = ref('payroll')
const tabs = [
  { id: 'payroll', label: 'Payroll Analysis' },
  { id: 'employees', label: 'Employee Directory' },
  { id: 'banking', label: 'Banking Reports' }
]

// Date filters
const payrollStartDate = ref('')
const payrollEndDate = ref('')
const bankingStartDate = ref('')
const bankingEndDate = ref('')

// Initialize date ranges (last 3 months)
const initializeDates = () => {
  const today = new Date()
  const threeMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 3, today.getDate())
  
  payrollStartDate.value = threeMonthsAgo.toISOString().split('T')[0]
  payrollEndDate.value = today.toISOString().split('T')[0]
  bankingStartDate.value = threeMonthsAgo.toISOString().split('T')[0]
  bankingEndDate.value = today.toISOString().split('T')[0]
}

// Load dashboard data
const loadDashboard = async () => {
  try {
    const response = await apiClient.get('/reports/dashboard/')
    dashboardData.value = response.data
  } catch (err) {
    error.value = 'Failed to load dashboard data'
    console.error(err)
  }
}

// Load payroll report
const loadPayrollReport = async () => {
  try {
    loading.value = true
    const params = new URLSearchParams()
    if (payrollStartDate.value) params.append('start_date', payrollStartDate.value)
    if (payrollEndDate.value) params.append('end_date', payrollEndDate.value)
    
    const response = await apiClient.get(`/reports/payroll-summary/?${params}`)
    payrollReport.value = response.data
  } catch (err) {
    error.value = 'Failed to load payroll report'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Load employees
const loadEmployees = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/reports/employees/')
    employees.value = response.data
  } catch (err) {
    error.value = 'Failed to load employees'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Load banking report
const loadBankingReport = async () => {
  try {
    loading.value = true
    const params = new URLSearchParams()
    if (bankingStartDate.value) params.append('start_date', bankingStartDate.value)
    if (bankingEndDate.value) params.append('end_date', bankingEndDate.value)
    
    const response = await apiClient.get(`/reports/banking/?${params}`)
    bankingReport.value = response.data
  } catch (err) {
    error.value = 'Failed to load banking report'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Utility functions
const formatCurrency = (amount) => {
  if (!amount) return '0.00'
  return Number(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatPercent = (decimal) => {
  if (!decimal) return '0%'
  return `${(Number(decimal) * 100).toFixed(1)}%`
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString()
}

// Initialize component
onMounted(() => {
  initializeDates()
  loadDashboard()
  loadPayrollReport()
  loadEmployees()
  loadBankingReport()
})
</script>

<style scoped>
.view-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.view-title {
  color: #1e3c72;
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 32px;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.summary-card {
  background: linear-gradient(120deg, #e3eafc 0%, #f8fbff 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(30,60,114,0.1);
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(30,60,114,0.2);
}

.summary-card h3 {
  color: #1e3c72;
  margin-bottom: 20px;
  font-size: 1.3rem;
  font-weight: 600;
}

.summary-card.banking {
  border-left: 4px solid #4CAF50;
}

.summary-card.payroll {
  border-left: 4px solid #2196F3;
}

.summary-card.business {
  border-left: 4px solid #FF9800;
}

.metric-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.metric {
  text-align: center;
}

.metric .label {
  display: block;
  font-size: 0.9rem;
  color: #555; /* Slightly lighter but still readable */
  margin-bottom: 4px;
  font-weight: 500;
}

.metric .value {
  display: block;
  font-size: 1.4rem;
  font-weight: 700;
  color: #1e3c72;
}

.metric .value.positive {
  color: #4CAF50;
}

.metric .value.negative {
  color: #f44336;
}

/* Report Tabs */
.report-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 32px;
  border-bottom: 2px solid #e3eafc;
}

.tab-button {
  padding: 12px 24px;
  background: transparent;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  color: #555; /* Darker grey for better readability */
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
}

.tab-button:hover {
  background: #f0f4f8;
  color: #1e3c72;
}

.tab-button.active {
  background: #1e3c72;
  color: white; /* Keep white text on navy background */
  font-weight: 600;
}

/* Report Sections */
.report-section {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.report-section h3 {
  color: #1e3c72;
  font-size: 1.6rem;
  margin-bottom: 24px;
}

/* Date Controls */
.date-controls {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
  align-items: center;
}

.date-controls input[type="date"] {
  padding: 8px 12px;
  border: 2px solid #e3eafc;
  border-radius: 8px;
  font-size: 1rem;
  color: #333; /* Ensure input text is dark */
  background: white;
}

.date-controls input[type="date"]:focus {
  outline: none;
  border-color: #1e3c72;
  box-shadow: 0 0 0 2px rgba(30, 60, 114, 0.1);
}

.refresh-btn {
  background: #1e3c72 !important;
  color: white !important; /* Force white text on navy button */
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.refresh-btn:hover {
  background: #2a5298 !important;
  color: white !important; /* Ensure white text stays on hover */
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(30, 60, 114, 0.3);
}

/* Summary Stats */
.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat {
  background: #f8fbff;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  border: 2px solid #e3eafc;
}

.stat h4 {
  color: #555; /* Darker for better readability */
  margin-bottom: 8px;
  font-size: 0.9rem;
  font-weight: 600; /* Slightly bolder */
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat .amount {
  font-size: 2rem;
  font-weight: 700;
  color: #1e3c72;
  margin: 0;
}

.stat .amount.positive {
  color: #4CAF50;
}

.stat .amount.negative {
  color: #f44336;
}

/* Data Tables */
.data-table {
  margin-bottom: 40px;
}

.data-table h4 {
  color: #1e3c72;
  margin-bottom: 16px;
  font-size: 1.2rem;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.data-table th {
  background: #1e3c72 !important;
  color: white !important; /* Force white text on navy header background */
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
}

.data-table thead th {
  background: #1e3c72 !important;
  color: white !important; /* Additional specificity for thead th */
}

.data-table tbody th {
  background: #1e3c72 !important;
  color: white !important; /* Additional specificity for tbody th if any */
}

.data-table td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.9rem;
  color: #333; /* Ensure text is dark, not grey */
}

.data-table tbody tr:hover {
  background: #f8fbff;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* Ensure all text elements have proper colors */
.view-container {
  color: #333;
}

.view-title {
  color: #1e3c72;
}

.summary-card h3 {
  color: #333;
  margin-bottom: 16px;
  font-size: 1.1rem;
  font-weight: 600;
}

/* Fix any remaining grey text issues */
.view-container * {
  color: inherit;
}

/* Override any default browser grey text - but exclude table headers */
.view-container p,
.view-container span,
.view-container div,
.view-container td {
  color: inherit;
}

/* Specific fixes for table content - but NOT headers */
.data-table tbody td {
  color: #333 !important;
}

/* Ensure table headers stay white on navy */
.data-table th,
.data-table thead th,
.data-table tbody th {
  background: #1e3c72 !important;
  color: white !important;
}

/* Fix button text */
.refresh-btn,
.tab-button {
  font-weight: 600;
}

/* Ensure loading and error states are visible */
.loading,
.error {
  color: #333;
  font-weight: 500;
}

.positive {
  color: #4CAF50 !important;
  font-weight: 600;
}

.negative {
  color: #f44336 !important;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-group {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .summary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .date-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .data-table {
    overflow-x: auto;
  }
  
  .report-tabs {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .metric-group {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style>
