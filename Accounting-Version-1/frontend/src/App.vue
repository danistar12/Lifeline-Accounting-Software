<template>
  <div id="app">
    <header class="app-header">
      <div class="logo">
        <router-link to="/">Lifeline Accounting</router-link>
      </div>
      <button v-if="isLoggedIn" class="mobile-toggle" @click="toggleMobileNav" :class="{ active: mobileNavOpen }">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <nav v-if="isLoggedIn" class="main-nav" :class="{ 'mobile-open': mobileNavOpen }">
        <router-link to="/" class="nav-item dashboard-nav" @click="closeMobileMenu">
          <div class="nav-icon">📊</div>
          <span class="nav-label">Dashboard</span>
          <div class="nav-highlight"></div>
        </router-link>

        <div class="nav-dropdown" @click="toggleDropdown($event)">
          <div class="nav-item dropdown-toggle">
            <div class="nav-icon">👥</div>
            <span class="nav-label">Accounts</span>
            <div class="nav-highlight"></div>
          </div>
          <div class="dropdown-menu">
            <router-link to="/accounts/companies" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🏢</i>
              <span>Companies</span>
            </router-link>
            <router-link to="/accounts/user-roles" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🔑</i>
              <span>User Roles</span>
            </router-link>
          </div>
        </div>

        <div class="nav-dropdown" @click="toggleDropdown($event)">
          <div class="nav-item dropdown-toggle">
            <div class="nav-icon">⚙️</div>
            <span class="nav-label">Core</span>
            <div class="nav-highlight"></div>
          </div>
          <div class="dropdown-menu">
            <router-link to="/core/bills" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🧾</i>
              <span>Bills</span>
            </router-link>
            <router-link to="/core/chart-of-accounts" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">📋</i>
              <span>Chart of Accounts</span>
            </router-link>
            <router-link to="/core/customers" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">👤</i>
              <span>Customers</span>
            </router-link>
            <router-link to="/core/general-ledger" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">📖</i>
              <span>General Ledger</span>
            </router-link>
            <router-link to="/core/invoices" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">📄</i>
              <span>Invoices</span>
            </router-link>
            <router-link to="/core/vendors" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🏪</i>
              <span>Vendors</span>
            </router-link>
          </div>
        </div>

        <div class="nav-dropdown" @click="toggleDropdown($event)">
          <div class="nav-item dropdown-toggle">
            <div class="nav-icon">💰</div>
            <span class="nav-label">Payroll</span>
            <div class="nav-highlight"></div>
          </div>
          <div class="dropdown-menu">
            <router-link to="/payroll/employees" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">👷</i>
              <span>Employees</span>
            </router-link>
            <router-link to="/payroll/payrolls" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">💵</i>
              <span>Payrolls</span>
            </router-link>
            <router-link to="/payroll/paystubs" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🧾</i>
              <span>Paystubs</span>
            </router-link>
            <router-link to="/payroll/taxes" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🏛️</i>
              <span>Taxes</span>
            </router-link>
            <router-link to="/payroll/deductions" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">➖</i>
              <span>Deductions</span>
            </router-link>
            <router-link to="/payroll/benefits" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🎁</i>
              <span>Benefits</span>
            </router-link>
          </div>
        </div>

        <router-link to="/subscriptions" class="nav-item" @click="closeMobileMenu">
          <div class="nav-icon">📦</div>
          <span class="nav-label">Subscriptions</span>
          <div class="nav-highlight"></div>
        </router-link>

        <div class="nav-dropdown" @click="toggleDropdown($event)">
          <div class="nav-item dropdown-toggle">
            <div class="nav-icon">🏦</div>
            <span class="nav-label">Banking</span>
            <div class="nav-highlight"></div>
          </div>
          <div class="dropdown-menu">
            <router-link to="/banking/accounts" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🏛️</i>
              <span>Bank Accounts</span>
            </router-link>
            <router-link to="/banking/statement-lines" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">📜</i>
              <span>Statement Lines</span>
            </router-link>
            <router-link to="/banking/reconciliations" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">⚖️</i>
              <span>Reconciliations</span>
            </router-link>
          </div>
        </div>

        <div class="nav-dropdown" @click="toggleDropdown($event)">
          <div class="nav-item dropdown-toggle">
            <div class="nav-icon">📊</div>
            <span class="nav-label">Reports</span>
            <div class="nav-highlight"></div>
          </div>
          <div class="dropdown-menu">
            <router-link to="/reports/balance-sheet" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">⚖️</i>
              <span>Balance Sheet</span>
            </router-link>
            <router-link to="/reports/income-statement" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">💹</i>
              <span>Income Statement</span>
            </router-link>
            <router-link to="/reports/cash-flow" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">💰</i>
              <span>Cash Flow</span>
            </router-link>
          </div>
        </div>
        
        <!-- Admin Section (Only visible for admin users) -->
        <div class="nav-dropdown" v-if="isAdmin" @click="toggleDropdown($event)">
          <div class="nav-item dropdown-toggle">
            <div class="nav-icon">🔐</div>
            <span class="nav-label">Admin</span>
            <div class="nav-highlight"></div>
          </div>
          <div class="dropdown-menu">
            <router-link to="/audit-logs" class="dropdown-link" @click="closeMobileMenu">
              <i class="link-icon">🔍</i>
              <span>Audit Logs</span>
            </router-link>
          </div>
        </div>
      </nav>
      <div class="user-actions">
        <button v-if="!isLoggedIn" @click="login">Login</button>
        
        <!-- User Profile Dropdown -->
        <div v-if="isLoggedIn" class="user-profile-dropdown" @click="toggleDropdown($event)">
          <div class="user-profile-toggle dropdown-toggle">
            <div class="user-avatar">
              <img v-if="user?.profile_photo || user?.user?.profile_photo" 
                   :src="user?.profile_photo || user?.user?.profile_photo" 
                   alt="" 
                   class="avatar-image high-res"
                   @error="$event.target.style.display='none'; $event.target.nextElementSibling.style.display='flex'" />
              <span class="avatar-initials" :style="(user?.profile_photo || user?.user?.profile_photo) ? 'display: none' : ''">{{ userInitials }}</span>
            </div>
            <span class="user-name">{{ userDisplayName }}</span>
          </div>
          <div class="dropdown-menu user-dropdown-menu">
            <div class="user-info-section">
              <div class="user-details">
                <strong>{{ user?.user?.username || user?.username }}</strong>
                <small v-if="user?.user?.email || user?.email">{{ user?.user?.email || user?.email }}</small>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" class="dropdown-item" @click="closeMobileMenu">
              <i class="icon-user"></i>
              My Profile
            </router-link>
            <router-link to="/settings" class="dropdown-item" @click="closeMobileMenu">
              <i class="icon-settings"></i>
              Settings
            </router-link>
            <router-link to="/audit-logs" class="dropdown-item" v-if="isAdmin" @click="closeMobileMenu">
              <i class="icon-list"></i>
              Audit Logs
            </router-link>
            <div class="dropdown-divider"></div>
            <a @click="handleLogout" class="dropdown-item logout-item">
              <i class="icon-logout"></i>
              Logout
            </a>
          </div>
        </div>
      </div>
    </header>
    <main class="app-content">
      <router-view/>
    </main>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';

