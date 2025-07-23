<template>
  <div class="vendors-container">
    <h1 class="page-title">Vendors</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary" @click="showCreateForm = true">New Vendor</button>
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
      showCreateForm: false,
      loading: false
    }
  },
  async mounted() {
    await this.fetchVendors()
  },
  methods: {
    async fetchVendors() {
      try {
        this.loading = true
        const response = await contactsService.getVendors()
        this.vendors = response.data
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
      // TODO: Implement edit functionality
      console.log('Edit vendor:', vendor)
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
.btn-primary {
  background-color: #2a5298;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
}
.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
</style>
