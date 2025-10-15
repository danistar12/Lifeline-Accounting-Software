import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/styles/ui-base.css'
import axios from 'axios'

// Ensure axios sends cookies (and CSRF cookies) for session-based auth with Django.
axios.defaults.withCredentials = true;

createApp(App).use(store).use(router).mount('#app')
