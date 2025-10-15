<template>
  <div class="profile-container">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="icon-user"></i>
          My Profile
        </h1>
        <p class="page-subtitle">Manage your account information and preferences</p>
      </div>
      <div class="header-actions">
        <button v-if="!editMode" class="btn btn-primary" @click="enableEditMode">
          <i class="icon-edit"></i>
          Edit Profile
        </button>
        <button v-if="editMode" class="btn btn-outline" @click="cancelEdit">
          Cancel
        </button>
        <button v-if="editMode" class="btn btn-primary" @click="saveProfile" :disabled="saving">
          <span v-if="saving">Saving...</span>
          <span v-else>Save Changes</span>
        </button>
      </div>
    </div>

    <div class="profile-content">
      <!-- Profile Card -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar-container">
            <div class="profile-avatar" @click="editMode && $refs.photoInput.click()" :class="{ 'editable': editMode }">
              <img v-if="profilePhoto || user?.profile_photo" :src="profilePhoto || user?.profile_photo" alt="Profile Photo" class="avatar-photo" />
              <span v-else class="avatar-initials">{{ userInitials }}</span>
              <div v-if="editMode" class="avatar-overlay">
                <i class="camera-icon" aria-hidden="true"></i>
              </div>
            </div>
            <input 
              ref="photoInput" 
              type="file" 
              accept="image/*" 
              @change="handlePhotoUpload" 
              style="display: none;"
            >
            <div v-if="editMode && (profilePhoto || user?.profile_photo)" class="photo-actions">
              <button @click="removePhoto" class="btn btn-text btn-small">Remove Photo</button>
            </div>
          </div>
          <div class="profile-info">
            <h2>{{ displayName }}</h2>
            <p class="username">@{{ user?.user?.username || user?.username }}</p>
            <p class="join-date">Member since {{ formatDate(user?.user?.date_joined || user?.date_joined) }}</p>
          </div>
        </div>
      </div>

      <!-- Profile Form -->
      <div class="profile-form-section">
        <form @submit.prevent="saveProfile" class="profile-form">
          <!-- Personal Information -->
          <div class="form-section">
            <h3>Personal Information</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="firstName">First Name</label>
                <input 
                  id="firstName"
                  v-model="profileForm.FirstName"
                  type="text" 
                  class="form-control" 
                  :readonly="!editMode"
                  placeholder="Enter your first name"
                >
              </div>
              <div class="form-group">
                <label for="lastName">Last Name</label>
                <input 
                  id="lastName"
                  v-model="profileForm.LastName"
                  type="text" 
                  class="form-control" 
                  :readonly="!editMode"
                  placeholder="Enter your last name"
                >
              </div>
            </div>
            
            <div class="form-group">
              <label for="email">Email Address</label>
              <input 
                id="email"
                v-model="profileForm.Email"
                type="email" 
                class="form-control" 
                :readonly="!editMode"
                placeholder="Enter your email address"
              >
            </div>
            
            <div class="form-group">
              <label for="userNotes">Notes</label>
              <textarea 
                id="userNotes"
                v-model="profileForm.UserNotes"
                class="form-control" 
                rows="4"
                :readonly="!editMode"
                placeholder="Add any notes about yourself"
              ></textarea>
            </div>
          </div>

          <!-- Account Information -->
          <div class="form-section">
            <h3>Account Information</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="username">Username</label>
                <input 
                  id="username"
                  v-model="profileForm.username"
                  type="text" 
                  class="form-control" 
                  readonly
                  placeholder="Username cannot be changed"
                >
                <small class="form-text">Username cannot be modified</small>
              </div>
              <div class="form-group">
                <label>Account Status</label>
                <div class="status-badge active">
                  <i class="icon-check"></i>
                  Active
                </div>
              </div>
            </div>
          </div>

          <!-- Company Roles -->
          <div class="form-section">
            <h3>Company Access</h3>
            <div class="company-roles">
              <div v-if="companyRoles.length === 0" class="no-companies">
                <p>You don't have access to any companies yet.</p>
                <router-link to="/accounts/companies" class="btn btn-outline">
                  <i class="icon-building"></i>
                  Manage Companies
                </router-link>
              </div>
              <div v-for="role in companyRoles" :key="role.UserCompanyRoleID || role.user_company_role_id" class="company-role-card">
                <div class="company-avatar">
                  {{ getCompanyInitials(role.Company?.CompanyName || role.company?.company_name) }}
                </div>
                <div class="company-details">
                  <h4>{{ role.Company?.CompanyName || role.company?.company_name }}</h4>
                  <p class="role">{{ role.Role || role.role }}</p>
                  <small class="join-date">Joined {{ formatDate(role.CreatedDate || role.created_date) }}</small>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import axios from 'axios';

