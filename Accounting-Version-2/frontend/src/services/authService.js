import apiClient from './api'

const authService = {
  // Login user
  async login(credentials) {
    const response = await apiClient.post('/auth/login/', credentials)
    
    if (response.data.access) {
      // Store tokens in localStorage
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
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
  }
}

export default authService
