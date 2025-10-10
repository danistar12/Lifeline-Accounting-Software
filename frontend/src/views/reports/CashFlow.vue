<template>
  <div class="page-shell cash-flow-view">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Cash Flow Statement</h1>
        <p class="page-subtitle">Analyze cash movements across operating, investing and financing activities.</p>
      </div>

      <div class="toolbar-group">
        <UiFormField label="Period">
          <select v-model="filters.period" @change="fetchReport">
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
            <option value="365">Last year</option>
            <option value="all">All time</option>
          </select>
        </UiFormField>

        <UiButton variant="secondary" :loading="loading" @click="fetchReport">Refresh</UiButton>
        <UiButton variant="outline" @click="exportCsv" :disabled="!report">Export CSV</UiButton>
      </div>
    </header>

    <UiCard title="Cash flow" subtitle="Summary of cash inflows and outflows by activity type.">
      <div v-if="loading" class="table-empty">Loading cash flow…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>

      <div v-else-if="report" class="report-container">
        <div class="report-section">
          <h3>Operating Activities</h3>
          <table class="data-table report-table">
            <thead>
              <tr><th>Description</th><th class="is-numeric">Amount</th></tr>
            </thead>
            <tbody>
              <tr v-for="item in report.operating_activities" :key="item.name">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="section-total">
                <td><strong>Net Cash from Operating Activities</strong></td>
                <td class="is-numeric"><strong>{{ formatCurrency(report.net_operating) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h3>Investing Activities</h3>
          <table class="data-table report-table">
            <thead>
              <tr><th>Description</th><th class="is-numeric">Amount</th></tr>
            </thead>
            <tbody>
              <tr v-for="item in report.investing_activities" :key="item.name">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="section-total">
                <td><strong>Net Cash from Investing Activities</strong></td>
                <td class="is-numeric"><strong>{{ formatCurrency(report.net_investing) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-section">
          <h3>Financing Activities</h3>
          <table class="data-table report-table">
            <thead>
              <tr><th>Description</th><th class="is-numeric">Amount</th></tr>
            </thead>
            <tbody>
              <tr v-for="item in report.financing_activities" :key="item.name">
                <td>{{ item.name }}</td>
                <td class="is-numeric">{{ formatCurrency(item.amount) }}</td>
              </tr>
              <tr class="section-total">
                <td><strong>Net Cash from Financing Activities</strong></td>
                <td class="is-numeric"><strong>{{ formatCurrency(report.net_financing) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="report-summary">
          <div class="summary-row"><span>Beginning Cash Balance</span><strong>{{ formatCurrency(report.beginning_cash) }}</strong></div>
          <div class="summary-row"><span>Ending Cash Balance</span><strong>{{ formatCurrency(report.ending_cash) }}</strong></div>
          <div class="summary-row net-cash"><span>Net Increase in Cash</span><strong>{{ formatCurrency(report.net_increase) }}</strong></div>
        </div>
      </div>

      <div v-else class="table-empty">No data available for the selected period.</div>
    </UiCard>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';

export default {
  name: 'CashFlowView',
  components: { UiButton, UiCard, UiFormField },
  data() {
    return {
      report: null,
      loading: false,
      error: '',
      filters: {
        period: '90',
      },
    };
  },
  async mounted() {
    await this.fetchReport();
  },
  methods: {
    async fetchReport() {
      this.loading = true;
      this.error = '';
      try {
        const params = {};
        if (this.filters.period && this.filters.period !== 'all') {
          params.days = parseInt(this.filters.period, 10);
        }
        const res = await apiClient.get('/reports/cash-flow/', { params });
        this.report = res.data || null;
      } catch (err) {
        console.warn('Failed to load cash flow', err);
        this.error = 'We couldn\'t load the cash flow report right now.';
      } finally {
        this.loading = false;
      }
    },
    formatCurrency(amount) {
      if (amount == null || amount === '') return '—';
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(amount);
    },
    exportCsv() {
      if (!this.report) return;
      const rows = [];
      const pushRows = (sectionName, items) => {
        rows.push([sectionName, '']);
        items.forEach(i => rows.push([i.name, i.amount]));
        rows.push(['', '']);
      };

      if (this.report.operating_activities) pushRows('Operating Activities', this.report.operating_activities);
      if (this.report.investing_activities) pushRows('Investing Activities', this.report.investing_activities);
      if (this.report.financing_activities) pushRows('Financing Activities', this.report.financing_activities);

      const csv = rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cash-flow-${this.filters.period}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    }
  }
};
</script>

<style scoped>
@import '@/assets/styles/tokens.css';
@import '@/assets/styles/ui-base.css';

.cash-flow-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-toolbar {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.report-container {
  display: grid;
  gap: 18px;
}

.report-section h3 {
  margin: 0 0 8px 0;
}

.report-table thead th {
  background: var(--color-panel);
  color: var(--color-text-muted);
}

.report-summary {
  margin-top: 18px;
  display: grid;
  gap: 8px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

.summary-row.net-cash {
  background: rgba(5,150,105,0.06);
  border-color: rgba(5,150,105,0.12);
}

.table-empty {
  text-align: center;
  padding: 28px 0;
  color: var(--color-text-muted);
}

.table-empty--error {
  color: var(--color-danger);
}
</style>
