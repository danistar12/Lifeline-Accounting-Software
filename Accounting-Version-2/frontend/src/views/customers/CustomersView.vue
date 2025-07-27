<template>
  <div class="customers-container">
    <h1 class="page-title">Customers</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary" @click="createCustomer">New Customer</button>
      <div class="filters">
        <input 
          type="text" 
          placeholder="Search customers..." 
          class="search-input"
          v-model="searchTerm"
        />
        <select class="filter-select" v-model="statusFilter">
          <option value="all">All Customers</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
          Loading customers...
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="error-state">
          {{ error }}
          <button @click="loadCustomers" class="btn btn-sm">Retry</button>
        </div>
        
        <!-- Empty state -->
        <div v-else-if="filteredCustomers().length === 0" class="empty-state">
          No customers found.
        </div>
        
        <!-- Customers table -->
        <table v-else class="customers-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Payment Terms</th>
              <th>Created Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in filteredCustomers()" :key="customer.customer_id">
              <td>{{ customer.name }}</td>
              <td>{{ customer.email || 'N/A' }}</td>
              <td>{{ customer.phone || 'N/A' }}</td>
              <td>{{ customer.payment_terms || 'Net 30' }}</td>
              <td>{{ new Date(customer.created_date).toLocaleDateString() }}</td>
              <td>
                <button class="btn btn-sm btn-outline" @click="viewCustomer(customer)">View</button>
                <button class="btn btn-sm btn-outline" @click="editCustomer(customer)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteCustomer(customer)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Customer Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalMode === 'view' ? 'View Customer' : modalMode === 'edit' ? 'Edit Customer' : 'New Customer' }}</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Name: <span class="required">*</span></label>
            <input 
              v-if="modalMode !== 'view'" 
              type="text" 
              v-model="selectedCustomer.name" 
              class="form-control"
              required
            />
            <span v-else class="form-value">{{ selectedCustomer.name }}</span>
          </div>
          
          <div class="form-group">
            <label>Email:</label>
            <input 
              v-if="modalMode !== 'view'" 
              type="email" 
              v-model="selectedCustomer.email" 
              class="form-control"
            />
            <span v-else class="form-value">{{ selectedCustomer.email || 'N/A' }}</span>
          </div>
          
          <div class="form-group">
            <label>Phone:</label>
            <input 
              v-if="modalMode !== 'view'" 
              type="text" 
              v-model="selectedCustomer.phone" 
              class="form-control"
            />
            <span v-else class="form-value">{{ selectedCustomer.phone || 'N/A' }}</span>
          </div>
          
          <div class="form-group">
            <label>Address:</label>
            <textarea 
              v-if="modalMode !== 'view'" 
              v-model="selectedCustomer.address" 
              class="form-control"
              rows="3"
            ></textarea>
            <span v-else class="form-value">{{ selectedCustomer.address || 'N/A' }}</span>
          </div>
          
          <div class="form-group">
            <label>Payment Terms:</label>
            <select 
              v-if="modalMode !== 'view'" 
              v-model="selectedCustomer.payment_terms" 
              class="form-control"
            >
              <option value="Net 15">Net 15</option>
              <option value="Net 30">Net 30</option>
              <option value="Net 45">Net 45</option>
              <option value="Net 60">Net 60</option>
              <option value="Due on Receipt">Due on Receipt</option>
              <option value="COD">Cash on Delivery</option>
            </select>
            <span v-else class="form-value">{{ selectedCustomer.payment_terms || 'Net 30' }}</span>
          </div>
          
          <div class="form-group">
            <label>Customer Notes:</label>
            <textarea 
              v-if="modalMode !== 'view'" 
              v-model="selectedCustomer.customer_notes" 
              class="form-control"
              rows="3"
              placeholder="Any special notes about this customer..."
            ></textarea>
            <span v-else class="form-value">{{ selectedCustomer.customer_notes || 'No notes' }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button v-if="modalMode === 'edit'" class="btn btn-primary" @click="saveCustomer" :disabled="!selectedCustomer.name">Save Changes</button>
          <button v-if="modalMode === 'create'" class="btn btn-primary" @click="createNewCustomer" :disabled="!selectedCustomer.name">Create Customer</button>
          <button class="btn btn-secondary" @click="closeModal">{{ modalMode === 'view' ? 'Close' : 'Cancel' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { contactsService } from '@/services';

export default {
  name: 'CustomersView',
  data() {
    return {
      customers: [],
      loading: false,
      searchTerm: '',
      statusFilter: 'all',
      error: null,
      showModal: false,
      modalMode: 'view', // 'view', 'edit', or 'create'
      selectedCustomer: {}
    };
  },
  async mounted() {
    await this.loadCustomers();
  },
  methods: {
    async loadCustomers() {
      this.loading = true;
      try {
        this.customers = await contactsService.getCustomers();
        console.log('Loaded customers:', this.customers); // Debug log
      } catch (error) {
        console.error('Error loading customers:', error);
        this.error = 'Failed to load customers';
      } finally {
        this.loading = false;
      }
    },
    
    async createCustomer() {
      this.selectedCustomer = {
        name: '',
        email: '',
        phone: '',
        address: '',
        payment_terms: 'Net 30',
        customer_notes: ''
      };
      this.modalMode = 'create';
      this.showModal = true;
    },
    
    async viewCustomer(customer) {
      this.selectedCustomer = { ...customer };
      this.modalMode = 'view';
      this.showModal = true;
    },
    
    async editCustomer(customer) {
      this.selectedCustomer = { ...customer };
      this.modalMode = 'edit';
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedCustomer = {};
    },

    async saveCustomer() {
      try {
        await contactsService.updateCustomer(this.selectedCustomer.customer_id, this.selectedCustomer);
        await this.loadCustomers(); // Reload the list
        this.closeModal();
        alert('Customer updated successfully!');
      } catch (error) {
        console.error('Error updating customer:', error);
        alert('Failed to update customer');
      }
    },

    async createNewCustomer() {
      if (!this.selectedCustomer.name.trim()) {
        alert('Customer name is required');
        return;
      }
      
      try {
        await contactsService.createCustomer(this.selectedCustomer);
        await this.loadCustomers(); // Reload the list
        this.closeModal();
        alert('Customer created successfully!');
      } catch (error) {
        console.error('Error creating customer:', error);
        alert('Failed to create customer');
      }
    },
    
    async deleteCustomer(customer) {
      if (confirm(`Are you sure you want to delete ${customer.name}?`)) {
        try {
          await contactsService.deleteCustomer(customer.customer_id);
          await this.loadCustomers(); // Reload the list
        } catch (error) {
          console.error('Error deleting customer:', error);
          alert('Failed to delete customer');
        }
      }
    },
    
    filteredCustomers() {
      return this.customers.filter(customer => {
        const matchesSearch = customer.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                            customer.email?.toLowerCase().includes(this.searchTerm.toLowerCase());
        const matchesStatus = this.statusFilter === 'all' || 
                            (this.statusFilter === 'active' && customer.is_active !== false);
        return matchesSearch && matchesStatus;
      });
    }
  }
};
</script>

<style scoped>
.customers-container {
  padding: 20px;
}

.page-title {
  font-size: 1.8rem;
  color: #2a5298;
  margin-bottom: 24px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.btn-primary {
  background-color: #2a5298;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.filters {
  display: flex;
  gap: 12px;
}

.search-input, .filter-select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  min-width: 200px;
}

.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-body {
  padding: 20px;
}

.customers-table {
  width: 100%;
  border-collapse: collapse;
}

.customers-table th {
  text-align: left;
  padding: 14px 20px;
  border-bottom: 2px solid #eee;
  color: #555;
  font-weight: 600;
}

.customers-table td {
  padding: 14px 20px;
  border-bottom: 1px solid #eee;
  color: #333; /* Ensure text is dark, not grey */
}

.btn {
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover {
  opacity: 0.8;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.badge-success {
  background-color: #dcf5e8;
  color: #0d9152;
}

.badge-neutral {
  background-color: #eee;
  color: #666;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 4px;
  margin-right: 5px;
}

.btn-outline {
  border: 1px solid #2a5298;
  color: #2a5298;
  background: transparent;
  cursor: pointer;
}

.btn-outline:hover {
  background-color: #2a5298;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border: 1px solid #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #2a5298;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.required {
  color: #dc3545;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #2a5298;
  box-shadow: 0 0 0 2px rgba(42, 82, 152, 0.1);
}

.form-control:invalid {
  border-color: #dc3545;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-value {
  display: block;
  padding: 8px 0;
  color: #333;
  min-height: 20px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: 1px solid #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-info {
  color: #666;
}
</style>
