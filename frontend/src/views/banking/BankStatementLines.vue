<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Statement lines</h1>
        <p class="page-subtitle">Review imported transaction details from your bank statements.</p>
      </div>
      <div class="toolbar-group">
        <UiFormField label="Filter by account">
          <select v-model="filters.accountId" @change="fetchLines">
            <option value="">All accounts</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.name }}
            </option>
          </select>
        </UiFormField>
        <UiButton variant="secondary" :loading="loading" @click="fetchLines">
          Refresh
        </UiButton>
      </div>
    </header>

    <UiCard title="Transaction details" subtitle="Imported statement lines with full transaction information.">
      <div v-if="loading" class="table-empty">Loading statement lines…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="lines.length" class="table-container">
        <table class="data-table statement-lines-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th class="is-numeric">Amount</th>
              <th>Reference</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in lines" :key="line.id">
              <td>{{ formatDate(line.date) }}</td>
              <td>
                <div class="line-description">{{ line.description }}</div>
                <div class="line-meta">{{ line.memo || '—' }}</div>
              </td>
              <td :class="['is-numeric', amountClass(line.amount)]">
                {{ formatCurrency(line.amount) }}
              </td>
              <td>{{ line.reference_number || '—' }}</td>
              <td>
                <UiStatusBadge :status="lineStatus(line)">
                  {{ line.status || 'Imported' }}
                </UiStatusBadge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">
        No statement lines found. Import a bank statement to get started.
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
  name: 'BankStatementLines',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiStatusBadge,
  },
  data() {
    return {
      lines: [],
      accounts: [],
      loading: false,
      error: '',
      filters: {
        accountId: '',
      },
    };
  },
  async mounted() {
    await this.loadAccounts();
    await this.fetchLines();
  },
  methods: {
    async loadAccounts() {
      try {
        const response = await apiClient.get('/banking/accounts/');
        const payload = Array.isArray(response.data?.results)
          ? response.data.results
          : Array.isArray(response.data) ? response.data : [];
        this.accounts = payload
          .map((account) => ({
            id: account.id ?? account.BankAccountID ?? account.bank_account_id,
            name: (account.name || account.BankName || account.bank_name || '').toString(),
          }))
          .filter((account) => account.id && account.name.trim() !== '');
      } catch (err) {
        console.warn('Failed to load accounts', err);
      }
    },
    async fetchLines() {
      this.loading = true;
      this.error = '';
      try {
        const params = {};
        if (this.filters.accountId) {
          params.account = this.filters.accountId;
        }

        const response = await apiClient.get('/banking/statement-lines/', { params });
        const payload = Array.isArray(response.data?.results)
          ? response.data.results
          : Array.isArray(response.data) ? response.data : [];
        this.lines = this.normalizeLines(payload);
      } catch (err) {
        console.warn('Failed to load statement lines', err);
        this.error = 'We couldn\'t load statement lines right now.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '—';
      return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(dateString));
    },
    formatCurrency(amount) {
      if (amount == null || amount === '') return '—';
      const numeric = typeof amount === 'number' ? amount : parseFloat(amount);
      if (!Number.isFinite(numeric)) return '—';
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(numeric);
    },
    amountClass(amount) {
      const numeric = typeof amount === 'number' ? amount : parseFloat(amount);
      if (!Number.isFinite(numeric)) return '';
      return numeric < 0 ? 'is-negative' : '';
    },
    lineStatus(line) {
      if (!line.status) return 'info';
      const statusMap = {
        'imported': 'info',
        'matched': 'success',
        'reconciled': 'success',
        'pending': 'warning',
        'error': 'danger',
      };
      return statusMap[line.status.toLowerCase()] || 'info';
    },
    normalizeLines(lines) {
      if (!Array.isArray(lines)) return [];
      return lines
        .map((line) => {
          const amount = this.toNumber(line.amount ?? line.Amount);
          const status = this.normalizeStatus(line.status ?? line.MatchStatus);
          return {
            ...line,
            id: line.id ?? line.BankStatementLineID ?? line.bank_statement_line_id,
            amount,
            status,
            description: (line.description || line.Description || '').toString(),
            memo: line.memo ?? line.BankAcctNotes ?? '',
            reference_number: line.reference_number ?? line.TransactionNumber ?? '',
            date: line.date ?? line.TransactionDate ?? line.transaction_date,
          };
        })
        .filter((line) => {
          const hasDescription = (line.description || '').trim() !== '';
          const hasAmount = Number.isFinite(line.amount) && Math.abs(line.amount) > 0;
          return hasDescription || hasAmount;
        });
    },
    toNumber(value) {
      if (typeof value === 'number') {
        return Number.isFinite(value) ? value : null;
      }
      if (typeof value === 'string' && value.trim() !== '') {
        const parsed = parseFloat(value.replace(/[^0-9.-]+/g, ''));
        return Number.isFinite(parsed) ? parsed : null;
      }
      return null;
    },
    normalizeStatus(status) {
      if (status == null) return null;
      const normalized = status.toString().trim().toLowerCase();
      if (normalized === '' || normalized === 'false' || normalized === '0' || normalized === 'no') {
        return null;
      }
      if (normalized === 'true' || normalized === '1' || normalized === 'yes') {
        return 'Matched';
      }
      if (['imported', 'matched', 'reconciled', 'pending', 'error'].includes(normalized)) {
        return normalized.charAt(0).toUpperCase() + normalized.slice(1);
      }
      return status.toString();
    },
  },
};
</script>

<style scoped>
.toolbar-group :deep(.ui-form-field) {
  min-width: 180px;
}

.statement-lines-table .line-description {
  font-weight: 600;
  color: var(--color-text);
}

.line-meta {
  color: var(--color-text-muted);
  font-size: 0.82rem;
  margin-top: 4px;
}

.statement-lines-table .is-numeric {
  font-variant-numeric: tabular-nums;
}

.table-empty--error {
  color: var(--color-danger);
}

.is-negative {
  color: var(--color-danger);
}
</style>
