<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Income statement</h1>
        <p class="page-subtitle">Track profitability across revenue and expense categories.</p>
      </div>
      <div class="toolbar-group">
        <UiFormField label="Period">
          <select v-model="filters.period" @change="fetchReport">
            <option v-for="option in periodOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
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
      <div v-if="loading" class="table-empty">Loading statement…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="report" class="statement-body">
        <div class="statement-summary">
          <UiStatusBadge :status="netStatus">
            {{ netLabel }}
          </UiStatusBadge>
          <span class="summary-value">{{ formatCurrency(report.net_income) }}</span>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th colspan="2">Revenue</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in report.revenue" :key="`rev-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
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
              <tr v-for="item in report.expenses" :key="`exp-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="row-accent">
                <td>Total expenses</td>
                <td class="is-numeric">{{ formatCurrency(report.total_expenses) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="net-income">
                <td>Net income</td>
                <td class="is-numeric">{{ formatCurrency(report.net_income) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
      <div v-else class="table-empty">No statement data for this period.</div>
    </UiCard>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiStatusBadge from '@/components/ui/UiStatusBadge.vue';

export default {
  name: 'IncomeStatement',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiStatusBadge,
  },
  data() {
    return {
      report: null,
      loading: false,
      error: '',
      filters: {
        period: 'month',
      },
      periodOptions: [
        { value: 'month', label: 'This month' },
        { value: 'quarter', label: 'This quarter' },
        { value: 'year', label: 'Year to date' },
      ],
    };
  },
  computed: {
    periodLabel() {
      const match = this.periodOptions.find((option) => option.value === this.filters.period);
      return match ? match.label.toLowerCase() : 'selected period';
    },
    cardTitle() {
      return 'Statement summary';
    },
    statementSubtitle() {
      return `Showing ${this.periodLabel} performance`;
    },
    netStatus() {
      if (!this.report) return 'info';
      return this.report.net_income >= 0 ? 'success' : 'danger';
    },
    netLabel() {
      if (!this.report) return 'Net position';
      return this.report.net_income >= 0 ? 'Profitable period' : 'Loss-making period';
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
        const response = await apiClient.get('/reports/income-statement/', {
          params: { period: this.filters.period },
        });
        this.report = response.data;
      } catch (err) {
        console.warn('Failed to load income statement', err);
        this.error = 'We couldn\'t load that statement. Try a different period.';
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
        ['Section', 'Name', 'Amount'],
        ...this.report.revenue.map((item) => ['Revenue', item.name, item.amount]),
        ['Revenue', 'Total revenue', this.report.total_revenue],
        ...this.report.expenses.map((item) => ['Expenses', item.name, item.amount]),
        ['Expenses', 'Total expenses', this.report.total_expenses],
        ['Summary', 'Net income', this.report.net_income],
      ];

      const csv = rows
        .map((row) => row.map((value) => `"${String(value ?? '')}"`).join(','))
        .join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `income-statement-${this.filters.period}.csv`;
      link.click();
      URL.revokeObjectURL(url);
    },
  },
};
</script>

<style scoped>
.toolbar-group {
  align-items: flex-end;
}

.toolbar-group :deep(.ui-form-field) {
  min-width: 180px;
}

.statement-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.statement-summary {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.summary-value {
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--color-text);
}

.row-accent {
  background: rgba(37, 99, 235, 0.04);
  font-weight: 600;
}

.net-income td {
  font-weight: 600;
  background: rgba(5, 150, 105, 0.08);
  color: var(--color-success);
  font-size: 1.05rem;
}

.table-empty--error {
  color: var(--color-danger);
}
</style>
