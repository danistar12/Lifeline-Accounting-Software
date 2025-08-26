<template>
  <div class="page container">
    <header class="page-header">
      <h1>Bank Accounts</h1>
      <div class="actions">
        <input v-model="q" @input="filter" placeholder="Search accounts..." class="search" />
        <button @click="openCreate" class="btn btn-primary">New Account</button>
      </div>
    </header>

    <section class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Account Number</th>
            <th>Bank</th>
            <th class="right">Balance</th>
            <th class="actions-col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account in filtered" :key="account.id">
            <td>{{ account.name }}</td>
            <td>{{ account.account_number || '-' }}</td>
            <td>{{ account.bank_name || '-' }}</td>
            <td class="right">{{ formatCurrency(account.balance) }}</td>
            <td class="actions-col">
              <button @click="edit(account)" class="btn btn-link">Edit</button>
            </td>
          </tr>
          <tr v-if="!filtered.length">
            <td colspan="5" class="muted">No bank accounts found.</td>
          </tr>
        </tbody>
      </table>
    </section>

    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-card">
        <h3>{{ modalTitle }}</h3>
        <div class="form-row">
          <label>Name</label>
          <input v-model="form.name" />
        </div>
        <div class="form-row">
          <label>Account Number</label>
          <input v-model="form.account_number" />
        </div>
        <div class="form-row">
          <label>Bank Name</label>
          <input v-model="form.bank_name" />
        </div>
        <div class="form-row">
          <label>Balance</label>
          <input type="number" v-model.number="form.balance" />
        </div>
        <div class="modal-actions">
          <button @click="save" class="btn btn-primary">Save</button>
          <button @click="closeModal" class="btn">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  name: 'BankAccountsView',
  data() {
    return {
      accounts: [],
      q: '',
      showModal: false,
      form: { id: null, name: '', account_number: '', bank_name: '', balance: 0 },
    };
  },
  computed: {
    filtered() {
      const q = this.q && this.q.toLowerCase();
      if (!q) return this.accounts;
      return this.accounts.filter(a => 
        (a.name || '').toLowerCase().includes(q) || 
        (a.account_number || '').toLowerCase().includes(q) ||
        (a.bank_name || '').toLowerCase().includes(q)
      );
    },
    modalTitle() {
      return this.form.id ? 'Edit Bank Account' : 'New Bank Account';
    },
  },
  methods: {
    async load() {
      try {
        const res = await apiClient.get('/banking/accounts/');
        this.accounts = res.data || [];
      } catch (err) {
        console.warn('Failed to load bank accounts', err);
      }
    },
    filter() {
      // computed handles filtering; method kept for potential debouncing later
    },
    formatCurrency(val) {
      if (val == null) return '-';
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(val);
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
    },
    async save() {
      try {
        if (this.form.id) {
          await apiClient.put(`/banking/accounts/${this.form.id}/`, this.form);
        } else {
          await apiClient.post('/banking/accounts/', this.form);
        }
        await this.load();
        this.closeModal();
      } catch (err) {
        console.warn('Failed to save bank account', err);
      }
    },
  },
  mounted() {
    this.load();
  },
};
</script>

<style scoped>
.page { padding: 1.25rem; }
.page-header { display: flex; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.actions { display: flex; gap: 0.5rem; align-items: center; }
.search { padding: 0.5rem; border-radius: 4px; border: 1px solid #ddd; }
.card { background: #fff; border: 1px solid #eee; padding: 0.75rem; border-radius: 6px; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 0.6rem; border-bottom: 1px solid #f2f2f2; text-align: left; }
.table .right { text-align: right; }
.actions-col { width: 120px; }
.modal-backdrop { position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.4); z-index: 1000; }
.modal-card { background: white; padding: 1rem; width: 360px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
.form-row { margin-bottom: 0.5rem; }
.form-row label { display: block; margin-bottom: 0.25rem; font-weight: 500; }
.form-row input { width: 100%; padding: 0.5rem; border-radius: 4px; border: 1px solid #ddd; }
.modal-actions { display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 0.75rem; }
.btn { padding: 0.5rem 0.75rem; border-radius: 4px; border: 1px solid transparent; cursor: pointer; }
.btn-primary { background: #2d8cf0; color: white; }
.btn-link { background: transparent; color: #2d8cf0; border: none; cursor: pointer; }
.muted { color: #888; padding: 1rem; text-align: center; }
</style>
