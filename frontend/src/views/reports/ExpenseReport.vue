<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Expense report</h1>
        <p class="page-subtitle">View a detailed breakdown of expenses by category and account.</p>
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
      <div v-if="loading" class="table-empty">Loading expense report…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="report" class="statement-body">
        <div class="expense-summary">
          <div class="summary-metric">
            <span class="metric-label">Total Expenses</span>
            <span class="metric-value">{{ formatCurrency(report.total_expenses) }}</span>
          </div>
          <div class="summary-metric">
            <span class="metric-label">Average Monthly</span>
            <span class="metric-value">{{ formatCurrency(report.average_monthly || 0) }}</span>
          </div>
          <div class="summary-metric">
            <span class="metric-label">Number of Transactions</span>
            <span class="metric-value">{{ report.transaction_count || 0 }}</span>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Category / Account</th>
                <th class="is-numeric">Amount</th>
                <th class="is-numeric">% of Total</th>
              </tr>
            </thead>
            <tbody v-if="report.expenses && report.expenses.length">
              <tr v-for="item in report.expenses" :key="`expense-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
                <td class="is-numeric">{{ formatPercentage(item.percentage) }}</td>
              </tr>
              <tr class="row-accent">
                <td>Total expenses</td>
                <td class="is-numeric">{{ formatCurrency(report.total_expenses) }}</td>
                <td class="is-numeric">100.0%</td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="3" class="table-empty">No expenses found for this period.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="table-empty">No expense data available.</div>
    </UiCard>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';

export default {
  name: 'ExpenseReport',
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
      return 'Expense breakdown';
    },
    statementSubtitle() {
      const start = this.filters.startDate ? new Date(this.filters.startDate).toLocaleDateString() : 'start';
      const end = this.filters.endDate ? new Date(this.filters.endDate).toLocaleDateString() : 'end';
      return `Expense report from ${start} to ${end}`;
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

        const response = await apiClient.get('/reports/expense-report/', { params });
        this.report = response.data;
      } catch (err) {
        console.warn('Failed to load expense report', err);
        this.error = 'We couldn\'t load the expense report. Try different dates.';
        this.report = null;
      } finally {
        this.loading = false;
      }
    },
    formatCurrency(amount) {
      if (typeof amount !== 'number') return '—';
      return amount.toLocaleString(undefined, { style: 'currency', currency: 'USD' });
    },
    formatPercentage(value) {
      if (typeof value !== 'number') return '—';
      return `${value.toFixed(1)}%`;
    },
    exportCsv() {
      if (!this.report) return;

      const rows = [
        ['Account', 'Amount', '% of Total'],
        ...(this.report.expenses || []).map((item) => [item.name, item.amount, item.percentage]),
        ['Total Expenses', this.report.total_expenses, '100.0'],
      ];

      const csv = rows
        .map((row) => row.map((value) => `"${String(value ?? '')}"`).join(','))
        .join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `expense-report-${this.filters.startDate}-${this.filters.endDate}.csv`;
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

.expense-summary {
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

.row-accent {
  background: rgba(37, 99, 235, 0.04);
  font-weight: 600;
}

.table-empty--error {
  color: var(--color-danger);
}
</style>
