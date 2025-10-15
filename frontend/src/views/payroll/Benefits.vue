<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Payroll Benefits</h1>
        <p class="page-subtitle">Capture employer-sponsored benefits alongside payroll.</p>
      </div>
      <div class="toolbar-group">
        <UiButton icon="+" variant="primary" @click="openCreate">New benefit</UiButton>
      </div>
    </header>

    <UiCard title="Benefits" subtitle="Employer contributions and reimbursements by paystub.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchBenefits">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading benefits…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="benefits.length" class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Paystub</th>
              <th>Benefit</th>
              <th class="amount-col">Amount</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="benefit in benefits" :key="benefit.BenefitID || benefit.benefit_id">
              <td>
                <div class="primary-cell">#{{ benefit.Paystub || benefit.paystub || '—' }}</div>
                <div class="secondary-cell">{{ resolvePaystubLabel(benefit.Paystub || benefit.paystub) }}</div>
              </td>
              <td>{{ benefit.BenefitName || benefit.benefit_name }}</td>
              <td class="amount-col">{{ formatCurrency(benefit.BenefitAmount ?? benefit.benefit_amount) }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editBenefit(benefit)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteBenefit(benefit.BenefitID || benefit.benefit_id)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No benefits recorded yet.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save benefit"
      :primary-loading="saving"
      @primary="saveBenefit"
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
          <UiFormField label="Benefit name" required>
            <input v-model="form.benefit_name" required placeholder="e.g., Health Insurance" />
          </UiFormField>
        </div>
        <UiFormField label="Amount" required>
          <input v-model="form.benefit_amount" required type="number" step="0.01" min="0" />
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
  name: 'PayrollBenefits',
  components: { UiButton, UiCard, UiFormField, UiModal },
  data() {
    return {
      benefits: [],
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
      return this.editingId ? 'Edit benefit' : 'New benefit';
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
    this.fetchBenefits();
  },
  methods: {
    defaultForm() {
      return { paystub: '', benefit_name: '', benefit_amount: '' };
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
    normalizeBenefits(payload) {
      if (!Array.isArray(payload)) return [];
      return normalizeArray(payload).map((item) => ({
        ...item,
        paystub: item.paystub ?? item.Paystub ?? '',
        benefit_name: item.benefit_name ?? item.BenefitName ?? '',
        benefit_amount: item.benefit_amount ?? item.BenefitAmount ?? '',
      }));
    },
    async fetchBenefits() {
      this.loading = true;
      this.error = '';
      try {
        const { data } = await axios.get('/api/payroll/benefits/');
        let payload = data;
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }
        this.benefits = this.normalizeBenefits(Array.isArray(payload) ? payload : []);
      } catch (err) {
        console.error('Error fetching benefits:', err);
        this.error = 'Unable to load benefits right now.';
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
    editBenefit(benefit) {
      this.editingId = benefit.BenefitID ?? benefit.benefit_id;
      this.form = {
        paystub: benefit.Paystub ?? benefit.paystub ?? '',
        benefit_name: benefit.BenefitName ?? benefit.benefit_name ?? '',
        benefit_amount: benefit.BenefitAmount ?? benefit.benefit_amount ?? '',
      };
      this.showModal = true;
    },
    async saveBenefit() {
      this.saving = true;
      try {
        const body = {
          paystub: this.form.paystub,
          benefit_name: this.form.benefit_name,
          benefit_amount: this.form.benefit_amount,
        };
        let response;
        if (this.editingId) {
          response = await axios.put(`/api/payroll/benefits/${this.editingId}/`, body);
        } else {
          response = await axios.post('/api/payroll/benefits/', body);
        }
        const record = addPascalAliases(response.data);
        const normalized = {
          ...record,
          paystub: record.paystub ?? record.Paystub ?? body.paystub,
          benefit_name: record.benefit_name ?? record.BenefitName ?? body.benefit_name,
          benefit_amount: record.benefit_amount ?? record.BenefitAmount ?? body.benefit_amount,
        };
        if (this.editingId) {
          const index = this.benefits.findIndex((item) => (item.BenefitID ?? item.benefit_id) === this.editingId);
          if (index !== -1) this.$set(this.benefits, index, normalized);
        } else {
          this.benefits.unshift(normalized);
        }
        this.showModal = false;
      } catch (err) {
        console.error('Error saving benefit:', err);
        this.error = 'Failed to save benefit. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    async deleteBenefit(id) {
      if (!id || !confirm('Delete this benefit?')) return;
      try {
        await axios.delete(`/api/payroll/benefits/${id}/`);
        this.benefits = this.benefits.filter((item) => (item.BenefitID ?? item.benefit_id) !== id);
      } catch (err) {
        console.error('Error deleting benefit:', err);
        alert('Failed to delete benefit.');
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
