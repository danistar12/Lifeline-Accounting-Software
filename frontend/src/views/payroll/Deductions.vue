<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Payroll Deductions</h1>
        <p class="page-subtitle">Manage employee-specific reductions per paystub.</p>
      </div>
      <div class="toolbar-group">
        <UiButton icon="+" variant="primary" @click="openCreate">New deduction</UiButton>
      </div>
    </header>

    <UiCard title="Deductions" subtitle="Benefit premiums, garnishments, and other withholdings.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchDeductions">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading deductions…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="deductions.length" class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Paystub</th>
              <th>Deduction</th>
              <th class="amount-col">Amount</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="deduction in deductions" :key="deduction.DeductionID || deduction.deduction_id">
              <td>
                <div class="primary-cell">#{{ deduction.Paystub || deduction.paystub || '—' }}</div>
                <div class="secondary-cell">{{ resolvePaystubLabel(deduction.Paystub || deduction.paystub) }}</div>
              </td>
              <td>{{ deduction.DeductionName || deduction.deduction_name }}</td>
              <td class="amount-col">{{ formatCurrency(deduction.DeductionAmount ?? deduction.deduction_amount) }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editDeduction(deduction)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteDeduction(deduction.DeductionID || deduction.deduction_id)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No deductions recorded yet.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save deduction"
      :primary-loading="saving"
      @primary="saveDeduction"
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
          <UiFormField label="Deduction name" required>
            <input v-model="form.deduction_name" required placeholder="e.g., 401(k)" />
          </UiFormField>
        </div>
        <UiFormField label="Amount" required>
          <input v-model="form.deduction_amount" required type="number" step="0.01" min="0" />
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
  name: 'PayrollDeductions',
  components: { UiButton, UiCard, UiFormField, UiModal },
  data() {
    return {
      deductions: [],
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
      return this.editingId ? 'Edit deduction' : 'New deduction';
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
    this.fetchDeductions();
  },
  methods: {
    defaultForm() {
      return { paystub: '', deduction_name: '', deduction_amount: '' };
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
    normalizeDeductions(payload) {
      if (!Array.isArray(payload)) return [];
      return normalizeArray(payload).map((item) => ({
        ...item,
        paystub: item.paystub ?? item.Paystub ?? '',
        deduction_name: item.deduction_name ?? item.DeductionName ?? '',
        deduction_amount: item.deduction_amount ?? item.DeductionAmount ?? '',
      }));
    },
    async fetchDeductions() {
      this.loading = true;
      this.error = '';
      try {
        const { data } = await axios.get('/api/payroll/deductions/');
        let payload = data;
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }
        this.deductions = this.normalizeDeductions(Array.isArray(payload) ? payload : []);
      } catch (err) {
        console.error('Error fetching deductions:', err);
        this.error = 'Unable to load deductions right now.';
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
    editDeduction(deduction) {
      this.editingId = deduction.DeductionID ?? deduction.deduction_id;
      this.form = {
        paystub: deduction.Paystub ?? deduction.paystub ?? '',
        deduction_name: deduction.DeductionName ?? deduction.deduction_name ?? '',
        deduction_amount: deduction.DeductionAmount ?? deduction.deduction_amount ?? '',
      };
      this.showModal = true;
    },
    async saveDeduction() {
      this.saving = true;
      try {
        const body = {
          paystub: this.form.paystub,
          deduction_name: this.form.deduction_name,
          deduction_amount: this.form.deduction_amount,
        };
        let response;
        if (this.editingId) {
          response = await axios.put(`/api/payroll/deductions/${this.editingId}/`, body);
        } else {
          response = await axios.post('/api/payroll/deductions/', body);
        }
        const record = addPascalAliases(response.data);
        const normalized = {
          ...record,
          paystub: record.paystub ?? record.Paystub ?? body.paystub,
          deduction_name: record.deduction_name ?? record.DeductionName ?? body.deduction_name,
          deduction_amount: record.deduction_amount ?? record.DeductionAmount ?? body.deduction_amount,
        };
        if (this.editingId) {
          const index = this.deductions.findIndex((item) => (item.DeductionID ?? item.deduction_id) === this.editingId);
          if (index !== -1) this.$set(this.deductions, index, normalized);
        } else {
          this.deductions.unshift(normalized);
        }
        this.showModal = false;
      } catch (err) {
        console.error('Error saving deduction:', err);
        this.error = 'Failed to save deduction. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    async deleteDeduction(id) {
      if (!id || !confirm('Delete this deduction?')) return;
      try {
        await axios.delete(`/api/payroll/deductions/${id}/`);
        this.deductions = this.deductions.filter((item) => (item.DeductionID ?? item.deduction_id) !== id);
      } catch (err) {
        console.error('Error deleting deduction:', err);
        alert('Failed to delete deduction.');
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
