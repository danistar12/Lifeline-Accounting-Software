<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="/logo.png" alt="Lifeline Logo" class="logo" />
        <h1 class="sidebar-title">Lifeline Accounting</h1>
      </div>
      <nav>
        <ul>
          <li v-for="item in navItems" :key="item.name" :class="{ active: $route.name === item.name }">
            <router-link :to="item.path">
              <span class="icon">{{ item.emoji }}</span>
              <span>{{ item.label }}</span>
            </router-link>
          </li>
        </ul>
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
        { name: 'accounts', label: 'Accounts', path: '/accounts', emoji: '👤' },
        { name: 'banking', label: 'Banking', path: '/banking', emoji: '🏦' },
        { name: 'core', label: 'Core', path: '/core', emoji: '⚙️' },
        { name: 'documents', label: 'Documents', path: '/documents', emoji: '📄' },
        { name: 'importer', label: 'Importer', path: '/importer', emoji: '📥' },
        { name: 'payments-ap', label: 'Payments AP', path: '/payments-ap', emoji: '💸' },
        { name: 'payments-ar', label: 'Payments AR', path: '/payments-ar', emoji: '🧾' },
        { name: 'payroll', label: 'Payroll', path: '/payroll', emoji: '👥' },
        { name: 'reports', label: 'Reports', path: '/reports', emoji: '📊' },
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
