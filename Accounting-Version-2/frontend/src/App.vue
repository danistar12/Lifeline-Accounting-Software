
<template>
  <div v-if="isAuthenticated" class="app-container">
    <header class="top-nav">
      <!-- Left Section: Logo & Mobile Menu -->
      <div class="nav-left">
        <button class="mobile-menu-button" :class="{ active: showMobileMenu }" @click="toggleMobileMenu">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
        <div class="logo-section">
          <img src="/logo.png" alt="Logo" class="logo desktop-logo">
          <h1 class="app-title">Lifeline</h1>
        </div>
      </div>

      <nav class="nav-menu" :class="{ 'mobile-open': showMobileMenu }">
        <!-- Dashboard -->
        <router-link to="/dashboard" class="nav-item" :class="{ active: $route.name === 'dashboard' }" @click="closeMobileMenu">
          <span class="icon">📊</span>
          <span>Dashboard</span>
        </router-link>

        <!-- Business Dropdown -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['customers', 'vendors', 'projects', 'inventory'].includes($route.name) || activeDropdown === 'business' }"
               @click="toggleDropdown('business')">
            <span class="icon">🏢</span>
            <span>Business</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'business'" class="dropdown-menu">
            <router-link to="/customers" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">👤</span>
              <span>Customers</span>
            </router-link>
            <router-link to="/vendors" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">🚚</span>
              <span>Vendors</span>
            </router-link>
            <router-link to="/projects" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">📋</span>
              <span>Projects</span>
            </router-link>
            <router-link to="/inventory" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">📦</span>
              <span>Inventory</span>
            </router-link>
          </div>
        </div>

        <!-- Banking & Payments -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['banking', 'payments', 'invoices', 'bills'].includes($route.name) || activeDropdown === 'banking' }"
               @click="toggleDropdown('banking')">
            <span class="icon">🏦</span>
            <span>Banking</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'banking'" class="dropdown-menu">
            <router-link to="/banking" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">🏦</span>
              <span>Accounts</span>
            </router-link>
            <router-link to="/payments" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">💳</span>
              <span>Payments</span>
            </router-link>
            <router-link to="/invoices" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">🧾</span>
              <span>Invoices</span>
            </router-link>
            <router-link to="/bills" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">📃</span>
              <span>Bills</span>
            </router-link>
          </div>
        </div>

        <!-- Financial -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['payroll', 'taxes', 'expenses'].includes($route.name) || activeDropdown === 'financial' }"
               @click="toggleDropdown('financial')">
            <span class="icon">💰</span>
            <span>Financial</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'financial'" class="dropdown-menu">
            <router-link to="/payroll" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">💼</span>
              <span>Payroll</span>
            </router-link>
            <router-link to="/taxes" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">📊</span>
              <span>Taxes</span>
            </router-link>
            <router-link to="/expenses" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">💸</span>
              <span>Expenses</span>
            </router-link>
          </div>
        </div>
        
        <!-- Reports & Admin -->
        <div class="nav-dropdown">
          <div class="nav-item dropdown-trigger" 
               :class="{ active: ['reports', 'documents', 'subscriptions'].includes($route.name) || activeDropdown === 'reports' }"
               @click="toggleDropdown('reports')">
            <span class="icon">📊</span>
            <span>Reports</span>
            <span class="dropdown-arrow">▼</span>
          </div>
          <div v-show="activeDropdown === 'reports'" class="dropdown-menu">
            <router-link to="/reports" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">📊</span>
              <span>Analytics</span>
            </router-link>
            <router-link to="/documents" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">📄</span>
              <span>Documents</span>
            </router-link>
            <router-link to="/subscriptions" class="dropdown-item" @click="closeMobileMenu">
              <span class="icon">🔄</span>
              <span>Subscriptions</span>
            </router-link>
          </div>
        </div>
      </nav>
      <!-- Right Section: Company Selector & User Menu -->
      <div class="nav-right">
        <!-- Company Selector -->
        <div class="company-selector" v-if="currentUser?.companies?.length > 0">
          <div class="company-dropdown dropdown-trigger" @click="toggleDropdown('company')">
            <div class="company-icon">🏢</div>
            <div class="company-name">{{ getActiveCompanyName() }}</div>
            <span class="dropdown-arrow" :class="{ 'dropdown-arrow-active': activeDropdown === 'company' }">▼</span>
          </div>
          
          <div v-show="activeDropdown === 'company'" class="dropdown-menu company-dropdown">
            <div v-for="company in currentUser.companies" :key="company.company_id" 
                 class="dropdown-item" 
                 :class="{ 'active-company': getActiveCompanyId() === company.company_id }"
                 @click="changeCompany(company.company_id)">
              <span class="icon">🏢</span>
              <span>{{ company.name }}</span>
              <span v-if="getActiveCompanyId() === company.company_id" class="check-icon">✓</span>
            </div>
          </div>
        </div>
      
        <!-- User Menu -->
        <div class="user-menu">
          <div class="user-info dropdown-trigger" @click="toggleDropdown('user')">
            <div class="user-avatar">
              <span>{{ getUserInitials() }}</span>
            </div>
            <div class="user-details desktop-only">
              <div class="user-name">{{ currentUser?.username || 'User' }}</div>
              <div class="user-role">{{ getCurrentRole() }}</div>
            </div>
            <span class="dropdown-arrow desktop-only" :class="{ 'dropdown-arrow-active': activeDropdown === 'user' }">▼</span>
          </div>
          
          <div v-show="activeDropdown === 'user'" class="dropdown-menu user-dropdown">
            <router-link to="/profile" class="dropdown-item" @click="closeMobileMenu">
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
    <div v-if="showMobileMenu" class="mobile-overlay" @click="closeMobileMenu"></div>
    <!-- Main Content Area -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
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
      activeDropdown: null,
      showMobileMenu: false
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
    
    getActiveCompanyId() {
      return localStorage.getItem('activeCompanyId') || 
        (this.currentUser?.companies && this.currentUser.companies.length > 0 
          ? this.currentUser.companies[0].company_id 
          : null)
    },
    
    getActiveCompanyName() {
      const activeCompanyId = this.getActiveCompanyId()
      const company = this.currentUser?.companies?.find(c => c.company_id == activeCompanyId)
      return company ? company.name : 'Select Company'
    },
    
    changeCompany(companyId) {
      localStorage.setItem('activeCompanyId', companyId)
      // Set header for future requests
      authService.setActiveCompany(companyId)
      // Reload current route to refresh data with new company
      this.$router.go()
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
    
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu
      // Close any open dropdowns when toggling mobile menu
      this.activeDropdown = null
    },
    
    closeMobileMenu() {
      this.showMobileMenu = false
      this.activeDropdown = null
    },
    
    // Handle clicks anywhere in the document
    handleGlobalClick(event) {
      const target = event.target
      
      // If click is outside all dropdowns and mobile menu, close them
      if (!target.closest('.nav-dropdown') && 
          !target.closest('.user-menu') && 
          !target.closest('.company-selector') &&
          !target.closest('.mobile-menu-button')) {
        this.activeDropdown = null
        this.showMobileMenu = false
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
        this.activeDropdown = null
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
  padding: 12px 20px;
  box-shadow: 0 2px 12px rgba(30,60,114,0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1000;
  min-height: 60px;
}

/* Left Section */
.nav-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: contain;
}

.app-title {
  font-size: 1.4rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin: 0;
  color: white;
}

/* Mobile Menu Button */
.mobile-menu-button {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 30px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
}

.hamburger-line {
  width: 25px;
  height: 3px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.mobile-menu-button.active .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.mobile-menu-button.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-button.active .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Navigation Menu */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 24px; /* Increased gap between sections */
  flex: 1;
  justify-content: center;
  max-width: 900px; /* Increased max-width to accommodate all sections */
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
  font-size: 0.95rem;
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
  transition: transform 0.2s;
}

.dropdown-arrow-active {
  transform: rotate(180deg);
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

/* Right Section */
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

/* Company Selector */
.company-selector {
  position: relative;
}

.company-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  background: rgba(255, 255, 255, 0.1);
  min-width: 140px;
}

.company-dropdown:hover {
  background: rgba(255, 255, 255, 0.15);
}

.company-icon {
  font-size: 1rem;
}

.company-name {
  font-weight: 500;
  white-space: nowrap;
  font-size: 0.9rem;
}

.company-dropdown .dropdown-menu {
  right: 0;
  left: auto;
  min-width: 220px;
}

.active-company {
  background: #f0f9ff;
  color: #1e40af;
}

.check-icon {
  margin-left: auto;
  color: #3b82f6;
}

/* User Menu */
.user-menu {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  color: white;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: 600;
  font-size: 0.85rem;
  line-height: 1.2;
}

.user-role {
  font-size: 0.7rem;
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

/* Mobile Overlay */
.mobile-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 24px;
  background: #f8fbff;
  overflow-y: auto;
}

/* Utility Classes */
.desktop-only {
  display: flex;
}

.desktop-logo {
  display: block;
}

/* Responsive Design */

/* Large Desktop (1200px+) */
@media (min-width: 1200px) {
  .top-nav {
    padding: 12px 32px;
  }
  
  .nav-menu {
    gap: 12px;
  }
  
  .nav-item {
    padding: 12px 20px;
  }
  
  .main-content {
    padding: 32px;
  }
}

/* Medium Desktop/Laptop (992px - 1199px) */
@media (max-width: 1199px) {
  .nav-menu {
    gap: 6px;
  }
  
  .nav-item {
    padding: 10px 14px;
    font-size: 0.9rem;
  }
  
  .company-name {
    font-size: 0.85rem;
  }
}

/* Tablet (768px - 991px) */
@media (max-width: 991px) {
  .mobile-menu-button {
    display: flex;
  }
  
  .nav-menu {
    position: fixed;
    top: 72px;
    left: 0;
    width: 100vw;
    height: calc(100vh - 72px);
    background: white;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    padding: 20px;
    gap: 0;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .nav-menu.mobile-open {
    transform: translateX(0);
  }
  
  .mobile-overlay {
    display: block;
  }
  
  .nav-item {
    color: #374151;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 4px;
    border-bottom: 1px solid #e5e7eb;
    justify-content: flex-start;
  }
  
  .nav-item:hover, .nav-item.active {
    background: #f3f4f6;
    color: #1e3c72;
    transform: none;
  }
  
  .nav-dropdown {
    width: 100%;
  }
  
  .dropdown-menu {
    position: static;
    box-shadow: none;
    background: #f9fafb;
    margin: 8px 0 16px 20px;
    border-left: 3px solid #e5e7eb;
  }
  
  .company-name {
    display: none;
  }
  
  .user-details {
    display: none;
  }
  
  .dropdown-arrow {
    margin-left: auto;
  }
}

/* Mobile (576px - 767px) */
@media (max-width: 767px) {
  .top-nav {
    padding: 10px 16px;
  }
  
  .app-title {
    font-size: 1.2rem;
  }
  
  .logo {
    width: 36px;
    height: 36px;
  }
  
  .company-dropdown {
    min-width: auto;
    padding: 8px;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }
  
  .main-content {
    padding: 16px;
  }
}

/* Small Mobile (up to 575px) */
@media (max-width: 575px) {
  .top-nav {
    padding: 8px 12px;
  }
  
  .app-title {
    display: none;
  }
  
  .desktop-logo {
    display: none;
  }
  
  .company-dropdown {
    padding: 6px;
  }
  
  .company-icon {
    font-size: 1.2rem;
  }
  
  .user-avatar {
    width: 30px;
    height: 30px;
    font-size: 0.75rem;
  }
  
  .nav-right {
    gap: 8px;
  }
  
  .main-content {
    padding: 12px;
  }
}

/* Very Small Mobile (up to 400px) */
@media (max-width: 400px) {
  .nav-right {
    gap: 6px;
  }
  
  .logo-section {
    gap: 6px;
  }
  
  .mobile-menu-button {
    width: 26px;
    height: 26px;
  }
  
  .hamburger-line {
    width: 20px;
    height: 2px;
  }
}

/* Fix dropdown positioning on mobile */
@media (max-width: 991px) {
  .company-dropdown .dropdown-menu,
  .user-dropdown {
    position: fixed;
    top: 70px;
    right: 16px;
    left: auto;
    width: calc(100vw - 32px);
    max-width: 300px;
    background: white;
    z-index: 1002; /* Above the mobile overlay */
  }

  .company-dropdown,
  .user-info {
    position: relative;
    z-index: 1002; /* Above the mobile overlay */
  }

  .mobile-overlay {
    z-index: 999; /* Below the dropdowns */
  }

  .nav-menu {
    z-index: 1001; /* Above overlay but below dropdowns */
  }
}
</style>