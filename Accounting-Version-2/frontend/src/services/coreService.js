import apiClient from './api';

class CoreService {
  // Company endpoints
  async getCompanies() {
    const response = await apiClient.get('/core/companies/');
    return response.data;
  }

  async getCompany(id) {
    const response = await apiClient.get(`/core/companies/${id}/`);
    return response.data;
  }

  async createCompany(companyData) {
    const response = await apiClient.post('/core/companies/', companyData);
    return response.data;
  }

  async updateCompany(id, companyData) {
    const response = await apiClient.put(`/core/companies/${id}/`, companyData);
    return response.data;
  }

  async deleteCompany(id) {
    const response = await apiClient.delete(`/core/companies/${id}/`);
    return response.data;
  }

  // Chart of Accounts endpoints
  async getChartOfAccounts() {
    const response = await apiClient.get('/core/chart-of-accounts/');
    return response.data;
  }

  async getAccount(id) {
    const response = await apiClient.get(`/core/chart-of-accounts/${id}/`);
    return response.data;
  }

  async createAccount(accountData) {
    const response = await apiClient.post('/core/chart-of-accounts/', accountData);
    return response.data;
  }

  async updateAccount(id, accountData) {
    const response = await apiClient.put(`/core/chart-of-accounts/${id}/`, accountData);
    return response.data;
  }

  async deleteAccount(id) {
    const response = await apiClient.delete(`/core/chart-of-accounts/${id}/`);
    return response.data;
  }

  // General Ledger endpoints
  async getGeneralLedgerEntries() {
    const response = await apiClient.get('/core/general-ledger/');
    return response.data;
  }

  async getGeneralLedgerEntry(id) {
    const response = await apiClient.get(`/core/general-ledger/${id}/`);
    return response.data;
  }

  async createGeneralLedgerEntry(entryData) {
    const response = await apiClient.post('/core/general-ledger/', entryData);
    return response.data;
  }

  async updateGeneralLedgerEntry(id, entryData) {
    const response = await apiClient.put(`/core/general-ledger/${id}/`, entryData);
    return response.data;
  }

  async deleteGeneralLedgerEntry(id) {
    const response = await apiClient.delete(`/core/general-ledger/${id}/`);
    return response.data;
  }
}

export default new CoreService();
