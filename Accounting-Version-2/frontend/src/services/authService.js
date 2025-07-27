import apiClient from './api'

const authService = {
  // Login user
  async login(credentials) {
    const response = await apiClient.post('/auth/login/', credentials)
    
    if (response.data.access) {
      // Store tokens in localStorage
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      
      // Set active company if user has companies
      if (response.data.user.companies && response.data.user.companies.length > 0) {
        // Set the first company as active by default
        const activeCompany = response.data.user.companies[0]
        response.data.user.activeCompany = activeCompany
        localStorage.setItem('activeCompanyId', activeCompany.company_id)
      }
      
      localStorage.setItem('user', JSON.stringify(response.data.user))
      
      // Set the default authorization header
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    }
    
    return response
  },

  // Logout user
  async logout() {
    const refreshToken = localStorage.getItem('refresh_token')
    
    try {
      await apiClient.post('/auth/logout/', {
        refresh: refreshToken
      })
    } catch (error) {
      console.warn('Logout API call failed:', error)
    } finally {
      // Clear local storage regardless of API call success
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      delete apiClient.defaults.headers.common['Authorization']
    }
  },

  // Register new user
  async register(userData) {
    const response = await apiClient.post('/auth/register/', userData)
    
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    }
    
    return response
  },

  // Refresh token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token')
    
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }
    
    try {
      const response = await apiClient.post('/auth/refresh/', {
        refresh: refreshToken
      })
      
      localStorage.setItem('access_token', response.data.access)
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      
      return response
    } catch (error) {
      // If refresh fails, logout the user
      this.logout()
      throw error
    }
  },

  // Get current user profile
  async getUserProfile() {
    return await apiClient.get('/auth/profile/')
  },

  // Update user profile
  async updateProfile(profileData) {
    return await apiClient.put('/auth/profile/', profileData)
  },

  // Change password
  async changePassword(passwordData) {
    return await apiClient.post('/auth/change-password/', passwordData)
  },

  // Upload avatar
  async uploadAvatar(file) {
    const formData = new FormData()
    formData.append('avatar', file)
    
    return await apiClient.post('/auth/upload-avatar/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // Check if user is authenticated
  isAuthenticated() {
    const token = localStorage.getItem('access_token')
    return !!token
  },

  // Get current user from localStorage
  getCurrentUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  // Initialize auth state (call on app startup)
  initializeAuth() {
    const token = localStorage.getItem('access_token')
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    
    // Initialize company ID header
    const companyId = localStorage.getItem('activeCompanyId')
    if (companyId) {
      apiClient.defaults.headers.common['X-Company-ID'] = companyId
    } else {
      // If no active company is set but user has companies, set the first one as active
      const user = this.getCurrentUser()
      if (user && user.companies && user.companies.length > 0) {
        const firstCompanyId = user.companies[0].company_id
        this.setActiveCompany(firstCompanyId)
      }
    }
  },
  
  // Set active company
  setActiveCompany(companyId) {
    const user = this.getCurrentUser();
    if (!user || !user.companies) return false;
    
    const company = user.companies.find(c => c.company_id === companyId);
    if (!company) return false;
    
    // Update user object with new active company
    user.activeCompany = company;
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('activeCompanyId', companyId);
    
    // Update header for future requests
    apiClient.defaults.headers.common['X-Company-ID'] = companyId;
    
    return true;
  }
}

export default authService
