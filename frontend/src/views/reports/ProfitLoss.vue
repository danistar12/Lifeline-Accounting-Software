<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Profit & loss</h1>
        <p class="page-subtitle">View your company's revenues, expenses, and net income over a period.</p>
      </div>
      <div class="toolbar-group">
        <UiFormField label="Start date">
          <input v-model="filters.startDate" type="date" @change="fetchReport" />
        </UiFormField>
        <UiFormField label="End date">
          <input v-model="filters.endDate" type="date" @change="fetchReport" />
        </UiFormField>
        <UiButton variant="secondary" :loading="loading" @click="fetchReport">
          Refresh
        </UiButton>
        <UiButton variant="outline" :disabled="!report" @click="exportCsv">
          Export CSV
        </UiButton>
      </div>
    </header>

    <UiCard :title="cardTitle" :subtitle="statementSubtitle">
      <div v-if="loading" class="table-empty">Loading profit & loss statement…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="report" class="statement-body">
        <div class="pl-summary">
          <div class="summary-metric summary-metric--revenue">
            <span class="metric-label">Total Revenue</span>
            <span class="metric-value">{{ formatCurrency(report.total_revenue) }}</span>
          </div>
          <div class="summary-metric summary-metric--expense">
            <span class="metric-label">Total Expenses</span>
            <span class="metric-value">{{ formatCurrency(report.total_expenses) }}</span>
          </div>
          <div class="summary-metric summary-metric--profit">
            <span class="metric-label">Net Income</span>
            <span class="metric-value" :class="netIncomeClass">{{ formatCurrency(report.net_income) }}</span>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th colspan="2">Revenue</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="report.revenue && report.revenue.length" v-for="item in report.revenue" :key="`revenue-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr v-else>
                <td colspan="2" class="table-empty">No revenue recorded.</td>
              </tr>
              <tr class="row-accent">
                <td>Total revenue</td>
                <td class="is-numeric">{{ formatCurrency(report.total_revenue) }}</td>
              </tr>
            </tbody>
            
            <thead>
              <tr>
                <th colspan="2">Expenses</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="report.expenses && report.expenses.length" v-for="item in report.expenses" :key="`expense-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr v-else>
                <td colspan="2" class="table-empty">No expenses recorded.</td>
              </tr>
              <tr class="row-accent">
                <td>Total expenses</td>
                <td class="is-numeric">{{ formatCurrency(report.total_expenses) }}</td>
              </tr>
            </tbody>
            
            <tfoot>
              <tr class="net-income-row">
                <td>Net income</td>
                <td class="is-numeric" :class="netIncomeClass">{{ formatCurrency(report.net_income) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
      <div v-else class="table-empty">No profit & loss data available.</div>
    </UiCard>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';

export default {
  name: 'ProfitLoss',
  components: {
    UiButton,
    UiCard,
    UiFormField,
  },
  data() {
    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    
    return {
      report: null,
      loading: false,
      error: '',
      filters: {
        startDate: firstDayOfMonth.toISOString().split('T')[0],
        endDate: today.toISOString().split('T')[0],
      },
    };
  },
  computed: {
    cardTitle() {
      return 'Income statement';
    },
    statementSubtitle() {
      const start = this.filters.startDate ? new Date(this.filters.startDate).toLocaleDateString() : 'start';
      const end = this.filters.endDate ? new Date(this.filters.endDate).toLocaleDateString() : 'end';
      return `Profit & loss from ${start} to ${end}`;
    },
    netIncomeClass() {
      if (!this.report) return '';
      return this.report.net_income >= 0 ? 'is-profit' : 'is-loss';
    },
  },
  mounted() {
    this.fetchReport();
  },
  methods: {
    async fetchReport() {
      this.loading = true;
      this.error = '';
      try {
        const params = {};
        if (this.filters.startDate) {
          params.start_date = this.filters.startDate;
        }
        if (this.filters.endDate) {
          params.end_date = this.filters.endDate;
        }

        const response = await apiClient.get('/reports/profit-loss/', { params });
        this.report = response.data;
      } catch (err) {
        console.warn('Failed to load profit & loss', err);
        this.error = 'We couldn\'t load the profit & loss statement. Try different dates.';
        this.report = null;
      } finally {
        this.loading = false;
      }
    },
    formatCurrency(amount) {
      if (typeof amount !== 'number') return '—';
      return amount.toLocaleString(undefined, { style: 'currency', currency: 'USD' });
    },
    exportCsv() {
      if (!this.report) return;

      const rows = [
        ['Section', 'Account', 'Amount'],
        ['Revenue', '', ''],
        ...(this.report.revenue || []).map((item) => ['Revenue', item.name, item.amount]),
        ['Revenue', 'Total Revenue', this.report.total_revenue],
        ['Expenses', '', ''],
        ...(this.report.expenses || []).map((item) => ['Expenses', item.name, item.amount]),
        ['Expenses', 'Total Expenses', this.report.total_expenses],
        ['Summary', 'Net Income', this.report.net_income],
      ];

      const csv = rows
        .map((row) => row.map((value) => `"${String(value ?? '')}"`).join(','))
        .join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `profit-loss-${this.filters.startDate}-${this.filters.endDate}.csv`;
      link.click();
      URL.revokeObjectURL(url);
    },
  },
};
</script>

<style scoped>
.toolbar-group :deep(.ui-form-field) {
  min-width: 160px;
}

.statement-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.pl-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.summary-metric {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  text-align: center;
}

.summary-metric--revenue {
  border-left: 4px solid #10b981;
}

.summary-metric--expense {
  border-left: 4px solid #ef4444;
}

.summary-metric--profit {
  border-left: 4px solid #2563eb;
}

.metric-label {
  display: block;
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.metric-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.metric-value.is-profit {
  color: #10b981;
}

.metric-value.is-loss {
  color: #ef4444;
}

.row-accent {
  background: rgba(37, 99, 235, 0.04);
  font-weight: 600;
}

.net-income-row td {
  font-weight: 600;
  background: rgba(37, 99, 235, 0.08);
  font-size: 1.05rem;
  padding: 16px;
}

.net-income-row .is-profit {
  color: #10b981;
}

.net-income-row .is-loss {
  color: #ef4444;
}

.table-empty--error {
  color: var(--color-danger);
}
</style>
