<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Balance sheet</h1>
        <p class="page-subtitle">View your company's financial position with assets, liabilities, and equity.</p>
      </div>
      <div class="toolbar-group">
        <UiFormField label="As of date">
          <input v-model="filters.asOfDate" type="date" @change="fetchReport" />
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
      <div v-if="loading" class="table-empty">Loading balance sheet…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="report" class="statement-body">
        <div class="balance-summary">
          <div class="summary-metric">
            <span class="metric-label">Total Assets</span>
            <span class="metric-value">{{ formatCurrency(report.total_assets) }}</span>
          </div>
          <div class="summary-metric">
            <span class="metric-label">Total Liabilities</span>
            <span class="metric-value">{{ formatCurrency(report.total_liabilities) }}</span>
          </div>
          <div class="summary-metric">
            <span class="metric-label">Total Equity</span>
            <span class="metric-value">{{ formatCurrency(report.total_equity) }}</span>
          </div>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th colspan="2">Assets</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in report.assets" :key="`asset-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="row-accent">
                <td>Total assets</td>
                <td class="is-numeric">{{ formatCurrency(report.total_assets) }}</td>
              </tr>
            </tbody>
            <thead>
              <tr>
                <th colspan="2">Liabilities</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in report.liabilities" :key="`liability-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="row-accent">
                <td>Total liabilities</td>
                <td class="is-numeric">{{ formatCurrency(report.total_liabilities) }}</td>
              </tr>
            </tbody>
            <thead>
              <tr>
                <th colspan="2">Equity</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in report.equity" :key="`equity-${item.name}`">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="row-accent">
                <td>Total equity</td>
                <td class="is-numeric">{{ formatCurrency(report.total_equity) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="balance-check">
                <td>Liabilities + Equity</td>
                <td class="is-numeric">{{ formatCurrency(report.total_liabilities_and_equity) }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
      <div v-else class="table-empty">No balance sheet data available.</div>
    </UiCard>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';

export default {
  name: 'BalanceSheet',
  components: {
    UiButton,
    UiCard,
    UiFormField,
  },
  data() {
    return {
      report: null,
      loading: false,
      error: '',
      filters: {
        asOfDate: new Date().toISOString().split('T')[0], // Today's date
      },
    };
  },
  computed: {
    cardTitle() {
      return 'Financial position';
    },
    statementSubtitle() {
      const date = this.filters.asOfDate ? new Date(this.filters.asOfDate).toLocaleDateString() : 'today';
      return `Balance sheet as of ${date}`;
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
        if (this.filters.asOfDate) {
          params.as_of_date = this.filters.asOfDate;
        }

        const response = await apiClient.get('/reports/balance-sheet/', { params });
        this.report = response.data;
      } catch (err) {
        console.warn('Failed to load balance sheet', err);
        this.error = 'We couldn\'t load the balance sheet. Try a different date.';
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
        ...this.report.assets.map((item) => ['Assets', item.name, item.amount]),
        ['Assets', 'Total Assets', this.report.total_assets],
        ...this.report.liabilities.map((item) => ['Liabilities', item.name, item.amount]),
        ['Liabilities', 'Total Liabilities', this.report.total_liabilities],
        ...this.report.equity.map((item) => ['Equity', item.name, item.amount]),
        ['Equity', 'Total Equity', this.report.total_equity],
        ['Summary', 'Liabilities + Equity', this.report.total_liabilities_and_equity],
      ];

      const csv = rows
        .map((row) => row.map((value) => `"${String(value ?? '')}"`).join(','))
        .join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `balance-sheet-${this.filters.asOfDate || 'latest'}.csv`;
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

.balance-summary {
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

.balance-check td {
  font-weight: 600;
  background: rgba(5, 150, 105, 0.08);
  color: var(--color-success);
  font-size: 1.05rem;
}

.table-empty--error {
  color: var(--color-danger);
}
</style>
