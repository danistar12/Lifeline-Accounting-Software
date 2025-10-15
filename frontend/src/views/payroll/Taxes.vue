<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Payroll Taxes</h1>
        <p class="page-subtitle">Track statutory withholdings per paystub.</p>
      </div>
      <div class="toolbar-group">
        <UiButton icon="+" variant="primary" @click="openCreate">New tax</UiButton>
      </div>
    </header>

    <UiCard title="Taxes" subtitle="Deductions submitted to tax authorities.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchTaxes">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading taxes…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="taxes.length" class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Paystub</th>
              <th>Tax</th>
              <th class="amount-col">Amount</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tax in taxes" :key="tax.TaxID || tax.tax_id">
              <td>
                <div class="primary-cell">#{{ tax.Paystub || tax.paystub || '—' }}</div>
                <div class="secondary-cell">{{ resolvePaystubLabel(tax.Paystub || tax.paystub) }}</div>
              </td>
              <td>{{ tax.TaxName || tax.tax_name }}</td>
              <td class="amount-col">{{ formatCurrency(tax.TaxAmount ?? tax.tax_amount) }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editTax(tax)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteTax(tax.TaxID || tax.tax_id)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No taxes recorded yet.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save tax"
      :primary-loading="saving"
      @primary="saveTax"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Paystub" required>
            <select v-model="form.paystub" required>
              <option disabled value="">Select paystub</option>
              <option v-for="option in paystubOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </UiFormField>
          <UiFormField label="Tax name" required>
            <input v-model="form.tax_name" required placeholder="e.g., Federal Income" />
          </UiFormField>
        </div>
        <UiFormField label="Amount" required>
          <input v-model="form.tax_amount" required type="number" step="0.01" min="0" />
        </UiFormField>
      </form>
    </UiModal>
  </div>
</template>

<script>
import axios from 'axios';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';
import { normalizeArray, addPascalAliases } from '@/services/normalizeApi';

export default {
  name: 'PayrollTaxes',
  components: { UiButton, UiCard, UiFormField, UiModal },
  data() {
    return {
      taxes: [],
      paystubs: [],
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      editingId: null,
      form: this.defaultForm(),
    };
  },
  computed: {
    modalTitle() {
      return this.editingId ? 'Edit tax' : 'New tax';
    },
    paystubOptions() {
      return this.paystubs.map((stub) => ({
        value: stub.PaystubID ?? stub.paystub_id ?? stub.Paystub ?? stub.paystub,
        label: this.resolvePaystubLabel(stub.PaystubID ?? stub.paystub_id ?? stub.Paystub ?? stub.paystub, stub),
      }));
    },
  },
  mounted() {
    this.fetchPaystubs();
    this.fetchTaxes();
  },
  methods: {
    defaultForm() {
      return { paystub: '', tax_name: '', tax_amount: '' };
    },
    formatCurrency(value) {
      const amount = Number(value);
      if (Number.isNaN(amount)) return '—';
      return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
    },
    resolvePaystubLabel(id, stub = null) {
      const source = stub || this.paystubs.find((item) => {
        const key = item.PaystubID ?? item.paystub_id ?? item.Paystub ?? item.paystub;
        return String(key) === String(id);
      });
      if (!source) return `Paystub ${id || 'N/A'}`;
      const number = source.PaystubID ?? source.paystub_id ?? source.Paystub ?? source.paystub;
      const employee = source.EmployeeName || source.employee_name || 'Unassigned';
      return `${employee} · #${number}`;
    },
    normalizeTaxes(payload) {
      if (!Array.isArray(payload)) return [];
      return normalizeArray(payload).map((item) => ({
        ...item,
        paystub: item.paystub ?? item.Paystub ?? '',
        tax_name: item.tax_name ?? item.TaxName ?? '',
        tax_amount: item.tax_amount ?? item.TaxAmount ?? '',
      }));
    },
    async fetchTaxes() {
      this.loading = true;
      this.error = '';
      try {
        const { data } = await axios.get('/api/payroll/taxes/');
        let payload = data;
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }
        this.taxes = this.normalizeTaxes(Array.isArray(payload) ? payload : []);
      } catch (err) {
        console.error('Error fetching taxes:', err);
        this.error = 'Unable to load taxes right now.';
      } finally {
        this.loading = false;
      }
    },
    async fetchPaystubs() {
      try {
        const { data } = await axios.get('/api/payroll/paystubs/');
        let payload = data;
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }
        this.paystubs = normalizeArray(Array.isArray(payload) ? payload : []);
      } catch (err) {
        console.error('Error fetching paystubs:', err);
      }
    },
    openCreate() {
      this.editingId = null;
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editTax(tax) {
      this.editingId = tax.TaxID ?? tax.tax_id;
      this.form = {
        paystub: tax.Paystub ?? tax.paystub ?? '',
        tax_name: tax.TaxName ?? tax.tax_name ?? '',
        tax_amount: tax.TaxAmount ?? tax.tax_amount ?? '',
      };
      this.showModal = true;
    },
    async saveTax() {
      this.saving = true;
      try {
        const body = {
          paystub: this.form.paystub,
          tax_name: this.form.tax_name,
          tax_amount: this.form.tax_amount,
        };
        let response;
        if (this.editingId) {
          response = await axios.put(`/api/payroll/taxes/${this.editingId}/`, body);
        } else {
          response = await axios.post('/api/payroll/taxes/', body);
        }
        const record = addPascalAliases(response.data);
        const normalized = {
          ...record,
          paystub: record.paystub ?? record.Paystub ?? body.paystub,
          tax_name: record.tax_name ?? record.TaxName ?? body.tax_name,
          tax_amount: record.tax_amount ?? record.TaxAmount ?? body.tax_amount,
        };
        if (this.editingId) {
          const index = this.taxes.findIndex((item) => (item.TaxID ?? item.tax_id) === this.editingId);
          if (index !== -1) this.$set(this.taxes, index, normalized);
        } else {
          this.taxes.unshift(normalized);
        }
        this.showModal = false;
      } catch (err) {
        console.error('Error saving tax:', err);
        this.error = 'Failed to save tax. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    async deleteTax(id) {
      if (!id || !confirm('Delete this tax entry?')) return;
      try {
        await axios.delete(`/api/payroll/taxes/${id}/`);
        this.taxes = this.taxes.filter((item) => (item.TaxID ?? item.tax_id) !== id);
      } catch (err) {
        console.error('Error deleting tax:', err);
        alert('Failed to delete tax.');
      }
    },
  },
};
</script>

<style scoped>
.amount-col {
  text-align: right;
  white-space: nowrap;
}

.primary-cell {
  font-weight: 600;
  color: #2c3e50;
}

.secondary-cell {
  color: #6c757d;
  font-size: 0.85rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
