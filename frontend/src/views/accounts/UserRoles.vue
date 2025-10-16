<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">User Roles</h1>
        <p class="page-subtitle">Control which companies you can access and the role assigned to each.</p>
      </div>
      <div class="toolbar-group">
        <UiButton icon="+" variant="primary" @click="openCreate">Assign role</UiButton>
      </div>
    </header>

    <UiCard title="Company Roles" subtitle="Your access across the organizations in Lifeline.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchRoles">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading user roles…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="roles.length" class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Role</th>
              <th>Assigned</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="role in roles" :key="role.UserCompanyRoleID || role.user_company_role_id">
              <td>
                <div class="primary-cell">{{ role.Company?.CompanyName || 'Unknown company' }}</div>
                <div class="secondary-cell">ID: {{ role.CompanyID }}</div>
              </td>
              <td>{{ role.Role }}</td>
              <td>{{ formatDate(role.CreatedDate) }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editRole(role)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteRole(role)">Remove</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No roles assigned yet.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save role"
      :primary-loading="saving"
      @primary="saveRole"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Company" required>
            <select v-model="form.CompanyID" required>
              <option disabled value="">Select company</option>
              <option v-for="company in companyOptions" :key="company.value" :value="company.value">
                {{ company.label }}
              </option>
            </select>
          </UiFormField>
          <UiFormField label="Role" required>
            <input v-model.trim="form.Role" required placeholder="e.g., Administrator" />
          </UiFormField>
        </div>
      </form>
    </UiModal>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';
import { normalizeArray, addPascalAliases } from '@/services/normalizeApi';

export default {
  name: 'UserRolesView',
  components: { UiButton, UiCard, UiFormField, UiModal },
  data() {
    return {
      roles: [],
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      editingId: null,
      form: this.defaultForm(),
    };
  },
  computed: {
    ...mapState(['user']),
    modalTitle() {
      return this.editingId ? 'Edit role' : 'Assign role';
    },
    companiesFromUser() {
      return this.user?.companies || [];
    },
    companyOptions() {
      return this.companiesFromUser.map((company) => ({
        value: company.CompanyID ?? company.company_id,
        label: company.CompanyName || company.company_name,
      }));
    },
  },
  async mounted() {
    if (!this.companiesFromUser.length) {
      try {
        await this.$store.dispatch('loadCompanies');
      } catch (err) {
        console.warn('Unable to load companies for role selector:', err);
      }
    }
    this.fetchRoles();
  },
  methods: {
    defaultForm() {
      return { CompanyID: '', Role: '' };
    },
    formatDate(value) {
      if (!value) return '—';
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return value;
      return date.toLocaleDateString();
    },
    normalizeRoles(payload) {
      if (!Array.isArray(payload)) return [];
      return normalizeArray(payload).map((item) => ({
        ...item,
        CompanyID: item.CompanyID ?? item.company_id,
        Role: item.Role ?? item.role,
      }));
    },
    async fetchRoles() {
      this.loading = true;
      this.error = '';
      try {
        const { data } = await axios.get('/api/accounts/user-company-roles/');
        let payload = data;
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }
        this.roles = this.normalizeRoles(Array.isArray(payload) ? payload : []);
      } catch (err) {
        console.error('Error fetching user roles:', err);
        this.error = 'Unable to load user roles right now.';
      } finally {
        this.loading = false;
      }
    },
    openCreate() {
      this.editingId = null;
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editRole(role) {
      this.editingId = role.UserCompanyRoleID ?? role.user_company_role_id;
      this.form = {
        CompanyID: role.CompanyID,
        Role: role.Role,
      };
      this.showModal = true;
    },
    async saveRole() {
      this.saving = true;
      try {
        const payload = { CompanyID: this.form.CompanyID, Role: this.form.Role };
        let response;
        if (this.editingId) {
          response = await axios.put(`/api/accounts/user-company-roles/${this.editingId}/`, payload);
        } else {
          response = await axios.post('/api/accounts/user-company-roles/', payload);
        }
        const record = addPascalAliases(response.data);
        const normalized = {
          ...record,
          CompanyID: record.CompanyID ?? payload.CompanyID,
          Role: record.Role ?? payload.Role,
        };
        if (this.editingId) {
          const index = this.roles.findIndex((role) => (role.UserCompanyRoleID ?? role.user_company_role_id) === this.editingId);
          if (index !== -1) this.$set(this.roles, index, normalized);
        } else {
          this.roles.unshift(normalized);
        }
        this.showModal = false;
      } catch (err) {
        console.error('Error saving role:', err);
        this.error = 'Unable to save role. Please try again.';
      } finally {
        this.saving = false;
      }
    },
    async deleteRole(role) {
      const id = role.UserCompanyRoleID ?? role.user_company_role_id;
      if (!id || !confirm('Remove this role?')) return;
      try {
        await axios.delete(`/api/accounts/user-company-roles/${id}/`);
        this.roles = this.roles.filter((item) => (item.UserCompanyRoleID ?? item.user_company_role_id) !== id);
      } catch (err) {
        console.error('Error deleting role:', err);
        alert('Failed to delete role.');
      }
    },
  },
};
</script>

<style scoped>
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
