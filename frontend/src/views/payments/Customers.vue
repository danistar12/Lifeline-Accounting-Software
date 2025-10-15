<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Customers</h1>
        <p class="page-subtitle">Manage your customer database and contact information.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input
              v-model="searchTerm"
              type="search"
              placeholder="Search customers..."
              @input="filterCustomers"
            />
          </UiFormField>
        </div>
        <UiButton icon="+" variant="primary" @click="openCreate">
          New customer
        </UiButton>
      </div>
    </header>

    <UiCard title="Customers" subtitle="List of all customers with contact details.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchCustomers">
          Refresh
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading customers…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filteredCustomers.length" class="table-container">
        <table class="data-table customers-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in filteredCustomers" :key="customer.CustomerID">
              <td>
                <div class="customer-name">{{ customer.Name }}</div>
              </td>
              <td>{{ customer.Email || '—' }}</td>
              <td>{{ customer.Phone || '—' }}</td>
              <td>{{ customer.Address || '—' }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="viewCustomer(customer)">
                  View
                </UiButton>
                <UiButton size="sm" variant="ghost" @click="editCustomer(customer)">
                  Edit
                </UiButton>
                <UiButton size="sm" variant="danger" @click="deleteCustomer(customer.CustomerID)">
                  Delete
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No customers found.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save customer"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Name" required>
            <input v-model="form.Name" required />
          </UiFormField>
          <UiFormField label="Email">
            <input v-model="form.Email" type="email" />
          </UiFormField>
          <UiFormField label="Phone">
            <input v-model="form.Phone" type="tel" />
          </UiFormField>
          <UiFormField label="Payment Terms">
            <input v-model="form.PaymentTerms" placeholder="e.g., Net 30" />
          </UiFormField>
        </div>
        <UiFormField label="Address">
          <textarea v-model="form.Address" rows="2" placeholder="Street address..." />
        </UiFormField>
        <UiFormField label="Notes">
          <textarea v-model="form.CustomerNotes" rows="3" placeholder="Additional notes..." />
        </UiFormField>
      </form>
    </UiModal>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';
import { normalizeArray } from '@/services/normalizeApi';

export default {
  name: 'CustomersView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
  },
  data() {
    return {
      customers: [],
      filteredCustomers: [],
      searchTerm: '',
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    ...mapGetters(['selectedCompanyId']),
    modalTitle() {
      return this.form.CustomerID ? 'Edit customer' : 'New customer';
    },
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    defaultForm() {
      const companyId = this.selectedCompanyId ? Number(this.selectedCompanyId) : null;
      return {
        CustomerID: null,
        CompanyID: companyId,
        Name: '',
        Email: '',
        Phone: '',
        Address: '',
        PaymentTerms: '',
        CustomerNotes: '',
      };
    },
    async fetchCustomers() {
      this.loading = true;
      this.error = '';
      try {
        const response = await axios.get('/api/customers/');
        const payload = response.data || [];
        this.customers = normalizeArray(payload);
        this.filteredCustomers = [...this.customers];
      } catch (error) {
        console.error('Error fetching customers:', error);
        this.error = 'Unable to load customers right now.';
      } finally {
        this.loading = false;
      }
    },
    filterCustomers() {
      let filtered = [...this.customers];

      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter(customer =>
          (customer.Name || '').toString().toLowerCase().includes(term) ||
          (customer.Email || '').toString().toLowerCase().includes(term)
        );
      }

      this.filteredCustomers = filtered;
    },
    openCreate() {
      this.form = this.defaultForm();
      if (!this.form.CompanyID && this.customers.length) {
        this.form.CompanyID = this.customers[0].CompanyID ?? null;
      }
      this.showModal = true;
    },
    editCustomer(customer) {
      this.form = {
        CustomerID: customer.CustomerID ?? null,
  CompanyID: customer.CompanyID ?? (this.selectedCompanyId ? Number(this.selectedCompanyId) : null),
        Name: customer.Name || '',
        Email: customer.Email || '',
        Phone: customer.Phone || '',
        Address: customer.Address || '',
        PaymentTerms: customer.PaymentTerms || '',
        CustomerNotes: customer.CustomerNotes || '',
      };
      this.showModal = true;
    },
    viewCustomer(customer) {
      // TODO: Navigate to customer detail view
      console.log('View customer:', customer);
    },
    async deleteCustomer(customerId) {
      if (!confirm('Are you sure you want to delete this customer?')) return;
      try {
        await axios.delete(`/api/customers/${customerId}/`);
        this.fetchCustomers();
      } catch (error) {
        console.error('Error deleting customer:', error);
        alert('Failed to delete customer.');
      }
    },
    async save() {
      this.saving = true;
      try {
        const payload = {
          ...this.form,
        };

        if (!payload.CompanyID && this.selectedCompanyId) {
          payload.CompanyID = Number(this.selectedCompanyId);
        }

        const { CustomerID, ...body } = payload;

        if (CustomerID) {
          await axios.put(`/api/customers/${CustomerID}/`, body);
        } else {
          await axios.post('/api/customers/', body);
        }
        this.showModal = false;
        this.fetchCustomers();
      } catch (error) {
        console.error('Error saving customer:', error);
        alert('Failed to save customer.');
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.toolbar-group {
  align-items: flex-end;
}

.customers-table .customer-name {
  font-weight: 600;
  color: #2c3e50;
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

