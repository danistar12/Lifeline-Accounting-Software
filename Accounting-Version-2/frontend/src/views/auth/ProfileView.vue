<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>User Profile</h1>
      <p>Manage your account settings and preferences</p>
    </div>

    <div class="profile-content">
      <!-- Profile Information Card -->
      <div class="card">
        <div class="card-header">
          <h2>Profile Information</h2>
          <button 
            v-if="!editingProfile" 
            @click="editingProfile = true" 
            class="btn btn-outline"
          >
            Edit Profile
          </button>
        </div>
        
        <div class="card-body">
          <div class="profile-avatar-section">
            <div class="avatar-container">
              <img 
                v-if="profile.avatar_url" 
                :src="profile.avatar_url" 
                :alt="profile.full_name"
                class="avatar-image"
              />
              <div v-else class="avatar-placeholder">
                {{ getInitials(profile.full_name || profile.username) }}
              </div>
              <input 
                ref="avatarInput"
                type="file" 
                accept="image/*" 
                @change="handleAvatarUpload"
                style="display: none"
              />
              <button @click="$refs.avatarInput.click()" class="avatar-upload-btn">
                📷
              </button>
            </div>
          </div>

          <form v-if="editingProfile" @submit.prevent="saveProfile" class="profile-form">
            <div class="form-row">
              <div class="form-group">
                <label>First Name</label>
                <input 
                  v-model="editForm.first_name" 
                  type="text" 
                  class="form-input"
                  placeholder="First Name"
                />
              </div>
              <div class="form-group">
                <label>Last Name</label>
                <input 
                  v-model="editForm.last_name" 
                  type="text" 
                  class="form-input"
                  placeholder="Last Name"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label>Email</label>
              <input 
                v-model="editForm.email" 
                type="email" 
                class="form-input"
                placeholder="Email"
              />
            </div>
            
            <div class="form-group">
              <label>Phone</label>
              <input 
                v-model="editForm.phone" 
                type="tel" 
                class="form-input"
                placeholder="Phone Number"
              />
            </div>
            
            <div class="form-group">
              <label>Notes</label>
              <textarea 
                v-model="editForm.user_notes" 
                class="form-textarea"
                placeholder="Additional notes..."
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-actions">
              <button type="submit" :disabled="loading" class="btn btn-primary">
                {{ loading ? 'Saving...' : 'Save Changes' }}
              </button>
              <button type="button" @click="cancelEdit" class="btn btn-outline">
                Cancel
              </button>
            </div>
          </form>

          <div v-else class="profile-display">
            <div class="info-row">
              <span class="label">Full Name:</span>
              <span class="value">{{ profile.full_name || 'Not set' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Username:</span>
              <span class="value">{{ profile.username }}</span>
            </div>
            <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ profile.email || 'Not set' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Phone:</span>
              <span class="value">{{ profile.phone || 'Not set' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Member Since:</span>
              <span class="value">{{ formatDate(profile.created_date) }}</span>
            </div>
            <div v-if="profile.user_notes" class="info-row">
              <span class="label">Notes:</span>
              <span class="value">{{ profile.user_notes }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Change Password Card -->
      <div class="card">
        <div class="card-header">
          <h2>Change Password</h2>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="changePassword" class="password-form">
            <div class="form-group">
              <label>Current Password</label>
              <input 
                v-model="passwordForm.current_password" 
                type="password" 
                class="form-input"
                required
              />
            </div>
            
            <div class="form-group">
              <label>New Password</label>
              <input 
                v-model="passwordForm.new_password" 
                type="password" 
                class="form-input"
                required
                minlength="8"
              />
            </div>
            
            <div class="form-group">
              <label>Confirm New Password</label>
              <input 
                v-model="passwordForm.confirm_password" 
                type="password" 
                class="form-input"
                required
              />
            </div>
            
            <button type="submit" :disabled="loading" class="btn btn-primary">
              {{ loading ? 'Changing...' : 'Change Password' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Company Roles Card -->
      <div class="card">
        <div class="card-header">
          <h2>Company Access</h2>
        </div>
        
        <div class="card-body">
          <div v-if="profile.companies && profile.companies.length > 0" class="companies-list">
            <div v-for="company in profile.companies" :key="company.company_id" class="company-item">
              <div class="company-info">
                <h3>{{ company.company_name }}</h3>
                <span class="role-badge">{{ company.role }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-companies">
            <p>You don't have access to any companies yet.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>
</template>

<script>
import authService from '@/services/authService'

export default {
  name: 'UserProfileView',
  data() {
    return {
      profile: {},
      editingProfile: false,
      loading: false,
      message: '',
      messageType: 'success',
      editForm: {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        user_notes: ''
      },
      passwordForm: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      }
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      try {
        this.loading = true
        const response = await authService.getUserProfile()
        this.profile = response.data
        
        // Initialize edit form with current data
        this.editForm = {
          first_name: this.profile.first_name || '',
          last_name: this.profile.last_name || '',
          email: this.profile.email || '',
          phone: this.profile.phone || '',
          user_notes: this.profile.user_notes || ''
        }
      } catch (error) {
        console.error('Error loading profile:', error)
        this.showMessage('Failed to load profile', 'error')
      } finally {
        this.loading = false
      }
    },

    async saveProfile() {
      try {
        this.loading = true
        const response = await authService.updateProfile(this.editForm)
        this.profile = response.data
        this.editingProfile = false
        this.showMessage('Profile updated successfully!', 'success')
        
        // Update user in localStorage
        const user = authService.getCurrentUser()
        if (user) {
          Object.assign(user, {
            first_name: this.profile.first_name,
            last_name: this.profile.last_name,
            email: this.profile.email
          })
          localStorage.setItem('user', JSON.stringify(user))
        }
      } catch (error) {
        console.error('Error saving profile:', error)
        this.showMessage('Failed to update profile', 'error')
      } finally {
        this.loading = false
      }
    },

    cancelEdit() {
      this.editingProfile = false
      // Reset form to original values
      this.editForm = {
        first_name: this.profile.first_name || '',
        last_name: this.profile.last_name || '',
        email: this.profile.email || '',
        phone: this.profile.phone || '',
        user_notes: this.profile.user_notes || ''
      }
    },

    async changePassword() {
      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        this.showMessage('New passwords do not match', 'error')
        return
      }

      try {
        this.loading = true
        await authService.changePassword(this.passwordForm)
        this.showMessage('Password changed successfully!', 'success')
        
        // Clear password form
        this.passwordForm = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
      } catch (error) {
        console.error('Error changing password:', error)
        this.showMessage(error.response?.data?.error || 'Failed to change password', 'error')
      } finally {
        this.loading = false
      }
    },

    async handleAvatarUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      try {
        this.loading = true
        const response = await authService.uploadAvatar(file)
        this.showMessage('Avatar uploaded successfully!', 'success')
        await this.loadProfile() // Reload to get new avatar URL
      } catch (error) {
        console.error('Error uploading avatar:', error)
        this.showMessage(error.response?.data?.error || 'Failed to upload avatar', 'error')
      } finally {
        this.loading = false
      }
    },

    getInitials(name) {
      return name
        .split(' ')
        .map(word => word.charAt(0))
        .join('')
        .toUpperCase()
        .slice(0, 2)
    },

    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      return new Date(dateString).toLocaleDateString()
    },

    showMessage(text, type = 'success') {
      this.message = text
      this.messageType = type
      setTimeout(() => {
        this.message = ''
      }, 5000)
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  margin-bottom: 32px;
}

.profile-header h1 {
  color: #1e3c72;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.profile-header p {
  color: #6b7280;
  font-size: 1rem;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  background: #f8f9fa;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  color: #1e3c72;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.card-body {
  padding: 24px;
}

.profile-avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e5e7eb;
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 600;
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #2a5298;
  color: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  font-size: 1rem;
}

.profile-form, .password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.form-input, .form-textarea {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #2a5298;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.profile-display {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-row .label {
  font-weight: 600;
  color: #374151;
  min-width: 120px;
}

.info-row .value {
  color: #6b7280;
}

.companies-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.company-item {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.company-info h3 {
  margin: 0 0 8px 0;
  color: #1e3c72;
  font-size: 1.1rem;
}

.role-badge {
  background: #e3eafc;
  color: #2a5298;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 0.875rem;
  font-weight: 600;
}

.no-companies {
  text-align: center;
  color: #6b7280;
  padding: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
  color: white;
}

.btn-outline {
  background: white;
  color: #2a5298;
  border: 2px solid #2a5298;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 16px 24px;
  border-radius: 8px;
  font-weight: 600;
  z-index: 1000;
}

.message.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.message.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
