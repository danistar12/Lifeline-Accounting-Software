
<template>
  <div v-if="isAuthenticated" class="app-container">
    <!-- Top Navigation Bar -->
    <header class="top-nav">
      <div class="nav-left">
        <div class="logo-section">
          <img src="/logo.png" alt="Lifeline Logo" class="logo" />
          <h1 class="app-title">Lifeline Accounting</h1>
        </div>
      </div>
      
      <nav class="nav-menu">
        <!-- Dashboard -->
        <router-link to="/" class="nav-item" :class="{ active: $route.name === 'dashboard' }">
          <span class="icon">🏠</span>
          <span>Dashboard</span>
        </router-link>
        
        <!-- Customers & Vendors Dropdown -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['customers', 'vendors'].includes($route.name) || activeDropdown === 'contacts' }"
               @click="toggleDropdown('contacts')">
            <span class="icon">👥</span>
            <span>Contacts</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'contacts'" class="dropdown-menu">
            <router-link to="/customers" class="dropdown-item">
              <span class="icon">👤</span>
              <span>Customers</span>
            </router-link>
            <router-link to="/vendors" class="dropdown-item">
              <span class="icon">🚚</span>
              <span>Vendors</span>
            </router-link>
          </div>
        </div>
        
        <!-- Financial Dropdown -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['payments', 'banking', 'invoices', 'bills'].includes($route.name) || activeDropdown === 'financial' }"
               @click="toggleDropdown('financial')">
            <span class="icon">💰</span>
            <span>Financial</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'financial'" class="dropdown-menu">
            <router-link to="/payments" class="dropdown-item">
              <span class="icon">💳</span>
              <span>Payments</span>
            </router-link>
            <router-link to="/banking" class="dropdown-item">
              <span class="icon">🏦</span>
              <span>Banking</span>
            </router-link>
            <router-link to="/invoices" class="dropdown-item">
              <span class="icon">📧</span>
              <span>Invoices</span>
            </router-link>
            <router-link to="/bills" class="dropdown-item">
              <span class="icon">📄</span>
              <span>Bills</span>
            </router-link>
          </div>
        </div>
        
        <!-- Operations Dropdown -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['projects', 'inventory', 'payroll'].includes($route.name) || activeDropdown === 'operations' }"
               @click="toggleDropdown('operations')">
            <span class="icon">⚙️</span>
            <span>Operations</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'operations'" class="dropdown-menu">
            <router-link to="/projects" class="dropdown-item">
              <span class="icon">📋</span>
              <span>Projects</span>
            </router-link>
            <router-link to="/inventory" class="dropdown-item">
              <span class="icon">📦</span>
              <span>Inventory</span>
            </router-link>
            <router-link to="/payroll" class="dropdown-item">
              <span class="icon">💼</span>
              <span>Payroll</span>
            </router-link>
          </div>
        </div>
        
        <!-- Reports & More Dropdown -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['reports', 'documents', 'subscriptions'].includes($route.name) || activeDropdown === 'reports' }"
               @click="toggleDropdown('reports')">
            <span class="icon">📊</span>
            <span>Reports & More</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'reports'" class="dropdown-menu">
            <router-link to="/reports" class="dropdown-item">
              <span class="icon">📊</span>
              <span>Reports</span>
            </router-link>
            <router-link to="/documents" class="dropdown-item">
              <span class="icon">📄</span>
              <span>Documents</span>
            </router-link>
            <router-link to="/subscriptions" class="dropdown-item">
              <span class="icon">🔄</span>
              <span>Subscriptions</span>
            </router-link>
          </div>
        </div>
      </nav>
      
      <!-- User Menu -->
      <div class="nav-right">
        <div class="user-menu">
          <div class="user-info dropdown-trigger" @click="toggleDropdown('user')">
            <div class="user-avatar">
              <span>{{ getUserInitials() }}</span>
            </div>
            <div class="user-details">
              <div class="user-name">{{ currentUser?.username || 'User' }}</div>
              <div class="user-role">{{ getCurrentRole() }}</div>
            </div>
            <span class="dropdown-arrow" :class="{ 'dropdown-arrow-active': activeDropdown === 'user' }">▼</span>
          </div>
          
          <div v-show="activeDropdown === 'user'" class="dropdown-menu user-dropdown">
            <router-link to="/profile" class="dropdown-item">
              <span class="icon">👤</span>
              <span>Profile</span>
            </router-link>
            <div class="dropdown-divider"></div>
            <button @click="handleLogout" class="dropdown-item logout-btn">
              <span class="icon">🚪</span>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Main Content Area -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
  
  <!-- Show router-view directly for login page when not authenticated -->
  <div v-else class="auth-container">
    <router-view />
  </div>
</template>

<script>
import authService from '@/services/authService'

