<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Invoices</h1>
        <p class="page-subtitle">Manage your customer invoices and track payments.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input
              v-model="searchTerm"
              type="search"
              placeholder="Search invoices..."
              @input="filterInvoices"
            />
          </UiFormField>
        </div>
        <UiFormField label="Status">
          <select v-model="statusFilter" @change="filterInvoices">
            <option value="">All statuses</option>
            <option value="Draft">Draft</option>
            <option value="Sent">Sent</option>
            <option value="Paid">Paid</option>
            <option value="Overdue">Overdue</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </UiFormField>
        <UiButton icon="+" variant="primary" @click="openCreate">
          New invoice
        </UiButton>
      </div>
    </header>

    <UiCard title="Customer invoices" subtitle="Outstanding and paid invoices with customer details.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchInvoices">
          Refresh
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading invoices…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filteredInvoices.length" class="table-container">
        <table class="data-table invoices-table">
          <thead>
            <tr>
              <th>Invoice #</th>
              <th>Customer</th>
              <th>Date</th>
              <th>Due Date</th>
              <th>Amount</th>
              <th>Status</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="invoice in filteredInvoices" :key="invoice.InvoiceID">
              <td>
                <div class="invoice-number">{{ invoice.InvoiceNumber }}</div>
              </td>
              <td>{{ invoice.CustomerName }}</td>
              <td>{{ formatDate(invoice.InvoiceDate) }}</td>
              <td>{{ formatDate(invoice.DueDate) }}</td>
              <td class="amount">{{ formatCurrency(invoice.TotalAmount) }}</td>
              <td>
                <span :class="`status-badge status-${(invoice.Status || invoice.status || '').toString().toLowerCase()}`">
                  {{ invoice.Status || invoice.status || 'Unknown' }}
                </span>
              </td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="viewInvoice(invoice)">
                  View
                </UiButton>
                <UiButton size="sm" variant="ghost" @click="editInvoice(invoice)">
                  Edit
                </UiButton>
                <UiButton
                  v-if="invoice.Status !== 'Paid'"
                  size="sm"
                  variant="success"
                  @click="markAsPaid(invoice)"
                >
                  Mark Paid
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No invoices found.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save invoice"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Invoice Number" required>
            <input v-model="form.InvoiceNumber" required />
          </UiFormField>
          <UiFormField label="Customer" required>
            <select v-model="form.CustomerID" required>
              <option value="">Select customer</option>
              <option v-for="customer in customers" :key="customer.id" :value="customer.id">
                {{ customer.name }}
              </option>
            </select>
          </UiFormField>
          <UiFormField label="Invoice Date" required>
            <input v-model="form.InvoiceDate" type="date" required />
          </UiFormField>
          <UiFormField label="Due Date" required>
            <input v-model="form.DueDate" type="date" required />
          </UiFormField>
          <UiFormField label="Total Amount" required>
            <input v-model="form.TotalAmount" type="number" step="0.01" required />
          </UiFormField>
          <UiFormField label="Status">
            <select v-model="form.Status">
              <option value="Draft">Draft</option>
              <option value="Sent">Sent</option>
              <option value="Paid">Paid</option>
              <option value="Overdue">Overdue</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </UiFormField>
          <UiFormField label="Currency Code">
            <input v-model="form.CurrencyCode" placeholder="USD" />
          </UiFormField>
        </div>
        <UiFormField label="Notes">
          <textarea v-model="form.InvoiceNotes" rows="3" placeholder="Additional notes..." />
        </UiFormField>
      </form>
    </UiModal>
  </div>
</template>

<script>
import axios from 'axios';
import { normalizeArray } from '@/services/normalizeApi';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';

