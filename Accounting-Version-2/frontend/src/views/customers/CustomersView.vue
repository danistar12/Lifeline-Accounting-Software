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
      error: null
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
      } catch (error) {
        console.error('Error loading customers:', error);
        this.error = 'Failed to load customers';
      } finally {
        this.loading = false;
      }
    },
    
    async createCustomer() {
      // TODO: Implement customer creation modal/form
      console.log('Create customer clicked');
    },
    
    async viewCustomer(customer) {
      console.log('View customer:', customer);
      // TODO: Navigate to customer detail view
    },
    
    async editCustomer(customer) {
      console.log('Edit customer:', customer);
      // TODO: Implement customer edit modal/form
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
