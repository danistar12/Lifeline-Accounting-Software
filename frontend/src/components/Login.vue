<template>
  <div class="login-view">
    <div class="login-panel">
      <div class="login-header">
        <h2>Welcome Back</h2>
        <p>Please enter your credentials to log in.</p>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required placeholder="Enter your username">
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required placeholder="Enter your password">
        </div>
        <div class="form-group remember-me">
          <input type="checkbox" id="remember_me" v-model="rememberMe">
          <label for="remember_me">Remember me for 30 days</label>
        </div>
        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="loading">Logging in...</span>
          <span v-else>Login</span>
        </button>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
    };
  },
  computed: {
    ...mapState(['loading', 'error', 'user']),
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      try {
        const userData = await this.login({ 
          username: this.username, 
          password: this.password,
          remember_me: this.rememberMe
        });
        
        if (userData) {
          // Navigate to dashboard without page reload
          this.$router.push('/').catch(() => {});
        }
      } catch (error) {
        console.error('Login failed:', error);
      }
    },
  },
  // Redirect to dashboard if already logged in
  created() {
    if (this.user) {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.login-view {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  height: 100vh;
  background-color: #f4f7f6;
  padding-top: 15vh;
}

.login-panel {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:disabled {
  background-color: #87ceeb;
  cursor: not-allowed;
}

.login-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.remember-me {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.remember-me input[type="checkbox"] {
  margin-right: 0.5rem;
}

.remember-me label {
  margin-bottom: 0;
  cursor: pointer;
}
</style>