export default {
  name: 'App',
  components: {
  },
  data() {
    return {
      mobileNavOpen: false,
    };
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
    ...mapState(['user']),
    isAdmin() {
      if (!this.user) return false;
      const userData = this.user.user || this.user;
      return userData.is_staff || userData.is_superuser || (userData.role && userData.role.toLowerCase().includes('admin'));
    },
    userDisplayName() {
      if (!this.user) return '';
      
      const userData = this.user.user || this.user;
      
      if (userData.first_name && userData.last_name) {
        return `${userData.first_name} ${userData.last_name}`;
      } else if (userData.first_name) {
        return userData.first_name;
      } else {
        return userData.username || 'User';
      }
    },
    userInitials() {
      if (!this.user) return 'U';
      
      const userData = this.user.user || this.user;
      
      if (userData.first_name && userData.last_name) {
        return `${userData.first_name.charAt(0)}${userData.last_name.charAt(0)}`.toUpperCase();
      } else if (userData.first_name) {
        return userData.first_name.charAt(0).toUpperCase();
      } else if (userData.username) {
        return userData.username.charAt(0).toUpperCase();
      } else {
        return 'U';
      }
    }
  },
  methods: {
    ...mapActions(['logout', 'me']),
    login() {
      this.$router.push({ name: 'Login' });
    },
    handleLogout() {
      this.logout().then(() => {
        this.$router.push({ name: 'Login' });
      });
    },
    toggleMobileNav() {
      this.mobileNavOpen = !this.mobileNavOpen;
    },
    closeMobileMenu() {
      this.mobileNavOpen = false;
    },
    toggleDropdown(event) {
      // Handle different types of dropdown toggles
      const navDropdown = event.currentTarget.classList.contains('nav-dropdown');
      const userProfileDropdown = event.currentTarget.classList.contains('user-profile-dropdown');
      
      if (navDropdown || userProfileDropdown) {
        const dropdown = event.currentTarget;
        
        // Close all other dropdowns
        document.querySelectorAll('.nav-dropdown, .user-profile-dropdown').forEach(el => {
          if (el !== dropdown && el.classList.contains('active')) {
            el.classList.remove('active');
          }
        });
        
        // Toggle the current dropdown
        dropdown.classList.toggle('active');
        event.stopPropagation(); // Prevent navigation
      }
    }
  },
  created() {
    // Try to load user data on app start
    this.me().catch(() => {
      // Not logged in, or session expired - silent fail
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
      document.querySelectorAll('.nav-dropdown.active, .user-profile-dropdown.active').forEach(el => {
        el.classList.remove('active');
      });
    });
  }
};
</script>

<style>
/* General App Styling */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f4f7f6;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app-header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.mobile-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.mobile-toggle span {
  width: 25px;
  height: 3px;
  background-color: #2c3e50;
  margin: 3px 0;
  transition: 0.3s;
  transform-origin: center;
}

.mobile-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.mobile-toggle.active span:nth-child(2) {
  opacity: 0;
}

