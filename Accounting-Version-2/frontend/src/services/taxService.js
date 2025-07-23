import apiClient from './api';

class TaxService {
  // Tax Rate endpoints
  async getTaxRates() {
    const response = await apiClient.get('/tax/tax-rates/');
    return response.data;
  }

  async getTaxRate(id) {
    const response = await apiClient.get(`/tax/tax-rates/${id}/`);
    return response.data;
  }

  async createTaxRate(taxRateData) {
    const response = await apiClient.post('/tax/tax-rates/', taxRateData);
    return response.data;
  }

  async updateTaxRate(id, taxRateData) {
    const response = await apiClient.put(`/tax/tax-rates/${id}/`, taxRateData);
    return response.data;
  }

  async deleteTaxRate(id) {
    const response = await apiClient.delete(`/tax/tax-rates/${id}/`);
    return response.data;
  }

  // Tax Transaction endpoints
  async getTaxTransactions() {
    const response = await apiClient.get('/tax/tax-transactions/');
    return response.data;
  }

  async getTaxTransaction(id) {
    const response = await apiClient.get(`/tax/tax-transactions/${id}/`);
    return response.data;
  }

  async createTaxTransaction(taxTransactionData) {
    const response = await apiClient.post('/tax/tax-transactions/', taxTransactionData);
    return response.data;
  }

  async updateTaxTransaction(id, taxTransactionData) {
    const response = await apiClient.put(`/tax/tax-transactions/${id}/`, taxTransactionData);
    return response.data;
  }

  async deleteTaxTransaction(id) {
    const response = await apiClient.delete(`/tax/tax-transactions/${id}/`);
    return response.data;
  }
}

export default new TaxService();
