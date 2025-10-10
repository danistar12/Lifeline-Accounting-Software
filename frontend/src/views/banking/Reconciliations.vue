<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Reconciliations</h1>
        <p class="page-subtitle">Track bank statement reconciliations and matched transactions.</p>
      </div>
      <div class="toolbar-group">
        <UiFormField label="Account">
          <select v-model="filters.accountId" @change="fetchEntries">
            <option value="">All accounts</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.name }}
            </option>
          </select>
        </UiFormField>
        <UiFormField label="Period">
          <select v-model="filters.period" @change="fetchEntries">
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
            <option value="365">Last year</option>
            <option value="all">All time</option>
          </select>
        </UiFormField>
        <UiButton variant="secondary" :loading="loading" @click="fetchEntries">
          Refresh
        </UiButton>
      </div>
    </header>

    <UiCard title="Reconciliation history" subtitle="Matched bank statement lines with general ledger transactions.">
      <template #actions>
        <span class="table-meta">{{ entries.length }} reconciliations</span>
      </template>

      <div v-if="loading" class="table-empty">Loading reconciliations…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="entries.length" class="table-container">
        <table class="data-table reconciliations-table">
          <thead>
            <tr>
              <th>Reconciled date</th>
              <th>Account</th>
              <th>Statement line</th>
              <th>GL transaction</th>
              <th class="is-numeric">Amount</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in entries" :key="entry.id">
              <td>
                <div class="reconciliation-date">{{ formatDate(entry.reconciled_date) }}</div>
                <div class="reconciliation-meta">{{ formatTime(entry.reconciled_date) }}</div>
              </td>
              <td>{{ entry.account_name || '—' }}</td>
              <td>
                <div class="transaction-ref">{{ entry.statement_line_ref || entry.statement_line }}</div>
                <div class="transaction-desc">{{ entry.statement_description || '—' }}</div>
              </td>
              <td>
                <div class="transaction-ref">{{ entry.gl_transaction_ref || entry.gl_transaction }}</div>
                <div class="transaction-desc">{{ entry.gl_description || '—' }}</div>
              </td>
              <td :class="['is-numeric', amountClass(entry.amount)]">
                {{ formatCurrency(entry.amount) }}
              </td>
              <td>
                <UiStatusBadge status="success">
                  Reconciled
                </UiStatusBadge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">
        No reconciliations found for the selected filters.
      </div>
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
  name: 'ReconciliationsView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiStatusBadge,
  },
  data() {
    return {
      entries: [],
      accounts: [],
      loading: false,
      error: '',
      filters: {
        accountId: '',
        period: '90',
      },
    };
  },
  async mounted() {
    await this.loadAccounts();
    await this.fetchEntries();
  },
  methods: {
    async loadAccounts() {
      try {
        const response = await apiClient.get('/banking/accounts/');
        this.accounts = response.data || [];
      } catch (err) {
        console.warn('Failed to load accounts', err);
      }
    },
    async fetchEntries() {
      this.loading = true;
      this.error = '';
      try {
        const params = {};
        if (this.filters.accountId) {
          params.account = this.filters.accountId;
        }
        if (this.filters.period && this.filters.period !== 'all') {
          const days = parseInt(this.filters.period);
          const date = new Date();
          date.setDate(date.getDate() - days);
          params.since_date = date.toISOString().split('T')[0];
        }

        const response = await apiClient.get('/banking/reconciliations/', { params });
        this.entries = response.data || [];
      } catch (err) {
        console.warn('Failed to load reconciliations', err);
        this.error = 'We couldn\'t load reconciliation entries right now.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '—';
      return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(dateString));
    },
    formatTime(dateString) {
      if (!dateString) return '';
      return new Intl.DateTimeFormat(undefined, { timeStyle: 'short' }).format(new Date(dateString));
    },
    formatCurrency(amount) {
      if (amount == null || amount === '') return '—';
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(amount);
    },
    amountClass(amount) {
      if (typeof amount !== 'number') return '';
      return amount < 0 ? 'is-negative' : '';
    },
  },
};
</script>

<style scoped>
@import '@/assets/styles/tokens.css';
@import '@/assets/styles/ui-base.css';

.reconciliations-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.filters-section {
  display: flex;
  gap: 12px;
  align-items: end;
  flex-wrap: wrap;
}

.filters-section .form-field {
  min-width: 200px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.data-table th {
  text-align: left;
  padding: 14px 18px;
  background: var(--color-panel);
  color: var(--color-text-muted);
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
}

.data-table td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.data-table tbody tr:hover {
  background: rgba(37, 99, 235, 0.05);
}

.amount-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.amount-cell.is-negative {
  color: var(--color-danger);
}

.status-cell {
  text-align: center;
}

.empty-state {
  text-align: center;
  padding: 32px 0;
  color: var(--color-text-muted);
}

@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-section .form-field {
    min-width: auto;
  }
}
</style>
