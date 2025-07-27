<template>
  <div class="vendors-container">
    <h1 class="page-title">Vendors</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary" @click="createVendor">New Vendor</button>
      <div class="filters">
        <input 
          type="text" 
          placeholder="Search vendors..." 
          class="search-input" 
          v-model="searchTerm"
          @input="filterVendors"
        />
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="vendors-table">
          <thead>
            <tr>
              <th>Vendor Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vendor in filteredVendors" :key="vendor.vendor_id">
              <td>{{ vendor.name }}</td>
              <td>{{ vendor.email || 'N/A' }}</td>
              <td>{{ vendor.phone || 'N/A' }}</td>
              <td>{{ vendor.address || 'N/A' }}</td>
              <td>
                <button class="btn btn-sm btn-outline" @click="viewVendor(vendor)">View</button>
                <button class="btn btn-sm btn-outline" @click="editVendor(vendor)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteVendor(vendor.vendor_id)">Delete</button>
              </td>
            </tr>
            <tr v-if="filteredVendors.length === 0">
              <td colspan="5" class="text-center">No vendors found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Vendor Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalMode === 'view' ? 'View Vendor' : modalMode === 'edit' ? 'Edit Vendor' : 'New Vendor' }}</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Name: <span class="required">*</span></label>
            <input 
              v-if="modalMode !== 'view'" 
              type="text" 
              v-model="selectedVendor.name" 
              class="form-control"
              required
            />
            <span v-else class="form-value">{{ selectedVendor.name }}</span>
          </div>
          
          <div class="form-group">
            <label>Email:</label>
            <input 
              v-if="modalMode !== 'view'" 
              type="email" 
              v-model="selectedVendor.email" 
              class="form-control"
            />
            <span v-else class="form-value">{{ selectedVendor.email || 'N/A' }}</span>
          </div>
          
          <div class="form-group">
            <label>Phone:</label>
            <input 
              v-if="modalMode !== 'view'" 
              type="text" 
              v-model="selectedVendor.phone" 
              class="form-control"
            />
            <span v-else class="form-value">{{ selectedVendor.phone || 'N/A' }}</span>
          </div>
          
          <div class="form-group">
            <label>Address:</label>
            <textarea 
              v-if="modalMode !== 'view'" 
              v-model="selectedVendor.address" 
              class="form-control"
              rows="3"
            ></textarea>
            <span v-else class="form-value">{{ selectedVendor.address || 'N/A' }}</span>
          </div>
          
          <div class="form-group">
            <label>Payment Terms:</label>
            <select 
              v-if="modalMode !== 'view'" 
              v-model="selectedVendor.payment_terms" 
              class="form-control"
            >
              <option value="Net 15">Net 15</option>
              <option value="Net 30">Net 30</option>
              <option value="Net 45">Net 45</option>
              <option value="Net 60">Net 60</option>
              <option value="Due on Receipt">Due on Receipt</option>
              <option value="COD">Cash on Delivery</option>
            </select>
            <span v-else class="form-value">{{ selectedVendor.payment_terms || 'Net 30' }}</span>
          </div>
          
          <div class="form-group">
            <label>Vendor Notes:</label>
            <textarea 
              v-if="modalMode !== 'view'" 
              v-model="selectedVendor.vendor_notes" 
              class="form-control"
              rows="3"
              placeholder="Any special notes about this vendor..."
            ></textarea>
            <span v-else class="form-value">{{ selectedVendor.vendor_notes || 'No notes' }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button v-if="modalMode === 'edit'" class="btn btn-primary" @click="saveVendor" :disabled="!selectedVendor.name">Save Changes</button>
          <button v-if="modalMode === 'create'" class="btn btn-primary" @click="createNewVendor" :disabled="!selectedVendor.name">Create Vendor</button>
          <button class="btn btn-secondary" @click="closeModal">{{ modalMode === 'view' ? 'Close' : 'Cancel' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import contactsService from '@/services/contactsService'

export default {
  name: 'VendorsView',
  data() {
    return {
      vendors: [],
      filteredVendors: [],
      searchTerm: '',
      loading: false,
      showModal: false,
      modalMode: 'view', // 'view', 'edit', or 'create'
      selectedVendor: {}
    }
  },
  async mounted() {
    await this.fetchVendors()
  },
  methods: {
    async fetchVendors() {
      try {
        this.loading = true
        const vendors = await contactsService.getVendors()
        this.vendors = vendors
        this.filteredVendors = [...this.vendors]
      } catch (error) {
        console.error('Error fetching vendors:', error)
      } finally {
        this.loading = false
      }
    },
    filterVendors() {
      if (!this.searchTerm) {
        this.filteredVendors = [...this.vendors]
        return
      }
      
      const term = this.searchTerm.toLowerCase()
      this.filteredVendors = this.vendors.filter(vendor => 
        vendor.name.toLowerCase().includes(term) ||
        (vendor.email && vendor.email.toLowerCase().includes(term)) ||
        (vendor.phone && vendor.phone.includes(term))
      )
    },
    editVendor(vendor) {
      this.selectedVendor = { ...vendor };
      this.modalMode = 'edit';
      this.showModal = true;
    },

    viewVendor(vendor) {
      this.selectedVendor = { ...vendor };
      this.modalMode = 'view';
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.selectedVendor = {};
    },

    async saveVendor() {
      try {
        await contactsService.updateVendor(this.selectedVendor.vendor_id, this.selectedVendor);
        await this.fetchVendors(); // Reload the list
        this.closeModal();
        alert('Vendor updated successfully!');
      } catch (error) {
        console.error('Error updating vendor:', error);
        alert('Failed to update vendor');
      }
    },

    createVendor() {
      this.selectedVendor = {
        name: '',
        email: '',
        phone: '',
        address: '',
        payment_terms: 'Net 30',
        vendor_notes: ''
      };
      this.modalMode = 'create';
      this.showModal = true;
    },

    async createNewVendor() {
      if (!this.selectedVendor.name.trim()) {
        alert('Vendor name is required');
        return;
      }
      
      try {
        await contactsService.createVendor(this.selectedVendor);
        await this.fetchVendors(); // Reload the list
        this.closeModal();
        alert('Vendor created successfully!');
      } catch (error) {
        console.error('Error creating vendor:', error);
        alert('Failed to create vendor');
      }
    },
    async deleteVendor(vendorId) {
      if (confirm('Are you sure you want to delete this vendor?')) {
        try {
          await contactsService.deleteVendor(vendorId)
          await this.fetchVendors() // Refresh the list
        } catch (error) {
          console.error('Error deleting vendor:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
.vendors-container {
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

.search-input {
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

.vendors-table {
  width: 100%;
  border-collapse: collapse;
}

.vendors-table th {
  text-align: left;
  padding: 14px 20px;
  border-bottom: 2px solid #eee;
  color: #555;
  font-weight: 600;
}

.vendors-table td {
  padding: 14px 20px;
  border-bottom: 1px solid #eee;
  color: #333;
}

.text-center {
  text-align: center;
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
</style>
