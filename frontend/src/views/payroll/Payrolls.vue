<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Payroll runs</h1>
        <p class="page-subtitle">Schedule, approve, and publish upcoming payroll cycles.</p>
      </div>
      <UiButton icon="+" variant="primary" @click="openCreate">
        New payroll run
      </UiButton>
    </header>

    <UiCard title="Scheduled runs" subtitle="Keep pay cycles on track for your team.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchPayrolls">
          Refresh
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading payrolls…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="payrolls.length" class="table-container">
        <table class="data-table payroll-table">
          <thead>
            <tr>
              <th>Run date</th>
              <th>Pay period</th>
              <th class="is-numeric">Employees</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payroll in payrolls" :key="payroll.id">
              <td>
                <div class="run-date">{{ formatDate(payroll.run_date) }}</div>
                <div class="run-meta">Submitted {{ relativeTime(payroll.created_at) }}</div>
              </td>
              <td>
                <div>{{ formatDate(payroll.pay_period_start) }} → {{ formatDate(payroll.pay_period_end) }}</div>
                <div class="run-meta">{{ payPeriodLength(payroll) }}</div>
              </td>
              <td class="is-numeric">{{ payroll.employee_count ?? '—' }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editPayroll(payroll)">
                  Edit
                </UiButton>
                <UiButton size="sm" variant="danger" @click="deletePayroll(payroll.id)">
                  Delete
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No payroll runs yet. Schedule one to get started.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save run"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Run date" required>
            <input v-model="form.run_date" type="date" required />
          </UiFormField>
          <UiFormField label="Employees included" hint="Optional headcount for tracking">
            <input v-model.number="form.employee_count" type="number" min="0" />
          </UiFormField>
          <UiFormField label="Pay period start" required>
            <input v-model="form.pay_period_start" type="date" required />
          </UiFormField>
          <UiFormField label="Pay period end" required>
            <input v-model="form.pay_period_end" type="date" required />
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
  name: 'PayrollsView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
  },
  data() {
    return {
      payrolls: [],
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    modalTitle() {
      return this.form.id ? 'Edit payroll run' : 'New payroll run';
    },
  },
  mounted() {
    this.fetchPayrolls();
  },
  methods: {
    defaultForm() {
      return {
        id: null,
        run_date: '',
        pay_period_start: '',
        pay_period_end: '',
        employee_count: null,
      };
    },
    async fetchPayrolls() {
      this.loading = true;
      this.error = '';
      try {
        const response = await apiClient.get('/payroll/payrolls/');
        const payload = Array.isArray(response.data) ? response.data : [];
        this.payrolls = payload.map((entry) => ({
          ...entry,
          id: entry.id ?? entry.payroll_id,
        }));
      } catch (error) {
        console.error('Error fetching payrolls:', error);
        this.error = 'Unable to load payroll runs right now.';
      } finally {
        this.loading = false;
      }
    },
    openCreate() {
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editPayroll(payroll) {
      this.form = {
        id: payroll.id,
        run_date: payroll.run_date,
        pay_period_start: payroll.pay_period_start,
        pay_period_end: payroll.pay_period_end,
        employee_count: payroll.employee_count ?? null,
      };
      this.showModal = true;
    },
    async deletePayroll(payrollId) {
      if (!payrollId) return;

      const confirmed = window.confirm('Delete this payroll run? This action cannot be undone.');
      if (!confirmed) return;

      try {
        await apiClient.delete(`/payroll/payrolls/${payrollId}/`);
        this.payrolls = this.payrolls.filter((payroll) => payroll.id !== payrollId);
      } catch (error) {
        console.error('Error deleting payroll:', error);
        this.error = 'Unable to delete that run. Please try again later.';
      }
    },
    async save() {
      if (!this.form.run_date || !this.form.pay_period_start || !this.form.pay_period_end) {
        return;
      }

      this.saving = true;
      const payload = {
        run_date: this.form.run_date,
        pay_period_start: this.form.pay_period_start,
        pay_period_end: this.form.pay_period_end,
        employee_count: this.form.employee_count ?? undefined,
      };

      try {
        if (this.form.id) {
          await apiClient.put(`/payroll/payrolls/${this.form.id}/`, payload);
        } else {
          await apiClient.post('/payroll/payrolls/', payload);
        }

        await this.fetchPayrolls();
        this.showModal = false;
        this.form = this.defaultForm();
      } catch (error) {
        console.error('Error saving payroll:', error);
        this.error = 'Unable to save that payroll run.';
      } finally {
        this.saving = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '—';
      return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(dateString));
    },
    relativeTime(dateString) {
      if (!dateString) return '—';
      const formatter = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' });
      const diffMs = new Date(dateString) - new Date();
      const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
      return formatter.format(diffDays, 'day');
    },
    payPeriodLength(payroll) {
      if (!payroll.pay_period_start || !payroll.pay_period_end) return '';
      const start = new Date(payroll.pay_period_start);
      const end = new Date(payroll.pay_period_end);
      const diffDays = (end - start) / (1000 * 60 * 60 * 24) + 1;
      return `${diffDays} day period`;
    },
  },
};
</script>

<style scoped>
.payroll-table .actions-col {
  width: 160px;
}

.run-date {
  font-weight: 600;
}

.run-meta {
  color: var(--color-text-muted);
  font-size: 0.82rem;
  margin-top: 4px;
}

.table-empty--error {
  color: var(--color-danger);
}

.form-grid {
  display: grid;
  gap: 16px;
}

@media (min-width: 640px) {
  .form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
