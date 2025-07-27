import axios from 'axios';
import authService from './authService';

class DashboardService {
  getActiveCompanyId() {
    return localStorage.getItem('activeCompanyId') || 
      (authService.getCurrentUser()?.companies?.[0]?.company_id);
  }

  async getHeaders() {
    const headers = authService.getAuthHeaders();
    const companyId = this.getActiveCompanyId();
    if (!companyId) {
      throw new Error('No active company selected');
    }
    return {
      ...headers,
      'X-Company-ID': companyId
    };
  }

  async getOverview(period = 'month') {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/overview', { 
      headers,
      params: { period }
    });
    return response.data;
  }

  async getRevenueData(startDate, endDate) {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/revenue', { 
      headers,
      params: { startDate, endDate }
    });
    return response.data;
  }

  async getExpensesData(startDate, endDate, categories = []) {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/expenses', { 
      headers,
      params: { startDate, endDate, categories }
    });
    return response.data;
  }

  async getRecentTransactions(limit = 10, type = 'all') {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/transactions', { 
      headers,
      params: { limit, type }
    });
    return response.data;
  }

  async getCashFlow(period = 'month', projection = true) {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/cash-flow', { 
      headers,
      params: { period, projection }
    });
    return response.data;
  }

  async getAccountBalances(accountTypes = []) {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/account-balances', { 
      headers,
      params: { accountTypes }
    });
    return response.data;
  }

  async getKeyMetrics(period = 'month') {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/key-metrics', {
      headers,
      params: { period }
    });
    return response.data;
  }

  async getInvoiceStatus() {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/invoice-status', {
      headers
    });
    return response.data;
  }

  async getBudgetComparison(year, month) {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/budget-comparison', {
      headers,
      params: { year, month }
    });
    return response.data;
  }

  async getAccountingHealth() {
    const headers = await this.getHeaders();
    const response = await axios.get('/api/dashboard/accounting-health', {
      headers
    });
    return response.data;
  }
}

export default new DashboardService();