export default {
  name: 'ProfileView',
  data() {
    return {
      editMode: false,
      saving: false,
      companyRoles: [],
      profilePhoto: null,
      profileForm: {
        username: '',
        FirstName: '',
        LastName: '',
        Email: '',
        UserNotes: ''
      },
      originalForm: {}
    };
  },
  computed: {
    ...mapState(['user']),
    displayName() {
      if (!this.user) return '';

      const userData = this.user.user || this.user;
      const first = userData.FirstName ?? userData.first_name;
      const last = userData.LastName ?? userData.last_name;
      if (first && last) return `${first} ${last}`;
      if (first) return first;
      return userData.username || 'User';
    },
    userInitials() {
      if (!this.user) return 'U';

      const userData = this.user.user || this.user;
      const first = userData.FirstName ?? userData.first_name;
      const last = userData.LastName ?? userData.last_name;
      if (first && last) return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase();
      if (first) return first.charAt(0).toUpperCase();
      if (userData.username) return userData.username.charAt(0).toUpperCase();
      return 'U';
    }
  },
  methods: {
    ...mapActions(['me']),
    
    async loadProfileData() {
      try {
        // Load user data
        const response = await axios.get('/api/accounts/auth/user/');
        const userData = response.data.user;
        
        this.profileForm = {
          username: userData.username || '',
          FirstName: userData.FirstName ?? userData.first_name ?? '',
          LastName: userData.LastName ?? userData.last_name ?? '',
          Email: userData.Email ?? userData.email ?? '',
          UserNotes: userData.UserNotes ?? userData.user_notes ?? ''
        };
        
        // Store original form data for cancel functionality
        this.originalForm = { ...this.profileForm };
        
        // Load company roles
        this.companyRoles = response.data.company_roles || [];
        
      } catch (error) {
        console.error('Failed to load profile data:', error);
      }
    },
    
    enableEditMode() {
      this.editMode = true;
    },
    
    cancelEdit() {
      this.editMode = false;
      this.profileForm = { ...this.originalForm };
    },
    
    async saveProfile() {
      this.saving = true;
        try {
        // send both canonical CamelCase and legacy snake_case keys
        await axios.patch('/api/accounts/auth/user/', {
          FirstName: this.profileForm.FirstName,
          LastName: this.profileForm.LastName,
          Email: this.profileForm.Email,
          UserNotes: this.profileForm.UserNotes,
          first_name: this.profileForm.FirstName,
          last_name: this.profileForm.LastName,
          email: this.profileForm.Email,
          user_notes: this.profileForm.UserNotes
        });
        
        // Update the store with new user data
        await this.me();
        
        // Update original form data
        this.originalForm = { ...this.profileForm };
        
        this.editMode = false;
        console.log('Profile updated successfully');
        
      } catch (error) {
        console.error('Failed to update profile:', error);
        alert('Failed to update profile. Please try again.');
      } finally {
        this.saving = false;
      }
    },
    
    handlePhotoUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file');
        return;
      }
      
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB');
        return;
      }
      
      // Create a preview URL
      const reader = new FileReader();
      reader.onload = (e) => {
        this.profilePhoto = e.target.result;
      };
      reader.readAsDataURL(file);
      
      // Upload the file
      this.uploadProfilePhoto(file);
    },
    
    async uploadProfilePhoto(file) {
      const formData = new FormData();
      formData.append('profile_photo', file);
      
      try {
        console.log('Uploading profile photo...', file);
        const response = await axios.patch('/api/accounts/auth/user/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        console.log('Upload response:', response.data);
        
        // Update the store with new user data
        await this.me();
        
        console.log('Profile photo updated successfully');
        
      } catch (error) {
        console.error('Failed to upload profile photo:', error);
        console.error('Error response:', error.response?.data);
        alert('Failed to upload profile photo. Please try again.');
        // Reset the preview on error
        this.profilePhoto = null;
      }
    },
    
    async removePhoto() {
      try {
        await axios.patch('/api/accounts/auth/user/', {
          profile_photo: null
        });
        
        // Update the store with new user data
        await this.me();
        
        console.log('Profile photo removed successfully');
        
      } catch (error) {
        console.error('Failed to remove profile photo:', error);
        alert('Failed to remove profile photo. Please try again.');
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Unknown';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    },
    
    getCompanyInitials(name) {
      if (!name) return 'CN'; // Company Name
      
      return name.split(' ')
        .map(word => word.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2);
    }
  },
  
  async mounted() {
    await this.loadProfileData();
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.header-content h1 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-content p {
  margin: 0;
  color: #6c757d;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.icon-user::before { content: ''; }
.icon-edit::before { content: ''; }
.icon-check::before { content: ''; }
.icon-building::before { content: ''; }

/* Profile Card */
.profile-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.profile-avatar-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 2rem;
  position: relative;
  overflow: hidden;
  cursor: default;
  transition: all 0.2s;
}

.profile-avatar.editable {
  cursor: pointer;
}

.profile-avatar.editable:hover {
  transform: scale(1.05);
}

.avatar-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-initials {
  font-size: 2rem;
  font-weight: 700;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  border-radius: 50%;
}

.profile-avatar.editable:hover .avatar-overlay {
  opacity: 1;
}

.camera-icon {
  font-size: 1.5rem;
}

.photo-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.btn-text {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  text-decoration: underline;
}

.btn-text:hover {
  color: #dc3545;
}

.profile-info h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.profile-info .username {
  margin: 0 0 0.25rem 0;
  color: #007bff;
  font-weight: 500;
}

.profile-info .join-date {
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

/* Form */
.profile-form-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-form {
  padding: 2rem;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.form-section h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
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

.form-control[readonly] {
  background-color: #f8f9fa;
  color: #6c757d;
}

.form-text {
  color: #6c757d;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #d4edda;
  color: #155724;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Company Roles */
.company-roles {
  display: grid;
  gap: 1rem;
}

.no-companies {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.company-role-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  background-color: #f8f9fa;
}

.company-avatar {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
}

.company-details h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.company-details .role {
  margin: 0 0 0.25rem 0;
  color: #007bff;
  font-weight: 500;
}

.company-details .join-date {
  margin: 0;
  color: #6c757d;
  font-size: 0.8rem;
}

/* Buttons */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-outline {
  background-color: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline:hover {
  background-color: #007bff;
  color: white;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .profile-form {
    padding: 1.5rem;
  }
}
</style>
