<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Bank accounts</h1>
        <p class="page-subtitle">Review cash balances and manage your linked institutions.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input
              v-model="q"
              type="search"
              placeholder="Search accounts..."
              @input="filter"
            />
          </UiFormField>
        </div>
      </div>
    </header>

    <UiCard title="Accounts" subtitle="Balances update with each import or reconciliation run.">
      <template #actions>
        <span class="table-meta">{{ filtered.length }} records</span>
        <UiButton
          v-if="canAddAccount"
          icon="+"
          variant="primary"
          @click="openCreate"
        >
          New account
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading accounts…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filtered.length" class="table-container">
        <table class="data-table accounts-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Account number</th>
              <th>Bank</th>
              <th class="is-numeric">Balance</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="account in filtered" :key="account.id">
              <td class="account-name">
                <div class="account-primary">{{ account.name }}</div>
                <div class="account-secondary">{{ account.type || 'Account' }}</div>
              </td>
              <td>{{ account.account_number || '—' }}</td>
              <td>{{ account.bank_name || '—' }}</td>
              <td :class="['is-numeric', balanceClass(account.balance)]">
                {{ formatCurrency(account.balance) }}
              </td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="edit(account)">
                  Edit
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">
        No bank accounts yet. Create one to start tracking balances.
      </div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save account"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Name" required>
            <input v-model="form.name" required />
          </UiFormField>
          <UiFormField label="Account number">
            <input v-model="form.account_number" placeholder="•••• •••• ••••" />
          </UiFormField>
          <UiFormField label="Bank name">
            <input v-model="form.bank_name" />
          </UiFormField>
          <UiFormField label="Balance" hint="Enter the current ledger balance">
            <input type="number" step="0.01" v-model.number="form.balance" />
          </UiFormField>
        </div>
      </form>
    </UiModal>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';

export default {
  name: 'BankAccountsView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
  },
  data() {
    return {
      accounts: [],
      q: '',
      showModal: false,
      loading: false,
      saving: false,
      error: '',
      form: { id: null, name: '', account_number: '', bank_name: '', balance: 0 },
    };
  },
  computed: {
    filtered() {
      const q = this.q && this.q.toLowerCase();
      if (!q) return this.accounts;
      return this.accounts.filter((account) =>
        [account.name, account.account_number, account.bank_name]
          .map((value) => (value || '').toLowerCase())
          .some((value) => value.includes(q))
      );
    },
    modalTitle() {
      return this.form.id ? 'Edit bank account' : 'New bank account';
    },
    canAddAccount() {
      // Allow adding bank accounts when the user is logged in and a company is selected
      const isLoggedIn = this.$store.getters.isLoggedIn;
      const companyId = this.$store.state.selectedCompany?.id;
      return !!(isLoggedIn && companyId);
    }
  },
  methods: {
    async load() {
      this.loading = true;
      this.error = '';
      try {
        const res = await apiClient.get('/banking/accounts/');
        this.accounts = res.data || [];
      } catch (err) {
        console.warn('Failed to load bank accounts', err);
        this.error = 'We couldn\'t load bank accounts right now.';
      } finally {
        this.loading = false;
      }
    },
    filter() {
      // placeholder for future debounced search
    },
    formatCurrency(val) {
      if (val == null || val === '') return '—';
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(val);
    },
    balanceClass(val) {
      if (typeof val !== 'number') return '';
      return val < 0 ? 'is-negative' : '';
    },
    openCreate() {
      this.form = { id: null, name: '', account_number: '', bank_name: '', balance: 0 };
      this.showModal = true;
    },
    edit(account) {
      this.form = { ...account };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.saving = false;
    },
    async save() {
      if (!this.form.name) {
        return;
      }

      this.saving = true;
      try {
        const payload = { ...this.form };

        if (this.form.id) {
          await apiClient.put(`/banking/accounts/${this.form.id}/`, payload);
        } else {
          await apiClient.post('/banking/accounts/', payload);
        }

        await this.load();
        this.closeModal();
      } catch (err) {
        console.warn('Failed to save bank account', err);
        this.error = 'We couldn\'t save that account. Try again.';
        this.saving = false;
      }
    },
  },
  mounted() {
    this.load();
  },
};
</script>

<style scoped>
.toolbar-search :deep(.ui-form-field) {
  min-width: 220px;
}

.toolbar-group {
  display: flex;
  gap: 12px;
  align-items: center; /* center items so the button aligns with the input */
}

.toolbar-search {
  display: flex;
  align-items: center; /* make search field and its label layout align with the button */
}

/* Ensure the UiButton component aligns itself to the center of the toolbar */
.toolbar-group :deep(.ui-button) {
  align-self: center;
}

.accounts-table .account-name {
  width: 28%;
}

.account-primary {
  font-weight: 600;
  color: var(--color-text);
}

.account-secondary {
  color: var(--color-text-muted);
  font-size: 0.82rem;
  margin-top: 4px;
}

.accounts-table .actions-col {
  width: 120px;
}

.table-empty--error {
  color: var(--color-danger);
}

.is-negative {
  color: var(--color-danger);
}

.form-grid {
  display: grid;
  gap: 16px;
}

.modal-form {
  padding-top: 4px;
}

@media (min-width: 640px) {
  .form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