.mobile-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
}

.logo a {
  color: #007bff;
  text-decoration: none;
}

.main-nav {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

/* Navigation Items */
.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  overflow: hidden;
}

.nav-item:hover {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.nav-item:hover .nav-icon {
  transform: scale(1.2) rotate(5deg);
}

.nav-item.router-link-exact-active {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.nav-item.router-link-exact-active .nav-highlight {
  opacity: 1;
}

.nav-icon {
  font-size: 1.2rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.nav-label {
  font-size: 0.9rem;
  white-space: nowrap;
}

.nav-highlight {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 80%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #007bff, transparent);
  opacity: 0;
  transition: all 0.3s ease;
}

.nav-item:hover .nav-highlight {
  opacity: 0.7;
  transform: translateX(-50%) scaleX(1);
}

/* Dropdown styling */
.nav-dropdown {
  position: relative;
}

.nav-dropdown.active .nav-item {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1565c0;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  min-width: 220px;
  padding: 0.75rem 0;
  display: none;
  z-index: 1000;
  border: 1px solid #e9ecef;
  overflow: hidden;
}

.nav-dropdown.active .dropdown-menu {
  display: block;
  animation: dropdownSlide 0.3s ease-out;
}

@keyframes dropdownSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  position: relative;
}

.dropdown-link:hover {
  background: linear-gradient(135deg, #f8f9fa, #e3f2fd);
  color: #007bff;
  transform: translateX(4px);
}

.dropdown-link:hover .link-icon {
  transform: scale(1.2);
}

.link-icon {
  font-size: 1rem;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
}

/* Dashboard specific styling */
.dashboard-nav .nav-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
  border-radius: 6px;
  color: white;
  width: 28px;
  height: 28px;
}

/* User Profile Dropdown */
.user-profile-dropdown {
  position: relative;
  cursor: pointer;
}

.user-profile-dropdown .dropdown-menu {
  display: none;
}

.user-profile-dropdown.active .dropdown-menu {
  display: block;
}

.user-profile-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 25px;
  transition: background-color 0.2s;
}

.user-profile-toggle:hover {
  background-color: #f8f9fa;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.85rem;
  overflow: hidden;
}

/* Avatar Styles */
.avatar-image {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #e3f2fd;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  image-rendering: auto;
  image-rendering: crisp-edges;
  image-rendering: high-quality;
}
.avatar-image.high-res {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  background: #e3f2fd;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  image-rendering: auto;
  image-rendering: crisp-edges;
  image-rendering: high-quality;
}
.avatar-initials {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  color: #1565c0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.user-name {
  font-weight: 500;
  color: #2c3e50;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-dropdown-menu {
  right: 0;
  left: auto;
  min-width: 220px;
  padding: 0;
}

.user-info-section {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

.user-details strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.user-details small {
  color: #6c757d;
  font-size: 0.8rem;
}

.dropdown-divider {
  height: 1px;
  background-color: #e9ecef;
  margin: 0.5rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #2c3e50;
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #007bff;
}

.dropdown-item i {
  width: 16px;
  text-align: center;
}

.logout-item {
  color: #dc3545;
  cursor: pointer;
}

.logout-item:hover {
  background-color: #fff5f5;
  color: #c82333;
}

/* Icon classes for dropdown items */
.icon-user::before { content: '👤'; }
.icon-settings::before { content: '⚙️'; }
.icon-logout::before { content: '🚪'; }

.user-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-actions button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.user-actions button:hover {
  background-color: #0056b3;
}

.app-content {
  flex: 1;
  padding: 2rem;
}

/* Mobile Responsive Styles */
@media (max-width: 768px) {
  .app-header {
    padding: 0.5rem 1rem;
  }
  
  .mobile-toggle {
    display: flex;
  }
  
  .main-nav {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: #ffffff;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    flex-direction: column;
    gap: 0;
    display: none;
    z-index: 1000;
    padding: 1rem 0;
  }
  
  .main-nav.mobile-open {
    display: flex;
  }
  
  .nav-item {
    width: 100%;
    padding: 1rem 1.5rem;
    border-radius: 0;
    justify-content: flex-start;
  }
  
  .nav-item:hover {
    background: linear-gradient(135deg, #f8f9fa, #e3f2fd);
    transform: none;
    box-shadow: none;
  }
  
  .nav-dropdown {
    width: 100%;
  }
  
  .dropdown-menu {
    position: static;
    box-shadow: none;
    border: none;
    background-color: #f8f9fa;
    border-left: 3px solid #007bff;
    margin: 0.5rem 0;
    display: none;
    border-radius: 0;
  }
  
  .nav-dropdown.active .dropdown-menu {
    display: block;
  }
  
  .dropdown-link {
    padding: 0.75rem 2rem;
  }
  
  .dropdown-link:hover {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    transform: none;
  }
  
  .user-actions {
    order: -1;
    margin-right: auto;
  }
  
  .user-profile-dropdown .user-dropdown-menu {
    right: auto;
    left: 0;
  }
  
  .user-name {
    display: none;
  }
  
  .app-content {
    padding: 1rem;
  }
}
</style>
