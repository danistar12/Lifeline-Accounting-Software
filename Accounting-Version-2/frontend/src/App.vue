<script setup>
// No imports needed at setup level - router is already provided globally
</script>

<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="/logo.png" alt="Lifeline Logo" class="logo" />
        <h1 class="sidebar-title">Lifeline Accounting</h1>
      </div>
      <nav>
        <div class="nav-section">
          <div class="nav-label">Overview</div>
          <ul>
            <li :class="{ active: $route.name === 'dashboard' }">
              <router-link to="/">
                <span class="icon">🏠</span>
                <span>Dashboard</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <div class="nav-label">Customers & Vendors</div>
          <ul>
            <li :class="{ active: $route.name === 'customers' }">
              <router-link to="/customers">
                <span class="icon">👥</span>
                <span>Customers</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'vendors' }">
              <router-link to="/vendors">
                <span class="icon">🚚</span>
                <span>Vendors</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <div class="nav-label">Accounts Receivable</div>
          <ul>
            <li :class="{ active: $route.name === 'invoices' }">
              <router-link to="/invoices">
                <span class="icon">📧</span>
                <span>Invoices</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'payments-ar' }">
              <router-link to="/payments-ar">
                <span class="icon">💲</span>
                <span>Received Payments</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <div class="nav-label">Accounts Payable</div>
          <ul>
            <li :class="{ active: $route.name === 'bills' }">
              <router-link to="/bills">
                <span class="icon">📝</span>
                <span>Bills</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'payments-ap' }">
              <router-link to="/payments-ap">
                <span class="icon">💸</span>
                <span>Made Payments</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <div class="nav-label">Financial Management</div>
          <ul>
            <li :class="{ active: $route.name === 'banking' }">
              <router-link to="/banking">
                <span class="icon">🏦</span>
                <span>Banking</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'inventory' }">
              <router-link to="/inventory">
                <span class="icon">📦</span>
                <span>Inventory</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'payroll' }">
              <router-link to="/payroll">
                <span class="icon">💼</span>
                <span>Payroll</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'projects' }">
              <router-link to="/projects">
                <span class="icon">📋</span>
                <span>Projects</span>
              </router-link>
            </li>
          </ul>
        </div>
        
        <div class="nav-section">
          <div class="nav-label">Additional Services</div>
          <ul>
            <li :class="{ active: $route.name === 'reports' }">
              <router-link to="/reports">
                <span class="icon">📊</span>
                <span>Reports</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'documents' }">
              <router-link to="/documents">
                <span class="icon">📄</span>
                <span>Documents</span>
              </router-link>
            </li>
            <li :class="{ active: $route.name === 'subscriptions' }">
              <router-link to="/subscriptions">
                <span class="icon">🔄</span>
                <span>Subscriptions</span>
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      navItems: [
        { name: 'dashboard', label: 'Dashboard', path: '/', emoji: '🏠' },
        
        // Core data management
        { name: 'customers', label: 'Customers', path: '/customers', emoji: '�' },
        { name: 'vendors', label: 'Vendors', path: '/vendors', emoji: '🚚' },
        
        // Accounts receivable
        { name: 'invoices', label: 'Invoices', path: '/invoices', emoji: '📧' },
        { name: 'payments-ar', label: 'Received Payments', path: '/payments-ar', emoji: '�' },
        
        // Accounts payable
        { name: 'bills', label: 'Bills', path: '/bills', emoji: '�' },
        { name: 'payments-ap', label: 'Made Payments', path: '/payments-ap', emoji: '💸' },
        
        // Financial management
        { name: 'banking', label: 'Banking', path: '/banking', emoji: '🏦' },
        { name: 'inventory', label: 'Inventory', path: '/inventory', emoji: '📦' },
        { name: 'payroll', label: 'Payroll', path: '/payroll', emoji: '�' },
        
        // Support functions
        { name: 'reports', label: 'Reports', path: '/reports', emoji: '📊' },
        { name: 'documents', label: 'Documents', path: '/documents', emoji: '📄' },
        { name: 'subscriptions', label: 'Subscriptions', path: '/subscriptions', emoji: '🔄' },
      ]
    }
  }
}
</script>

<style>
.app-container {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  margin: 0;
  background: linear-gradient(120deg, #e3eafc 0%, #f8fbff 100%);
  box-sizing: border-box;
}
.sidebar {
  width: 260px;
  background: linear-gradient(120deg, #1e3c72 0%, #2a5298 100%);
  color: #fff;
  box-shadow: 2px 0 12px rgba(30,60,114,0.08);
  display: flex;
  flex-direction: column;
  padding: 32px 0 24px 0;
}
.sidebar-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 0 24px 32px 24px;
}
.sidebar-title {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 1px;
  white-space: nowrap;
  margin-top: 8px;
  color: #fff;
}
.logo {
  width: 180px;
  height: 80px;
  border-radius: 30px;
  object-fit: contain;
  box-shadow: none;
  background: none;
  margin-bottom: 8px;
}
nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
nav li {
  margin-bottom: 12px;
  border-radius: 8px;
  transition: background 0.2s, box-shadow 0.2s;
}
nav li.active, nav li:hover {
  background: rgba(255,255,255,0.12);
  box-shadow: 0 2px 8px rgba(30,60,114,0.12);
}
nav a {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #fff;
  text-decoration: none;
  font-size: 1.12rem;
  padding: 14px 28px;
  border-radius: 8px;
  width: 100%;
  font-weight: 500;
  letter-spacing: 0.5px;
}
.icon {
  width: 28px;
  text-align: center;
  font-size: 1.5rem;
}
.nav-section {
  margin-bottom: 24px;
}
.nav-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  padding: 0 28px;
  margin-bottom: 8px;
}
.main-content {
  flex: 1;
  padding: 40px 32px;
  background: #f8fbff;
  min-height: 100vh;
  border-radius: 0 16px 16px 0;
  box-shadow: 0 4px 24px rgba(30,60,114,0.04);
}
@media (max-width: 900px) {
  .sidebar {
    width: 64px;
    padding: 12px 0;
  }
  .sidebar-header h1, .sidebar-header .logo {
    display: none;
  }
  nav a span:not(.icon) {
    display: none;
  }
  .main-content {
    padding: 12px;
    border-radius: 0;
  }
}
</style>
