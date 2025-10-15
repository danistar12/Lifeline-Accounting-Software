<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Bills</h1>
        <p class="page-subtitle">Manage your vendor bills and track expenses.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input
              v-model="searchTerm"
              type="search"
              placeholder="Search bills..."
              @input="filterBills"
            />
          </UiFormField>
        </div>
        <UiFormField label="Status">
          <select v-model="statusFilter" @change="filterBills">
            <option value="">All statuses</option>
            <option value="Draft">Draft</option>
            <option value="Sent">Sent</option>
            <option value="Paid">Paid</option>
            <option value="Overdue">Overdue</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </UiFormField>
        <UiButton icon="+" variant="primary" @click="openCreate">
          New bill
        </UiButton>
      </div>
    </header>

    <UiCard title="Vendor bills" subtitle="Outstanding and paid bills with vendor details.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchBills">
          Refresh
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading bills…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filteredBills.length" class="table-container">
        <table class="data-table bills-table">
          <thead>
            <tr>
              <th>Bill #</th>
              <th>Vendor</th>
              <th>Date</th>
              <th>Due Date</th>
              <th>Amount</th>
              <th>Status</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="bill in filteredBills" :key="bill.BillID">
              <td>
                <div class="bill-number">{{ bill.BillNumber }}</div>
              </td>
              <td>{{ (bill.Vendor && bill.Vendor.Name) || '—' }}</td>
              <td>{{ formatDate(bill.BillDate) }}</td>
              <td>{{ formatDate(bill.DueDate) }}</td>
              <td class="amount">{{ formatCurrency(bill.TotalAmount) }}</td>
              <td>
                <span :class="`status-badge status-${(bill.Status || '').toString().toLowerCase()}`">
                  {{ bill.Status }}
                </span>
              </td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="viewBill(bill)">
                  View
                </UiButton>
                <UiButton size="sm" variant="ghost" @click="editBill(bill)">
                  Edit
                </UiButton>
                <UiButton
                  v-if="bill.Status !== 'Paid'"
                  size="sm"
                  variant="success"
                  @click="markAsPaid(bill)"
                >
                  Mark Paid
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No bills found.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save bill"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Bill Number" required>
            <input v-model="form.BillNumber" required />
          </UiFormField>
          <UiFormField label="Vendor" required>
            <select v-model="form.VendorID" required>
              <option value="">Select vendor</option>
              <option v-for="vendor in vendors" :key="vendor.VendorID" :value="vendor.VendorID">
                {{ vendor.Name || vendor.CompanyName || '' }}
              </option>
            </select>
          </UiFormField>
          <UiFormField label="Bill Date" required>
            <input v-model="form.BillDate" type="date" required />
          </UiFormField>
          <UiFormField label="Due Date" required>
            <input v-model="form.DueDate" type="date" required />
          </UiFormField>
          <UiFormField label="Total Amount" required>
            <input v-model.number="form.TotalAmount" type="number" step="0.01" required />
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
          <textarea v-model="form.BillNotes" rows="3" placeholder="Additional notes..." />
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
import { normalizeArray } from '@/services/normalizeApi';

export default {
  name: 'BillsView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
  },
  data() {
    return {
      bills: [],
      filteredBills: [],
      vendors: [],
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
      return this.form.BillID ? 'Edit bill' : 'New bill';
    },
  },
  mounted() {
    this.fetchBills();
    this.fetchVendors();
  },
  methods: {
    defaultForm() {
      return {
        BillID: null,
        CompanyID: null,
        VendorID: null,
        BillNumber: '',
        BillDate: new Date().toISOString().split('T')[0],
        DueDate: '',
        TotalAmount: null,
        Status: 'Draft',
        CurrencyCode: 'USD',
        BillNotes: '',
      };
    },
    async fetchBills() {
      this.loading = true;
      this.error = '';
      try {
        const response = await axios.get('/api/bills/');
        const payload = response.data || [];
        this.bills = normalizeArray(payload);
        this.filteredBills = [...this.bills];
      } catch (error) {
        console.error('Error fetching bills:', error);
        this.error = 'Unable to load bills right now.';
      } finally {
        this.loading = false;
      }
    },
    async fetchVendors() {
      // Populate vendors used by the create/edit bill form
      try {
        // Try the canonical vendors endpoint first, then a namespaced one if missing
        let response;
        try {
          response = await axios.get('/api/vendors/');
        } catch (err) {
          // fallback to older namespaced endpoint
          response = await axios.get('/api/accounts/vendors/');
        }

        const payload = response.data || [];
        this.vendors = normalizeArray(payload);
      } catch (error) {
        console.warn('Failed to load vendors for bills form:', error);
        // keep vendors empty; form will show 'Select vendor'
      }
    },
    filterBills() {
      let filtered = [...this.bills];

      if (this.statusFilter) {
        filtered = filtered.filter(bill => bill.Status === this.statusFilter);
      }

      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter(bill =>
          (bill.BillNumber || '').toString().toLowerCase().includes(term) ||
          ((bill.Vendor && bill.Vendor.Name) || '').toString().toLowerCase().includes(term)
        );
      }

      this.filteredBills = filtered;
    },
    openCreate() {
      this.form = this.defaultForm();
      if (this.bills.length) {
        this.form.CompanyID = this.bills[0].CompanyID ?? null;
      }
      this.showModal = true;
    },
    editBill(bill) {
      this.form = {
        BillID: bill.BillID ?? null,
        CompanyID: bill.CompanyID ?? null,
        VendorID: (bill.Vendor && bill.Vendor.VendorID) || bill.VendorID || null,
        BillNumber: bill.BillNumber || '',
        BillDate: bill.BillDate || '',
        DueDate: bill.DueDate || '',
        TotalAmount: bill.TotalAmount ?? null,
        Status: bill.Status || 'Draft',
        CurrencyCode: bill.CurrencyCode || 'USD',
        BillNotes: bill.BillNotes || '',
      };
      this.showModal = true;
    },
    viewBill(bill) {
      // TODO: Navigate to bill detail view
      console.log('View bill:', bill);
    },
    async markAsPaid(bill) {
      try {
        await axios.patch(`/api/bills/${bill.BillID}/`, { Status: 'Paid' });
        bill.Status = 'Paid';
        this.filterBills();
      } catch (error) {
        console.error('Error marking bill as paid:', error);
        alert('Failed to mark bill as paid.');
      }
    },
    async save() {
      this.saving = true;
      try {
        const payload = { ...this.form };
        if (payload.BillID) {
          await axios.put(`/api/bills/${payload.BillID}/`, payload);
        } else {
          await axios.post('/api/bills/', payload);
        }
        this.showModal = false;
        this.fetchBills();
      } catch (error) {
        console.error('Error saving bill:', error);
        alert('Failed to save bill.');
      } finally {
        this.saving = false;
      }
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString();
    },
    formatCurrency(amount) {
      const numeric = typeof amount === 'number' ? amount : Number(amount);
      if (Number.isNaN(numeric)) return amount;
      return numeric.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
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

.bills-table .bill-number {
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
