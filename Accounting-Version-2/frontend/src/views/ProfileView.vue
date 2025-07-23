<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>Profile</h1>
    </div>

    <div class="profile-content">
      <div class="profile-section">
        <h2>Personal Information</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>Username</label>
            <div class="info-value">{{ currentUser?.username || 'N/A' }}</div>
          </div>
          <div class="info-item">
            <label>First Name</label>
            <div class="info-value">{{ currentUser?.first_name || 'N/A' }}</div>
          </div>
          <div class="info-item">
            <label>Last Name</label>
            <div class="info-value">{{ currentUser?.last_name || 'N/A' }}</div>
          </div>
          <div class="info-item">
            <label>Email</label>
            <div class="info-value">{{ currentUser?.email || 'N/A' }}</div>
          </div>
        </div>
      </div>

      <div class="profile-section">
        <h2>Company Information</h2>
        <div class="companies-list" v-if="currentUser?.companies?.length">
          <div v-for="company in currentUser.companies" :key="company.id" class="company-card">
            <div class="company-header">
              <h3>{{ company.name }}</h3>
              <span class="role-badge">{{ company.role }}</span>
            </div>
            <div class="company-details">
              <div class="detail-item">
                <label>Company ID</label>
                <span>{{ company.id }}</span>
              </div>
              <div class="detail-item">
                <label>Status</label>
                <span :class="['status', company.is_active ? 'active' : 'inactive']">
                  {{ company.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-companies">
          No company associations found
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from '@/services/authService'

export default {
  name: 'ProfileView',
  
  data() {
    return {
      currentUser: null
    }
  },
  
  created() {
    this.currentUser = authService.getCurrentUser()
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

.profile-header {
  margin-bottom: 32px;
}

.profile-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #1e3c72;
}

.profile-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.profile-section h2 {
  font-size: 1.5rem;
  font-weight: 500;
  color: #2a5298;
  margin-bottom: 24px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item label {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

.info-value {
  font-size: 1rem;
  color: #111827;
  font-weight: 500;
  padding: 8px 12px;
  background: #f3f4f6;
  border-radius: 6px;
}

.companies-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.company-card {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.company-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.role-badge {
  background: #2a5298;
  color: white;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 500;
}

.company-details {
  display: grid;
  gap: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-item label {
  font-size: 0.9rem;
  color: #6b7280;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status.active {
  background: #dcfce7;
  color: #15803d;
}

.status.inactive {
  background: #fee2e2;
  color: #dc2626;
}

.no-companies {
  text-align: center;
  color: #6b7280;
  padding: 32px;
  background: #f3f4f6;
  border-radius: 8px;
  font-weight: 500;
}

@media (max-width: 640px) {
  .profile-container {
    padding: 16px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .companies-list {
    grid-template-columns: 1fr;
  }
}
</style>
