<template>
  <div class="settings-container">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="icon-settings"></i>
          Settings
        </h1>
        <p class="page-subtitle">Manage your application preferences and security settings</p>
      </div>
    </div>

    <div class="settings-content">
      <!-- Account Security -->
      <div class="settings-section">
        <div class="section-header">
          <h3>Account Security</h3>
          <p>Manage your password and security preferences</p>
        </div>
        
        <div class="settings-card">
          <form @submit.prevent="changePassword" class="security-form">
            <div class="form-group">
              <label for="currentPassword">Current Password</label>
              <input 
                id="currentPassword"
                v-model="passwordForm.current_password"
                type="password" 
                class="form-control" 
                required
                placeholder="Enter your current password"
              >
            </div>
            
            <div class="form-group">
              <label for="newPassword">New Password</label>
              <input 
                id="newPassword"
                v-model="passwordForm.new_password"
                type="password" 
                class="form-control" 
                required
                placeholder="Enter your new password"
              >
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">Confirm New Password</label>
              <input 
                id="confirmPassword"
                v-model="passwordForm.confirm_password"
                type="password" 
                class="form-control" 
                required
                placeholder="Confirm your new password"
              >
            </div>
            
            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="changingPassword">
                <span v-if="changingPassword">Changing Password...</span>
                <span v-else>Change Password</span>
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Application Preferences -->
      <div class="settings-section">
        <div class="section-header">
          <h3>Application Preferences</h3>
          <p>Customize your application experience</p>
        </div>
        
        <div class="settings-card">
          <div class="preference-item">
            <div class="preference-info">
              <h4>Email Notifications</h4>
              <p>Receive email notifications for important updates</p>
            </div>
            <div class="preference-control">
              <label class="switch">
                <input type="checkbox" v-model="preferences.email_notifications">
                <span class="slider"></span>
              </label>
            </div>
          </div>
          
          <div class="preference-item">
            <div class="preference-info">
              <h4>Desktop Notifications</h4>
              <p>Show desktop notifications for real-time updates</p>
            </div>
            <div class="preference-control">
              <label class="switch">
                <input type="checkbox" v-model="preferences.desktop_notifications">
                <span class="slider"></span>
              </label>
            </div>
          </div>
          
          <div class="preference-item">
            <div class="preference-info">
              <h4>Auto-save Forms</h4>
              <p>Automatically save form data as you type</p>
            </div>
            <div class="preference-control">
              <label class="switch">
                <input type="checkbox" v-model="preferences.auto_save">
                <span class="slider"></span>
              </label>
            </div>
          </div>
          
          <div class="form-actions">
            <button @click="savePreferences" class="btn btn-primary" :disabled="savingPreferences">
              <span v-if="savingPreferences">Saving...</span>
              <span v-else>Save Preferences</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Data Management -->
      <div class="settings-section">
        <div class="section-header">
          <h3>Data Management</h3>
          <p>Export or manage your account data</p>
        </div>
        
        <div class="settings-card">
          <div class="data-item">
            <div class="data-info">
              <h4>Export Data</h4>
              <p>Download a copy of your personal data and company information</p>
            </div>
            <div class="data-control">
              <button @click="exportData" class="btn btn-outline" :disabled="exporting">
                <span v-if="exporting">Exporting...</span>
                <span v-else>Export Data</span>
              </button>
            </div>
          </div>
          
          <div class="data-item danger">
            <div class="data-info">
              <h4>Delete Account</h4>
              <p>Permanently delete your account and all associated data</p>
            </div>
            <div class="data-control">
              <button @click="confirmDeleteAccount" class="btn btn-danger">
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Tools Section (Only visible to admins) -->
      <div class="settings-section" v-if="isAdmin">
        <div class="section-header">
          <h3>Administrator Tools</h3>
          <p>Advanced tools for system administrators</p>
        </div>
        
        <div class="settings-card">
          <div class="admin-item">
            <div class="admin-info">
              <h4>Audit Logs</h4>
              <p>Review system activity and user actions</p>
            </div>
            <div class="admin-control">
              <router-link to="/audit-logs" class="btn btn-primary">
                View Audit Logs
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  name: 'SettingsView',
  data() {
    return {
      changingPassword: false,
      savingPreferences: false,
      exporting: false,
      passwordForm: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      },
      preferences: {
        email_notifications: true,
        desktop_notifications: false,
        auto_save: true
      },
      userSettings: {},
    };
  },
  computed: {
    isAdmin() {
      const user = this.$store.state.user;
      if (!user) return false;
      const userData = user.user || user;
      return userData.is_staff || userData.is_superuser || (userData.role && userData.role.toLowerCase().includes('admin'));
    }
  },
  mounted() {
    this.fetchUserSettings();
  },
  methods: {
    async fetchUserSettings() {
      try {
        const res = await axios.get('/api/settings/settings/user/');
        this.userSettings = res.data;
        // Optionally map backend settings to preferences here
      } catch (error) {
        console.error('Failed to fetch user settings:', error);
      }
    },
    async changePassword() {
      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        alert('New passwords do not match!');
        return;
      }
      this.changingPassword = true;
      try {
        // Replace with your actual password change endpoint if different
        await axios.post('/api/accounts/change-password/', this.passwordForm);
        alert('Password changed successfully!');
        this.passwordForm = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        };
      } catch (error) {
        console.error('Failed to change password:', error);
        alert('Failed to change password. Please try again.');
      } finally {
        this.changingPassword = false;
      }
    },
    async savePreferences() {
      this.savingPreferences = true;
      try {
        // Update user settings/preferences
        await axios.post('/api/settings/settings/update_user/', this.preferences);
        alert('Preferences saved successfully!');
      } catch (error) {
        console.error('Failed to save preferences:', error);
        alert('Failed to save preferences. Please try again.');
      } finally {
        this.savingPreferences = false;
      }
    },
    async exportData() {
      this.exporting = true;
      try {
        // Example: download user data (implement backend as needed)
        const res = await axios.get('/api/settings/settings/user/', { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'user_data.json');
        document.body.appendChild(link);
        link.click();
        link.remove();
        alert('Data export completed! Check your downloads folder.');
      } catch (error) {
        console.error('Failed to export data:', error);
        alert('Failed to export data. Please try again.');
      } finally {
        this.exporting = false;
      }
    },
    confirmDeleteAccount() {
      const confirmed = confirm(
        'Are you sure you want to delete your account? This action cannot be undone and will permanently delete all your data.'
      );
      if (confirmed) {
        const doubleConfirmed = confirm(
          'This is your final warning. Deleting your account will remove all companies, transactions, and data associated with your account. Are you absolutely sure?'
        );
        if (doubleConfirmed) {
          this.deleteAccount();
        }
      }
    },
    async deleteAccount() {
      try {
        // Implement account deletion endpoint as needed
        await axios.post('/api/accounts/delete/', {});
        alert('Account deleted. Logging out...');
        // Optionally redirect or log out user
        window.location.href = '/login';
      } catch (error) {
        console.error('Failed to delete account:', error);
        alert('Failed to delete account. Please contact support.');
      }
    }
  }
};
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

/* Header */
.page-header {
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

.icon-settings::before { content: '⚙️'; }

/* Settings Sections */
.settings-section {
  margin-bottom: 3rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
}

.section-header p {
  margin: 0;
  color: #6c757d;
}

.settings-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Forms */
.security-form .form-group {
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

.form-actions {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

/* Preferences */
.preference-item, .data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.preference-item:last-of-type, .data-item:last-of-type {
  border-bottom: none;
}

.preference-info h4, .data-info h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.preference-info p, .data-info p {
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #007bff;
}

input:checked + .slider:before {
  transform: translateX(26px);
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

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Danger zone */
.data-item.danger {
  background-color: #fff5f5;
  border-radius: 6px;
  padding: 1.5rem;
  border: 1px solid #fed7d7;
}

.data-item.danger .data-info h4 {
  color: #c53030;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .settings-card {
    padding: 1.5rem;
  }
  
  .preference-item, .data-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .preference-control, .data-control {
    align-self: stretch;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
