<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Paystubs</h1>
        <p class="page-subtitle">Manage employee paystubs and compensation details.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input v-model="searchTerm" type="search" placeholder="Search paystubs..." @input="filterPaystubs" />
          </UiFormField>
        </div>
        <UiButton icon="+" variant="primary" @click="openCreate">New Paystub</UiButton>
      </div>
    </header>

    <UiCard title="Employee Paystubs" subtitle="Payroll compensation records for all employees.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchPaystubs">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading paystubs…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filteredPaystubs.length" class="table-container">
        <table class="data-table paystubs-table">
          <thead>
            <tr>
              <th>Employee</th>
              <th>Payroll Period</th>
              <th>Gross Pay</th>
              <th>Net Pay</th>
              <th>Status</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="paystub in filteredPaystubs" :key="paystub.PaystubID || paystub.id">
              <td>{{ paystub.EmployeeName || paystub.employee_name }}</td>
              <td>{{ formatDate(paystub.PayPeriodStart || paystub.pay_period_start) }} - {{ formatDate(paystub.PayPeriodEnd || paystub.pay_period_end) }}</td>
              <td class="is-numeric">{{ formatCurrency(paystub.GrossPay ?? paystub.gross_pay) }}</td>
              <td class="is-numeric">{{ formatCurrency(paystub.NetPay ?? paystub.net_pay) }}</td>
              <td>
                <UiStatusBadge :status="(paystub.Status || paystub.status) === 'paid' ? 'success' : 'info'">{{ paystub.Status || paystub.status }}</UiStatusBadge>
              </td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="viewPaystub(paystub)">View</UiButton>
                <UiButton size="sm" variant="ghost" @click="editPaystub(paystub)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deletePaystub(paystub.id)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No paystubs found.</div>
    </UiCard>

    <UiModal v-model="showModal" :title="modalTitle" primary-label="Save Paystub" :primary-loading="saving" @primary="save">
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Employee" required>
            <select v-model="form.employee_id" required>
              <option value="">Select employee</option>
              <option v-for="employee in employees" :key="employee.id" :value="employee.id">{{ employee.first_name }} {{ employee.last_name }}</option>
            </select>
          </UiFormField>

          <UiFormField label="Payroll Run">
            <select v-model="form.payroll_id">
              <option value="">Select payroll run</option>
              <option v-for="payroll in payrolls" :key="payroll.id" :value="payroll.id">{{ formatDate(payroll.run_date) }}</option>
            </select>
          </UiFormField>

          <UiFormField label="Pay Period Start" required>
            <input v-model="form.pay_period_start" type="date" required />
          </UiFormField>

          <UiFormField label="Pay Period End" required>
            <input v-model="form.pay_period_end" type="date" required />
          </UiFormField>

          <UiFormField label="Gross Pay" required>
            <input v-model="form.gross_pay" type="number" step="0.01" required />
          </UiFormField>

          <UiFormField label="Net Pay" required>
            <input v-model="form.net_pay" type="number" step="0.01" required />
          </UiFormField>

          <UiFormField label="Status">
            <select v-model="form.status">
              <option value="draft">Draft</option>
              <option value="paid">Paid</option>
            </select>
          </UiFormField>
        </div>
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
import UiStatusBadge from '@/components/ui/UiStatusBadge.vue';

export default {
  name: 'PaystubsView',
  components: { UiButton, UiCard, UiFormField, UiModal, UiStatusBadge },
  data() {
    return {
      paystubs: [],
      filteredPaystubs: [],
      employees: [],
      payrolls: [],
      searchTerm: '',
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    modalTitle() {
      return this.form.id ? 'Edit Paystub' : 'New Paystub';
    },
  },
  mounted() {
    this.fetchPaystubs();
    this.fetchEmployees();
    this.fetchPayrolls();
  },
  methods: {
    defaultForm() {
      return { id: null, employee_id: '', payroll_id: '', pay_period_start: '', pay_period_end: '', gross_pay: '', net_pay: '', status: 'draft' };
    },
    async fetchPaystubs() {
      this.loading = true;
      this.error = '';
      try {
        const res = await axios.get('/api/payroll/paystubs/');
        const payload = res.data || [];
        this.paystubs = payload.map((p) => {
          const n = { ...p };
          n.PaystubID = p.PaystubID ?? p.id;
          n.PayrollID = p.PayrollID ?? p.payroll_id ?? p.payrollId;
          n.EmployeeID = p.EmployeeID ?? p.employee_id;
          n.EmployeeName = (p.EmployeeName ?? p.employee_name ?? (p.EmployeeID && p.EmployeeID.Name)) || p.employee_name;
          n.PayPeriodStart = p.PayPeriodStart ?? p.pay_period_start;
          n.PayPeriodEnd = p.PayPeriodEnd ?? p.pay_period_end;
          n.GrossPay = p.GrossPay ?? p.gross_pay;
          n.NetPay = p.NetPay ?? p.net_pay;
          n.Status = p.Status ?? p.status;
          return n;
        });
        this.filteredPaystubs = [...this.paystubs];
      } catch (err) {
        console.error('Error fetching paystubs:', err);
        this.error = 'Unable to load paystubs right now.';
      } finally {
        this.loading = false;
      }
    },
    async fetchEmployees() {
      try {
        const res = await axios.get('/api/payroll/employees/');
        this.employees = res.data || [];
      } catch (err) {
        console.error('Error fetching employees:', err);
      }
    },
    async fetchPayrolls() {
      try {
        const res = await axios.get('/api/payroll/payrolls/');
        this.payrolls = res.data || [];
      } catch (err) {
        console.error('Error fetching payrolls:', err);
      }
    },
    filterPaystubs() {
      let filtered = [...this.paystubs];
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter(p => p.employee_name && p.employee_name.toLowerCase().includes(term));
      }
      this.filteredPaystubs = filtered;
    },
    openCreate() {
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editPaystub(paystub) {
      this.form = { ...paystub };
      this.showModal = true;
    },
    viewPaystub(paystub) {
      console.log('View paystub:', paystub);
    },
    async deletePaystub(id) {
      if (!confirm('Are you sure you want to delete this paystub?')) return;
      try {
        await axios.delete(`/api/payroll/paystubs/${id}/`);
        this.fetchPaystubs();
      } catch (err) {
        console.error('Error deleting paystub:', err);
        alert('Failed to delete paystub.');
      }
    },
    async save() {
      this.saving = true;
      try {
        if (this.form.id) await axios.put(`/api/payroll/paystubs/${this.form.id}/`, this.form);
        else await axios.post('/api/payroll/paystubs/', this.form);
        this.showModal = false;
        this.fetchPaystubs();
      } catch (err) {
        console.error('Error saving paystub:', err);
        alert('Failed to save paystub.');
      } finally { this.saving = false; }
    },
    formatDate(date) { if (!date) return ''; return new Date(date).toLocaleDateString(); },
    formatCurrency(amount) { if (typeof amount !== 'number') return amount; return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' }); },
  },
};
</script>

<style scoped>
.toolbar-group { align-items: flex-end; }
.paystubs-table .employee-name { font-weight: 600; color: #2c3e50; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
@media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } }
</style>
