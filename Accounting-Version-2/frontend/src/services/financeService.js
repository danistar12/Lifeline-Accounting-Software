import apiClient from './api';

class FinanceService {
  // Budget endpoints
  async getBudgets() {
    const response = await apiClient.get('/finance/budgets/');
    return response.data;
  }

  async getBudget(id) {
    const response = await apiClient.get(`/finance/budgets/${id}/`);
    return response.data;
  }

  async createBudget(budgetData) {
    const response = await apiClient.post('/finance/budgets/', budgetData);
    return response.data;
  }

  async updateBudget(id, budgetData) {
    const response = await apiClient.put(`/finance/budgets/${id}/`, budgetData);
    return response.data;
  }

  async deleteBudget(id) {
    const response = await apiClient.delete(`/finance/budgets/${id}/`);
    return response.data;
  }

  // Fixed Asset endpoints
  async getFixedAssets() {
    const response = await apiClient.get('/finance/fixed-assets/');
    return response.data;
  }

  async getFixedAsset(id) {
    const response = await apiClient.get(`/finance/fixed-assets/${id}/`);
    return response.data;
  }

  async createFixedAsset(assetData) {
    const response = await apiClient.post('/finance/fixed-assets/', assetData);
    return response.data;
  }

  async updateFixedAsset(id, assetData) {
    const response = await apiClient.put(`/finance/fixed-assets/${id}/`, assetData);
    return response.data;
  }

  async deleteFixedAsset(id) {
    const response = await apiClient.delete(`/finance/fixed-assets/${id}/`);
    return response.data;
  }

  // Exchange Rate endpoints
  async getExchangeRates() {
    const response = await apiClient.get('/finance/exchange-rates/');
    return response.data;
  }

  async getExchangeRate(id) {
    const response = await apiClient.get(`/finance/exchange-rates/${id}/`);
    return response.data;
  }

  async createExchangeRate(rateData) {
    const response = await apiClient.post('/finance/exchange-rates/', rateData);
    return response.data;
  }

  async updateExchangeRate(id, rateData) {
    const response = await apiClient.put(`/finance/exchange-rates/${id}/`, rateData);
    return response.data;
  }

  async deleteExchangeRate(id) {
    const response = await apiClient.delete(`/finance/exchange-rates/${id}/`);
    return response.data;
  }
}

export default new FinanceService();
