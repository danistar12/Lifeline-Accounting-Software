<template>
  <div class="companies-container">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="icon-building"></i>
          Company Management
        </h1>
        <p class="page-subtitle">Select and manage your companies</p>
      </div>
      <div class="header-actions">
        <button class="btn btn-outline" @click="loadCompaniesData">
          <i class="icon-refresh"></i>
          Refresh
        </button>
        <button class="btn btn-primary" @click="showAddCompanyModal = true">
          <i class="icon-plus"></i>
          Add Company
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading companies...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h3>Error Loading Companies</h3>
      <p>{{ error }}</p>
      <div class="error-actions">
        <button class="btn btn-primary" @click="loadCompaniesData">
          <i class="icon-refresh"></i>
          Try Again
        </button>
        <button class="btn btn-outline" @click="$router.push('/login')">
          <i class="icon-login"></i>
          Go to Login
        </button>
      </div>
    </div>

    <!-- Companies Grid -->
    <div v-else-if="!error && companies.length > 0" class="companies-grid">
      <div 
        v-for="company in companies" 
        :key="company.CompanyID"
        class="company-card"
        :class="{ 'selected': selectedCompanyId === company.CompanyID }"
        @click="selectCompany(company)"
      >
        <div class="company-card-header">
          <div class="company-avatar">
            {{ getCompanyInitials(company.CompanyName) }}
          </div>
          <div class="company-basic-info">
            <h3 class="company-name">{{ company.CompanyName }}</h3>
            <p class="company-location">{{ company.City }}, {{ company.State }}</p>
          </div>
          <div class="company-status">
            <span class="status-badge active">Active</span>
          </div>
        </div>
        
        <div class="company-card-body">
          <div class="company-details">
            <div class="detail-item">
              <i class="icon-mail"></i>
              <span>{{ company.Email || 'No email provided' }}</span>
            </div>
            <div class="detail-item">
              <i class="icon-phone"></i>
              <span>{{ company.Phone || 'No phone provided' }}</span>
            </div>
            <div class="detail-item">
              <i class="icon-location"></i>
              <span>{{ formatAddress(company) }}</span>
            </div>
          </div>
        </div>

        <div class="company-card-footer">
          <button class="btn btn-outline" @click.stop="editCompany(company)">
            <i class="icon-edit"></i>
            Edit
          </button>
          <button class="btn btn-primary" @click.stop="viewCompanyDetails(company)">
            <i class="icon-eye"></i>
            View Details
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!error && !loading" class="empty-state">
      <div class="empty-icon">
        <i class="icon-building"></i>
      </div>
      <h3>No Companies Found</h3>
      <p>You don't have access to any companies yet. Contact your administrator or add a new company.</p>
      <button class="btn btn-primary" @click="showAddCompanyModal = true">
        <i class="icon-plus"></i>
        Add Your First Company
      </button>
    </div>

    <!-- Selected Company Details Panel -->
    <div v-if="selectedCompany" class="company-details-panel">
      <div class="panel-header">
  <h2>{{ selectedCompany.CompanyName }} - Details</h2>
        <button class="btn btn-ghost" @click="closeDetailsPanel">
          <i class="icon-close"></i>
        </button>
      </div>
      
      <div class="panel-content">
        <div class="details-grid">
          <!-- Company Information -->
          <div class="detail-section">
            <h4>Company Information</h4>
            <div class="detail-group">
              <div class="detail-row">
                <label>Company Name:</label>
                <span>{{ selectedCompany.CompanyName }}</span>
              </div>
              <div class="detail-row">
                <label>Contact Person:</label>
                <span>{{ selectedCompany.ContactPerson || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>Email:</label>
                <span>{{ selectedCompany.Email || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>Phone:</label>
                <span>{{ selectedCompany.Phone || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>Website:</label>
                <span v-if="selectedCompany.Website">
                  <a :href="selectedCompany.Website" target="_blank" class="link">{{ selectedCompany.Website }}</a>
                </span>
                <span v-else>Not provided</span>
              </div>
              <div class="detail-row">
                <label>Tax ID:</label>
                <span>{{ selectedCompany.TaxID || 'Not provided' }}</span>
              </div>
            </div>
          </div>

          <!-- Address Information -->
          <div class="detail-section">
            <h4>Address</h4>
            <div class="detail-group">
              <div class="detail-row">
                <label>Street Address:</label>
                <span>{{ selectedCompany.Address || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>City:</label>
                <span>{{ selectedCompany.City || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>State:</label>
                <span>{{ selectedCompany.State || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>ZIP Code:</label>
                <span>{{ selectedCompany.ZipCode || 'Not provided' }}</span>
              </div>
              <div class="detail-row">
                <label>Country:</label>
                <span>{{ selectedCompany.Country || 'United States' }}</span>
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="detail-section">
            <h4>Quick Stats</h4>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-value">{{ companyStats.totalUsers || 0 }}</div>
                <div class="stat-label">Users</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ companyStats.totalTransactions || 0 }}</div>
                <div class="stat-label">Transactions</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">${{ companyStats.totalRevenue || '0.00' }}</div>
                <div class="stat-label">Revenue</div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="detail-section">
            <h4>Actions</h4>
            <div class="action-buttons">
              <button class="btn btn-primary" @click="setActiveCompany(selectedCompany)">
                <i class="icon-check"></i>
                Set as Active Company
              </button>
              <button class="btn btn-outline" @click="editCompany(selectedCompany)">
                <i class="icon-edit"></i>
                Edit Company
              </button>
              <button class="btn btn-outline" @click="viewReports(selectedCompany)">
                <i class="icon-chart"></i>
                View Reports
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Current Active Company Banner -->
    <div v-if="activeCompany" class="active-company-banner">
      <div class="banner-content">
        <i class="icon-check-circle"></i>
  <span>Currently working in: <strong>{{ activeCompany?.CompanyName || 'No company selected' }}</strong></span>
      </div>
      <button class="btn btn-ghost btn-sm" @click="clearActiveCompany">
        Change Company
      </button>
    </div>

    <!-- Edit Company Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Edit Company</h3>
          <button class="modal-close" @click="closeEditModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveCompanyEdit" class="modal-body">
          <!-- Basic Information -->
          <div class="form-section">
            <h4>Basic Information</h4>
            <div class="form-group">
              <label for="editCompanyName">Company Name *</label>
              <input 
                id="editCompanyName"
                v-model="editForm.CompanyName" 
                type="text" 
                class="form-control" 
                required
                placeholder="Enter company name"
              >
            </div>
            
            <div class="form-group">
              <label for="editCompanyNotes">Company Notes</label>
              <textarea 
                id="editCompanyNotes"
                v-model="editForm.CompanyNotes" 
                class="form-control" 
                rows="3"
                placeholder="Optional notes about the company"
              ></textarea>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="form-section">
            <h4>Contact Information</h4>
            <div class="form-row">
              <div class="form-group">
                <label for="editContactPerson">Contact Person</label>
                <input 
                  id="editContactPerson"
                  v-model="editForm.ContactPerson" 
                  type="text" 
                  class="form-control" 
                  placeholder="Primary contact name"
                >
              </div>
              <div class="form-group">
                <label for="editEmail">Email</label>
                <input 
                  id="editEmail"
                  v-model="editForm.Email" 
                  type="email" 
                  class="form-control" 
                  placeholder="company@example.com"
                >
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="editPhone">Phone</label>
                <input 
                  id="editPhone"
                  v-model="editForm.Phone" 
                  type="tel" 
                  class="form-control" 
                  placeholder="(555) 123-4567"
                >
              </div>
              <div class="form-group">
                <label for="editWebsite">Website</label>
                <input 
                  id="editWebsite"
                  v-model="editForm.Website" 
                  type="url" 
                  class="form-control" 
                  placeholder="https://www.company.com"
                >
              </div>
            </div>
          </div>

          <!-- Address Information -->
          <div class="form-section">
            <h4>Address Information</h4>
            <div class="form-group">
              <label for="editAddress">Street Address</label>
              <input 
                id="editAddress"
                v-model="editForm.Address" 
                type="text" 
                class="form-control" 
                placeholder="123 Main Street"
              >
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="editCity">City</label>
                <input 
                  id="editCity"
                  v-model="editForm.City" 
                  type="text" 
                  class="form-control" 
                  placeholder="City"
                >
              </div>
              <div class="form-group">
                <label for="editState">State</label>
                <input 
                  id="editState"
                  v-model="editForm.State" 
                  type="text" 
                  class="form-control" 
                  placeholder="State"
                >
              </div>
              <div class="form-group">
                <label for="editZipCode">ZIP Code</label>
                <input 
                  id="editZipCode"
                  v-model="editForm.ZipCode" 
                  type="text" 
                  class="form-control" 
                  placeholder="12345"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label for="editCountry">Country</label>
              <input 
                id="editCountry"
                v-model="editForm.Country" 
                type="text" 
                class="form-control" 
                placeholder="United States"
              >
            </div>
          </div>

          <!-- Business Information -->
          <div class="form-section">
            <h4>Business Information</h4>
            <div class="form-group">
              <label for="editTaxId">Tax ID / EIN</label>
              <input 
                id="editTaxId"
                v-model="editForm.TaxID" 
                type="text" 
                class="form-control" 
                placeholder="12-3456789"
              >
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-outline" @click="closeEditModal">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="editLoading">
              <span v-if="editLoading">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add Company Modal -->
    <div v-if="showAddCompanyModal" class="modal-overlay" @click="closeAddModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Add New Company</h3>
          <button class="modal-close" @click="closeAddModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveNewCompany" class="modal-body">
          <!-- Basic Information -->
          <div class="form-section">
            <h4>Basic Information</h4>
            <div class="form-group">
              <label for="newCompanyName">Company Name *</label>
              <input 
                id="newCompanyName"
                v-model="addForm.CompanyName" 
                type="text" 
                class="form-control" 
                required
                placeholder="Enter company name"
              >
            </div>
            
            <div class="form-group">
              <label for="newCompanyNotes">Company Notes</label>
              <textarea 
                id="newCompanyNotes"
                v-model="addForm.CompanyNotes" 
                class="form-control" 
                rows="3"
                placeholder="Optional notes about the company"
              ></textarea>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="form-section">
            <h4>Contact Information</h4>
            <div class="form-row">
              <div class="form-group">
                <label for="newContactPerson">Contact Person</label>
                <input 
                  id="newContactPerson"
                  v-model="addForm.ContactPerson" 
                  type="text" 
                  class="form-control" 
                  placeholder="Primary contact name"
                >
              </div>
              <div class="form-group">
                <label for="newEmail">Email</label>
                <input 
                  id="newEmail"
                  v-model="addForm.Email" 
                  type="email" 
                  class="form-control" 
                  placeholder="company@example.com"
                >
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="newPhone">Phone</label>
                <input 
                  id="newPhone"
                  v-model="addForm.Phone" 
                  type="tel" 
                  class="form-control" 
                  placeholder="(555) 123-4567"
                >
              </div>
              <div class="form-group">
                <label for="newWebsite">Website</label>
                <input 
                  id="newWebsite"
                  v-model="addForm.Website" 
                  type="url" 
                  class="form-control" 
                  placeholder="https://www.company.com"
                >
              </div>
            </div>
          </div>

          <!-- Address Information -->
          <div class="form-section">
            <h4>Address Information</h4>
            <div class="form-group">
              <label for="newAddress">Street Address</label>
              <input 
                id="newAddress"
                v-model="addForm.Address" 
                type="text" 
                class="form-control" 
                placeholder="123 Main Street"
              >
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="newCity">City</label>
                <input 
                  id="newCity"
                  v-model="addForm.City" 
                  type="text" 
                  class="form-control" 
                  placeholder="City"
                >
              </div>
              <div class="form-group">
                <label for="newState">State</label>
                <input 
                  id="newState"
                  v-model="addForm.State" 
                  type="text" 
                  class="form-control" 
                  placeholder="State"
                >
              </div>
              <div class="form-group">
                <label for="newZipCode">ZIP Code</label>
                <input 
                  id="newZipCode"
                  v-model="addForm.ZipCode" 
                  type="text" 
                  class="form-control" 
                  placeholder="12345"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label for="newCountry">Country</label>
              <input 
                id="newCountry"
                v-model="addForm.Country" 
                type="text" 
                class="form-control" 
                placeholder="United States"
              >
            </div>
          </div>

          <!-- Business Information -->
          <div class="form-section">
            <h4>Business Information</h4>
            <div class="form-row">
              <div class="form-group">
                <label for="newTaxId">Tax ID / EIN</label>
                <input 
                  id="newTaxId"
                  v-model="addForm.TaxID" 
                  type="text" 
                  class="form-control" 
                  placeholder="12-3456789"
                >
              </div>
              <div class="form-group">
                <label for="newUserRole">Your Role</label>
                <select id="newUserRole" v-model="addForm.Role" class="form-control">
                  <option value="Admin">Admin</option>
                  <option value="Manager">Manager</option>
                  <option value="Accountant">Accountant</option>
                  <option value="Viewer">Viewer</option>
                </select>
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-outline" @click="closeAddModal">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="addLoading">
              <span v-if="addLoading">Creating...</span>
              <span v-else>Create Company</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';

export default {
  name: 'CompaniesView',
  data() {
    return {
      companies: [],
      loading: true,
      selectedCompany: null,
      selectedCompanyId: null,
      activeCompany: null,
      showAddCompanyModal: false,
      showEditModal: false,
      companyStats: {},
      error: null,
      editLoading: false,
      addLoading: false,
      editForm: {
        CompanyID: null,
        CompanyName: '',
        CompanyNotes: '',
        ContactPerson: '',
        Email: '',
        Phone: '',
        Website: '',
        Address: '',
        City: '',
        State: '',
        ZipCode: '',
        Country: 'United States',
        TaxID: '',
        AdminUserID: null,
      },
      addForm: {
        CompanyName: '',
        CompanyNotes: '',
        ContactPerson: '',
        Email: '',
        Phone: '',
        Website: '',
        Address: '',
        City: '',
        State: '',
        ZipCode: '',
        Country: 'United States',
        TaxID: '',
        AdminUserID: null,
        Role: 'Admin'
      }
    };
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
  },
  methods: {
    ...mapActions(['loadCompanies', 'setSelectedCompany']),
    
    async loadCompaniesData() {
      this.loading = true;
      try {
        console.log('Loading companies...');
        console.log('User logged in:', this.isLoggedIn);
        console.log('Axios default headers:', axios.defaults.headers.common);
        
        const response = await axios.get('/api/accounts/companies/');
        this.companies = response.data;
        console.log('Companies loaded successfully:', this.companies);
        
        // Load active company from localStorage
        const savedCompanyId = localStorage.getItem('selectedCompanyId');
        if (savedCompanyId) {
          const savedCompany = this.companies.find(c => `${c.CompanyID}` === `${savedCompanyId}`);
          if (savedCompany) {
            this.activeCompany = savedCompany;
            console.log('Restored active company:', savedCompany);
          }
        }
      } catch (error) {
        console.error('Failed to load companies:', error);
        console.error('Error status:', error.response?.status);
        console.error('Error data:', error.response?.data);
        console.error('Error headers:', error.response?.headers);
        
        // If it's an authentication error, try to re-authenticate
        if (error.response?.status === 401) {
          console.log('Authentication error, redirecting to login');
          this.error = 'Authentication required. Please log in again.';
          this.$router.push('/login');
        } else {
          this.error = `Failed to load companies: ${error.response?.data?.detail || error.message}`;
        }
      } finally {
        this.loading = false;
      }
    },

    selectCompany(company) {
      this.selectedCompany = company;
      this.selectedCompanyId = company.CompanyID;
      this.loadCompanyStats();
    },

    async loadCompanyStats() {
      // Mock stats for now - you can implement real API calls later
      this.companyStats = {
        totalUsers: Math.floor(Math.random() * 50) + 1,
        totalTransactions: Math.floor(Math.random() * 1000) + 100,
        totalRevenue: (Math.random() * 100000).toFixed(2)
      };
    },

    setActiveCompany(company) {
      this.activeCompany = company;
      localStorage.setItem('selectedCompanyId', company.CompanyID);
      
      // Set axios header for API requests
      axios.defaults.headers.common['X-Company-ID'] = company.CompanyID;
      
      // Update store
      this.setSelectedCompany(company.CompanyID);
      
      // Show success message
      this.$notify({
        type: 'success',
        title: 'Company Selected',
        message: `${company.CompanyName} is now your active company`
      });
    },

    clearActiveCompany() {
      this.activeCompany = null;
      localStorage.removeItem('selectedCompanyId');
      delete axios.defaults.headers.common['X-Company-ID'];
      this.setSelectedCompany(null);
    },

    closeDetailsPanel() {
      this.selectedCompany = null;
      this.selectedCompanyId = null;
    },

    editCompany(company) {
      // Populate edit form and show modal
      this.editForm = {
        CompanyID: company.CompanyID,
        CompanyName: company.CompanyName,
        CompanyNotes: company.CompanyNotes || '',
        ContactPerson: company.ContactPerson || '',
        Email: company.Email || '',
        Phone: company.Phone || '',
        Website: company.Website || '',
        Address: company.Address || '',
        City: company.City || '',
        State: company.State || '',
        ZipCode: company.ZipCode || '',
        Country: company.Country || 'United States',
        TaxID: company.TaxID || ''
      };
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
      this.editForm = {
        CompanyID: null,
        CompanyName: '',
        CompanyNotes: '',
        ContactPerson: '',
        Email: '',
        Phone: '',
        Website: '',
        Address: '',
        City: '',
        State: '',
        ZipCode: '',
        Country: 'United States',
        TaxID: ''
      };
    },

    closeAddModal() {
      this.showAddCompanyModal = false;
      this.addForm = {
        CompanyName: '',
        CompanyNotes: '',
        ContactPerson: '',
        Email: '',
        Phone: '',
        Website: '',
        Address: '',
        City: '',
        State: '',
        ZipCode: '',
        Country: 'United States',
        TaxID: '',
        Role: 'Admin'
      };
    },

    async saveCompanyEdit() {
      this.editLoading = true;
      try {
        const payload = {
          CompanyName: this.editForm.CompanyName,
          CompanyNotes: this.editForm.CompanyNotes,
          AdminUserID: this.editForm.AdminUserID ?? null,
        };

        const response = await axios.put(`/api/accounts/companies/${this.editForm.CompanyID}/`, payload);
        
        // Update the company in the local array
        const index = this.companies.findIndex(c => c.CompanyID === this.editForm.CompanyID);
        if (index !== -1) {
          this.companies[index] = response.data;
        }
        
        // Update selected company if it's the one being edited
        if (this.selectedCompany && this.selectedCompany.CompanyID === this.editForm.CompanyID) {
          this.selectedCompany = response.data;
        }
        
        this.closeEditModal();
        console.log('Company updated successfully');
      } catch (error) {
        console.error('Failed to update company:', error);
        alert('Failed to update company. Please try again.');
      } finally {
        this.editLoading = false;
      }
    },

    async saveNewCompany() {
      this.addLoading = true;
      try {
        const payload = {
          CompanyName: this.addForm.CompanyName,
          CompanyNotes: this.addForm.CompanyNotes,
          AdminUserID: this.addForm.AdminUserID ?? null,
        };

        const response = await axios.post('/api/accounts/companies/', payload);
        
        // Add the new company to the list
        this.companies.push(response.data);
        
        // Create user-company role
        await axios.post('/api/accounts/user-company-roles/', {
          CompanyID: response.data.CompanyID,
          Role: this.addForm.Role
        });
        
        this.closeAddModal();
        console.log('Company created successfully');
      } catch (error) {
        console.error('Failed to create company:', error);
        alert('Failed to create company. Please try again.');
      } finally {
        this.addLoading = false;
      }
    },

    viewCompanyDetails(company) {
      this.selectCompany(company);
    },

    viewReports(company) {
      // Navigate to reports for this company
      this.$router.push({
        path: '/reports/balance-sheet',
        query: { company: company.CompanyID }
      });
    },

    getCompanyInitials(name) {
      if (!name || typeof name !== 'string') {
        return 'NA';
      }

      const trimmedName = name.trim();
      if (!trimmedName) {
        return 'NA';
      }

      const parts = trimmedName.split(/\s+/).filter(Boolean);
      const initials = parts
        .slice(0, 2)
        .map(part => part.charAt(0).toUpperCase())
        .join('');

      if (initials) {
        return initials;
      }

      return trimmedName.substring(0, 2).toUpperCase();
    },

    formatAddress(company) {
      const parts = [company.Address, company.City, company.State, company.ZipCode];
      return parts.filter(part => part).join(', ') || 'No address provided';
    }
  },

  async mounted() {
    if (this.isLoggedIn) {
      await this.loadCompaniesData();
    }
  }
};
</script>

<style scoped>
/* Container */
.companies-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

/* Icons */
.icon-building::before { content: ''; }
.icon-plus::before { content: ''; }
.icon-refresh::before { content: ''; }
.icon-login::before { content: ''; }
.icon-mail::before { content: ''; }
.icon-phone::before { content: ''; }
.icon-location::before { content: ''; }
.icon-edit::before { content: ''; }
.icon-eye::before { content: ''; }
.icon-close::before { content: ''; }
.icon-check::before { content: ''; }
.icon-chart::before { content: ''; }
.icon-check-circle::before { content: ''; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: translateY(-1px);
}

.btn-outline {
  background-color: transparent;
  color: #007bff;
  border: 2px solid #007bff;
}

.btn-outline:hover {
  background-color: #007bff;
  color: white;
  transform: translateY(-1px);
}

.btn-ghost {
  background-color: transparent;
  color: #6c757d;
  border: none;
}

.btn-ghost:hover {
  background-color: #f8f9fa;
  color: #495057;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #6c757d;
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #6c757d;
  text-align: center;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-container h3 {
  margin: 0 0 0.5rem 0;
  color: #dc3545;
}

.error-container p {
  margin: 0 0 2rem 0;
  max-width: 500px;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e9ecef;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Companies Grid */
.companies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* Company Card */
.company-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  overflow: hidden;
  border: 2px solid transparent;
}

.company-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.company-card.selected {
  border-color: #007bff;
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.25);
}

.company-card-header {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.company-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
  margin-right: 1rem;
}

.company-basic-info {
  flex: 1;
}

.company-name {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
}

.company-location {
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.company-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.company-card-body {
  padding: 1.5rem;
}

.company-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #495057;
}

.company-card-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.company-card-footer .btn {
  flex: 1;
  justify-content: center;
  padding: 0.5rem 1rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #495057;
}

.empty-state p {
  margin: 0 0 2rem 0;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* Company Details Panel */
.company-details-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.panel-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.panel-content {
  padding: 2rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.detail-section {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.detail-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.detail-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-row label {
  font-weight: 500;
  color: #495057;
}

.detail-row span {
  color: #2c3e50;
  text-align: right;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #007bff;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Active Company Banner */
.active-company-banner {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 400px;
  z-index: 1000;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .companies-container {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .companies-grid {
    grid-template-columns: 1fr;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .company-card-footer {
    flex-direction: column;
  }
  
  .active-company-banner {
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: #495057;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-control textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

/* Form sections and rows */
.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.form-section:last-of-type {
  border-bottom: none;
  margin-bottom: 1rem;
}

.form-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-row.three-columns {
  grid-template-columns: 1fr 1fr 1fr;
}

/* Link styling in detail panels */
.link {
  color: #007bff;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

/* Mobile responsiveness for modals */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
    max-height: 95vh;
  }
  
  .modal-header,
  .modal-body {
    padding: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .form-row.three-columns {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
  
  .form-section {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
  }
}
</style>