export default {
  data() {
    return {
      isAuthenticated: false,
      currentUser: null,
      activeDropdown: null
    }
  },
  
  async mounted() {
    // Initialize authentication
    authService.initializeAuth()
    this.checkAuthentication()
    
    // Add click outside listener
    document.addEventListener('click', this.handleGlobalClick)
    
    // Listen for route changes to update auth state
    this.$router.beforeEach(() => {
      this.checkAuthentication()
      // Close dropdowns on route change
      this.activeDropdown = null
    })
  },
  
  methods: {
    checkAuthentication() {
      this.isAuthenticated = authService.isAuthenticated()
      this.currentUser = authService.getCurrentUser()
    },
    
    showDropdown(dropdown) {
      this.activeDropdown = dropdown
    },
    
    hideDropdown(dropdown) {
      if (this.activeDropdown === dropdown) {
        this.activeDropdown = null
      }
    },
    
    toggleDropdown(dropdown) {
      // If clicking the same dropdown, close it
      if (this.activeDropdown === dropdown) {
        this.activeDropdown = null
      } else {
        // If clicking a different dropdown, close the current one and open the new one
        this.activeDropdown = dropdown
      }
      // Prevent the click from bubbling up to the document click handler
      event.stopPropagation()
    },
    
    // Handle clicks anywhere in the document
    handleGlobalClick(event) {
      const target = event.target
      
      // If click is outside all dropdowns, close them
      if (!target.closest('.nav-dropdown') && !target.closest('.user-menu')) {
        this.activeDropdown = null
      }
    },
    
    getUserInitials() {
      if (this.currentUser?.first_name && this.currentUser?.last_name) {
        return `${this.currentUser.first_name.charAt(0)}${this.currentUser.last_name.charAt(0)}`.toUpperCase()
      }
      return this.currentUser?.username?.charAt(0)?.toUpperCase() || 'U'
    },
    
    getCurrentRole() {
      if (this.currentUser?.companies && this.currentUser.companies.length > 0) {
        return this.currentUser.companies[0].role
      }
      return 'User'
    },
    
    async handleLogout() {
      try {
        await authService.logout()
        this.isAuthenticated = false
        this.currentUser = null
        this.activeDropdown = null
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
        // Force logout even if API call fails
        this.isAuthenticated = false
        this.currentUser = null
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  background: linear-gradient(120deg, #e3eafc 0%, #f8fbff 100%);
  box-sizing: border-box;
}

.auth-container {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
}

/* Top Navigation Bar */
.top-nav {
  background: linear-gradient(120deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  padding: 12px 24px;
  box-shadow: 0 2px 12px rgba(30,60,114,0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  object-fit: contain;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin: 0;
  color: white;
}

/* Navigation Menu */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  justify-content: center;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
  font-weight: 500;
  white-space: nowrap;
}

.nav-item:hover, .nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.nav-item .icon {
  font-size: 1.1rem;
}

/* Dropdown Containers */
.nav-dropdown {
  position: relative;
}

.dropdown-trigger {
  cursor: pointer;
}

.dropdown-arrow {
  font-size: 0.7rem;
  margin-left: 4px;
  opacity: 0.8;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  overflow: hidden;
  margin-top: 8px;
  z-index: 1001;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: #374151;
  text-decoration: none;
  transition: background 0.2s;
  width: 100%;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item .icon {
  font-size: 1rem;
  width: 20px;
  text-align: center;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 4px 0;
}

/* User Menu */
.nav-right {
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
  color: white;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1.2;
}

.user-role {
  font-size: 0.75rem;
  opacity: 0.8;
  line-height: 1.2;
}

.user-dropdown {
  right: 0;
  min-width: 180px;
}

.logout-btn {
  color: #dc2626;
}

.logout-btn:hover {
  background: #fef2f2;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 32px;
  background: #f8fbff;
  overflow-y: auto;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .nav-menu {
    gap: 4px;
  }
  
  .nav-item {
    padding: 10px 12px;
    font-size: 0.9rem;
  }
  
  .app-title {
    font-size: 1.3rem;
  }
}

@media (max-width: 900px) {
  .top-nav {
    padding: 8px 16px;
  }
  
  .logo {
    width: 40px;
    height: 40px;
  }
  
  .app-title {
    display: none;
  }
  
  .nav-menu {
    gap: 2px;
  }
  
  .nav-item span:not(.icon) {
    display: none;
  }
  
  .nav-item {
    padding: 10px;
  }
  
  .dropdown-arrow {
    display: none;
  }
  
  .user-details {
    display: none;
  }
  
  .main-content {
    padding: 16px;
  }
}

@media (max-width: 640px) {
  .logo-section {
    gap: 8px;
  }
  
  .nav-menu {
    display: none;
  }
  
  .top-nav {
    justify-content: space-between;
  }
  
  .user-avatar {
    width: 36px;
    height: 36px;
  }
}
</style>