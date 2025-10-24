import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/styles/ui-base.css'
import axios from 'axios'

// Ensure axios sends cookies (and CSRF cookies) for session-based auth with Django.
axios.defaults.withCredentials = true;

// Inactivity logout configuration
const INACTIVITY_TIMEOUT = 30 * 60 * 1000; // 30 minutes in milliseconds
let inactivityTimer;

function resetInactivityTimer() {
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(async () => {
    // Log out user on inactivity
    try {
      await store.dispatch('logout');
    } catch (error) {
      console.error('Error during inactivity logout:', error);
    }
    router.push('/login');
  }, INACTIVITY_TIMEOUT);
}

function setupInactivityDetection() {
  // Reset timer on user activity
  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
  events.forEach(event => {
    document.addEventListener(event, resetInactivityTimer, true);
  });
  
  // Start the timer initially
  resetInactivityTimer();
}

// Only setup inactivity detection if user is logged in
store.watch(
  (state) => state.user,
  (newUser) => {
    if (newUser) {
      setupInactivityDetection();
    } else {
      clearTimeout(inactivityTimer);
    }
  },
  { immediate: true }
);

createApp(App).use(store).use(router).mount('#app')
