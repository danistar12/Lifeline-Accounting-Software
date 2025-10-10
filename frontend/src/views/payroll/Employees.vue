<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Employees</h1>
        <p class="page-subtitle">Manage your team members and their employment details.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input
              v-model="searchTerm"
              type="search"
              placeholder="Search employees..."
              @input="filterEmployees"
            />
          </UiFormField>
        </div>
        <UiFormField label="Department">
          <select v-model="departmentFilter" @change="filterEmployees">
            <option value="">All departments</option>
            <option v-for="dept in departments" :key="dept" :value="dept">
              {{ dept }}
            </option>
          </select>
        </UiFormField>
        <UiButton icon="+" variant="primary" @click="openCreate">
          New employee
        </UiButton>
      </div>
    </header>

    <UiCard title="Team members" subtitle="Active employees and their contact information.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchEmployees">
          Refresh
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading employees…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filteredEmployees.length" class="table-container">
        <table class="data-table employees-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Hire date</th>
              <th>Department</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="employee in filteredEmployees" :key="employee.id">
              <td>
                <div class="employee-name">{{ employee.first_name }} {{ employee.last_name }}</div>
                <div class="employee-meta">{{ employee.employee_id }}</div>
              </td>
              <td>{{ employee.email }}</td>
              <td>{{ employee.phone_number || '—' }}</td>
              <td>{{ formatDate(employee.hire_date) }}</td>
              <td>{{ employee.department || '—' }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editEmployee(employee)">
                  Edit
                </UiButton>
                <UiButton size="sm" variant="danger" @click="deleteEmployee(employee.id)">
                  Delete
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No employees found.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save employee"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="First name" required>
            <input v-model="form.first_name" required />
          </UiFormField>
          <UiFormField label="Last name" required>
            <input v-model="form.last_name" required />
          </UiFormField>
          <UiFormField label="Email" required>
            <input v-model="form.email" type="email" required />
          </UiFormField>
          <UiFormField label="Phone number">
            <input v-model="form.phone_number" type="tel" />
          </UiFormField>
          <UiFormField label="Hire date" required>
            <input v-model="form.hire_date" type="date" required />
          </UiFormField>
          <UiFormField label="Department">
            <select v-model="form.department">
              <option value="">Select department</option>
              <option value="Engineering">Engineering</option>
              <option value="Sales">Sales</option>
              <option value="Marketing">Marketing</option>
              <option value="HR">HR</option>
              <option value="Finance">Finance</option>
              <option value="Operations">Operations</option>
            </select>
          </UiFormField>
        </div>
        <UiFormField label="Notes">
          <textarea v-model="form.notes" rows="3" placeholder="Additional notes..." />
        </UiFormField>
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
  name: 'EmployeesView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
  },
  data() {
    return {
      employees: [],
      filteredEmployees: [],
      departments: ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
      searchTerm: '',
      departmentFilter: '',
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    modalTitle() {
      return this.form.id ? 'Edit employee' : 'New employee';
    },
  },
  mounted() {
    this.fetchEmployees();
  },
  methods: {
    defaultForm() {
      return {
        id: null,
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        hire_date: '',
        department: '',
        notes: '',
      };
    },
    async fetchEmployees() {
      this.loading = true;
      this.error = '';
      try {
        const response = await apiClient.get('/payroll/employees/');
        const payload = Array.isArray(response.data) ? response.data : [];
        this.employees = payload.map((employee) => ({
          ...employee,
          id: employee.id ?? employee.employee_id,
        }));
        this.filteredEmployees = [...this.employees];
      } catch (error) {
        console.error('Error fetching employees:', error);
        this.error = 'Unable to load employees right now.';
      } finally {
        this.loading = false;
      }
    },
    filterEmployees() {
      let filtered = [...this.employees];

      // Filter by department
      if (this.departmentFilter) {
        filtered = filtered.filter((employee) =>
          employee.department === this.departmentFilter
        );
      }

      // Filter by search term
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter((employee) =>
          `${employee.first_name} ${employee.last_name}`.toLowerCase().includes(term) ||
          employee.email?.toLowerCase().includes(term) ||
          employee.employee_id?.toString().includes(term)
        );
      }

      this.filteredEmployees = filtered;
    },
    openCreate() {
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editEmployee(employee) {
      this.form = {
        id: employee.id,
        first_name: employee.first_name || '',
        last_name: employee.last_name || '',
        email: employee.email || '',
        phone_number: employee.phone_number || '',
        hire_date: employee.hire_date || '',
        department: employee.department || '',
        notes: employee.notes || '',
      };
      this.showModal = true;
    },
    async deleteEmployee(employeeId) {
      if (!employeeId) return;

      const confirmed = window.confirm('Delete this employee? This action cannot be undone.');
      if (!confirmed) return;

      try {
        await apiClient.delete(`/payroll/employees/${employeeId}/`);
        this.employees = this.employees.filter((employee) => employee.id !== employeeId);
        this.filterEmployees();
      } catch (error) {
        console.error('Error deleting employee:', error);
        this.error = 'Unable to delete that employee.';
      }
    },
    async save() {
      if (!this.form.first_name || !this.form.last_name || !this.form.email || !this.form.hire_date) {
        return;
      }

      this.saving = true;
      const payload = {
        first_name: this.form.first_name,
        last_name: this.form.last_name,
        email: this.form.email,
        phone_number: this.form.phone_number || undefined,
        hire_date: this.form.hire_date,
        department: this.form.department || undefined,
        notes: this.form.notes || undefined,
      };

      try {
        if (this.form.id) {
          await apiClient.put(`/payroll/employees/${this.form.id}/`, payload);
        } else {
          await apiClient.post('/payroll/employees/', payload);
        }

        await this.fetchEmployees();
        this.showModal = false;
        this.form = this.defaultForm();
      } catch (error) {
        console.error('Error saving employee:', error);
        this.error = 'Unable to save that employee.';
      } finally {
        this.saving = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '—';
      return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(dateString));
    },
  },
};
</script>

<style scoped>
.toolbar-search :deep(.ui-form-field) {
  min-width: 220px;
}

.toolbar-group :deep(.ui-form-field) {
  min-width: 140px;
}

.employees-table .actions-col {
  width: 160px;
}

.employee-name {
  font-weight: 600;
  color: var(--color-text);
}

.employee-meta {
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

.modal-form {
  padding-top: 4px;
}

@media (min-width: 640px) {
  .form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