export default {
  name: 'InvoicesView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
  },
  data() {
    return {
      invoices: [],
      filteredInvoices: [],
      customers: [],
      searchTerm: '',
      statusFilter: '',
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    modalTitle() {
      return this.form.InvoiceID ? 'Edit invoice' : 'New invoice';
    },
  },
  mounted() {
    this.fetchInvoices();
    this.fetchCustomers();
  },
  methods: {
    defaultForm() {
      return {
        InvoiceID: null,
        InvoiceNumber: '',
        CustomerID: '',
        InvoiceDate: new Date().toISOString().split('T')[0],
        DueDate: '',
        TotalAmount: '',
        Status: 'Draft',
        CurrencyCode: 'USD',
        InvoiceNotes: '',
      };
    },
    async fetchInvoices() {
      this.loading = true;
      this.error = '';
      try {
        const response = await axios.get('/api/invoices/');
        let payload = response.data;

        // handle paginated or nested responses: { results: [...] } or { data: [...] }
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }

        if (!Array.isArray(payload)) {
          // if it's a single object, wrap it; otherwise ensure it's an array
          payload = payload ? [payload] : [];
        }

        this.invoices = normalizeArray(payload);
        this.filteredInvoices = [...this.invoices];
      } catch (error) {
        console.error('Error fetching invoices:', error);
        this.error = 'Unable to load invoices right now.';
      } finally {
        this.loading = false;
      }
    },
    async fetchCustomers() {
      try {
        const response = await axios.get('/api/customers/');
        let payload = response.data;
        if (payload && typeof payload === 'object' && !Array.isArray(payload)) {
          if (Array.isArray(payload.results)) payload = payload.results;
          else if (Array.isArray(payload.data)) payload = payload.data;
        }
        if (!Array.isArray(payload)) payload = payload ? [payload] : [];
        this.customers = normalizeArray(payload);
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    },
    filterInvoices() {
      let filtered = Array.isArray(this.invoices) ? [...this.invoices] : [];

      if (this.statusFilter) {
        filtered = filtered.filter(invoice => (invoice.Status || '').toString() === this.statusFilter);
      }

      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter((invoice) => {
          const invNum = (invoice.InvoiceNumber || invoice.invoice_number || '')?.toString().toLowerCase();
          const cust = (invoice.CustomerName || invoice.customer_name || '')?.toString().toLowerCase();
          return invNum.includes(term) || cust.includes(term);
        });
      }

      this.filteredInvoices = filtered;
    },
    openCreate() {
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editInvoice(invoice) {
      this.form = { ...invoice };
      this.showModal = true;
    },
    viewInvoice(invoice) {
      // TODO: Navigate to invoice detail view
      console.log('View invoice:', invoice);
    },
    async markAsPaid(invoice) {
      try {
        await axios.post(`/api/invoices/${invoice.InvoiceID}/mark_paid/`);
        invoice.Status = 'Paid';
        this.filterInvoices();
      } catch (error) {
        console.error('Error marking invoice as paid:', error);
        alert('Failed to mark invoice as paid.');
      }
    },
    async save() {
      if (this.saving) return; // Prevent double submission
      this.saving = true;
      try {
        if (this.form.InvoiceID) {
          await axios.put(`/api/invoices/${this.form.InvoiceID}/`, this.form);
        } else {
          await axios.post('/api/invoices/', this.form);
        }
        this.showModal = false;
        this.fetchInvoices();
      } catch (error) {
        console.error('Error saving invoice:', error);
        alert('Failed to save invoice.');
      } finally {
        this.saving = false;
      }
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString();
    },
    formatCurrency(amount) {
      if (typeof amount !== 'number') return amount;
      return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
    },
  },
};
</script>

<style scoped>
.toolbar-group {
  align-items: flex-end;
}

.toolbar-group :deep(.ui-form-field) {
  min-width: 180px;
}

.invoices-table .invoice-number {
  font-weight: 600;
  color: #2c3e50;
}

.amount {
  font-weight: 600;
  text-align: right;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-draft {
  background: #e9ecef;
  color: #6c757d;
}

.status-sent {
  background: #cce5ff;
  color: #0066cc;
}

.status-paid {
  background: #d4edda;
  color: #155724;
}

.status-overdue {
  background: #f8d7da;
  color: #721c24;
}

.status-cancelled {
  background: #f5c6cb;
  color: #721c24;
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
