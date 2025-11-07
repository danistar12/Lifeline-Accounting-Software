import { createStore } from 'vuex'
import axios from 'axios'
import apiClient from '@/services/apiClient'
import audit from './modules/audit'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

const envBaseUrl = process.env.VUE_APP_API_BASE ? process.env.VUE_APP_API_BASE.trim() : ''
if (envBaseUrl) {
  // Normalize trailing slashes so route helpers do not end up with /api/api
  axios.defaults.baseURL = envBaseUrl.replace(/\/+$/, '')
} else {
  delete axios.defaults.baseURL
}

// Load user state from localStorage if available
const savedUser = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;

// Restore JWT token to axios headers if available
const savedToken = localStorage.getItem('access_token');
if (savedToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`;
}

export default createStore({
  state: {
    user: savedUser,
    loading: false,
    error: null,
    selectedCompany: {
      id: localStorage.getItem('selectedCompanyId') || null,
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      // Save to localStorage for persistence
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
      } else {
        localStorage.removeItem('user');
      }
    },
    setLoading(state, loading) {
      state.loading = loading;
    },
    setError(state, error) {
      state.error = error;
    },
    setUserCompanies(state, companies) {
      console.log('Setting companies in store:', companies);
      if (state.user) {
        state.user.companies = companies;
        localStorage.setItem('user', JSON.stringify(state.user));
        console.log('Updated user in store:', state.user);
      }
    },
    setSelectedCompany(state, companyId) {
      state.selectedCompany.id = companyId;
      localStorage.setItem('selectedCompanyId', companyId);
    },
    clearAuthData(state) {
      state.user = null;
      state.selectedCompany.id = null;
      localStorage.removeItem('user');
      localStorage.removeItem('selectedCompanyId');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('current_user_id');
      // Clear axios authorization header
      delete axios.defaults.headers.common['Authorization'];
      state.error = null;
    }
  },
  actions: {
    async login({ commit, dispatch }, authData) {
      commit('setLoading', true);
      commit('setError', null);
      
      try {
        // Get CSRF token
        console.log('Getting CSRF token...');
        await apiClient.get('/api/accounts/auth/csrf/');
        
        // Login with remember_me flag
        console.log('Logging in...');
        const loginData = {
          username: authData.username,
          password: authData.password,
          remember_me: authData.remember_me || false
        };
        const loginResponse = await apiClient.post('/api/accounts/auth/login/', loginData);
        
        // Store JWT tokens in localStorage
        if (loginResponse.data.access) {
          localStorage.setItem('access_token', loginResponse.data.access);
          // Set the token in axios headers immediately
          axios.defaults.headers.common['Authorization'] = `Bearer ${loginResponse.data.access}`;
        }
        if (loginResponse.data.refresh) {
          localStorage.setItem('refresh_token', loginResponse.data.refresh);
        }
        
        // Fetch user data using apiClient (which has JWT interceptor)
        console.log('Fetching user data...');
        const response = await apiClient.get('/api/accounts/auth/user/');
        console.log('User data received:', response.data);
        commit('setUser', response.data);
        
        // Load companies after successful login
        console.log('Loading companies after login...');
        await dispatch('loadCompanies');
        
        commit('setLoading', false);
        return response.data;
      } catch (error) {
        commit('setLoading', false);
        commit('setError', error.response?.data?.detail || 'Login failed');
        console.error('Login error:', error);
        throw error;
      }
    },
    
    async logout({ commit }) {
      try {
        await apiClient.post('/api/accounts/auth/logout/');
        commit('clearAuthData');
        // Clear JWT tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        // Clear axios authorization header
        delete axios.defaults.headers.common['Authorization'];
      } catch (error) {
        console.error('Logout failed:', error);
        // Still clear the auth data even if the logout request fails
        commit('clearAuthData');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        delete axios.defaults.headers.common['Authorization'];
        throw error;
      }
    },

    async me({ commit, dispatch }) {
      try {
        console.log('Loading current user...');
        const response = await apiClient.get('/api/accounts/auth/user/');
        console.log('User data received:', response.data);
        console.log('Profile photo URL:', response.data?.user?.profile_photo || response.data?.profile_photo);
        
        // Verify user identity hasn't changed
        const currentUserId = localStorage.getItem('current_user_id');
        const newUserId = response.data?.user?.id || response.data?.id;
        
        if (currentUserId && currentUserId !== String(newUserId)) {
          // User identity changed - possible admin hijacking
          console.warn('User identity changed, logging out for security');
          commit('clearAuthData');
          throw new Error('Security violation: user identity changed');
        }
        
        // Store current user ID for verification
        localStorage.setItem('current_user_id', String(newUserId));
        
        commit('setUser', response.data);
        
        // Load companies after getting user data
        await dispatch('loadCompanies');
        
        return response.data;
      } catch (error) {
        console.error('Failed to load user:', error);
        commit('clearAuthData');
        localStorage.removeItem('current_user_id');
        throw error;
      }
    },

    async loadCompanies({ commit }) {
      try {
        console.log('Loading companies...');
        const response = await apiClient.get('/api/accounts/companies/');
        console.log('Companies loaded:', response.data);
        commit('setUserCompanies', response.data);
        // If no company is currently selected, pick the first available company
        const currentSelected = localStorage.getItem('selectedCompanyId');
        if (!currentSelected && Array.isArray(response.data) && response.data.length) {
          const first = response.data[0];
          const firstId = first.CompanyID ?? first.company_id ?? null;
          if (firstId) {
            commit('setSelectedCompany', firstId);
            // also set axios default so apiClient and existing code paths pick it up
            axios.defaults.headers.common['X-Company-ID'] = firstId;
            console.log('Auto-selected company:', firstId);
          }
        }
        return response.data;
      } catch (error) {
        console.error('Failed to load companies:', error);
        console.error('Error response:', error.response?.data);
        throw error;
      }
    },

    async loadCompanyData({ state }) {
      // This action can be used to load company-specific data
      // when a company is selected
      const companyId = state.selectedCompany.id;
      if (companyId) {
        // Add any company-specific data loading here
        console.log('Loading data for company:', companyId);
      }
    }
  },
  getters: {
    isLoggedIn: state => !!state.user,
    selectedCompanyId: state => state.selectedCompany.id
  },
  modules: {
    audit
  }
})
