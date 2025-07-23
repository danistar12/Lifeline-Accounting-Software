import apiClient from './api';

class ContactsService {
  // Customer endpoints
  async getCustomers() {
    const response = await apiClient.get('/contacts/customers/');
    return response.data;
  }

  async getCustomer(id) {
    const response = await apiClient.get(`/contacts/customers/${id}/`);
    return response.data;
  }

  async createCustomer(customerData) {
    const response = await apiClient.post('/contacts/customers/', customerData);
    return response.data;
  }

  async updateCustomer(id, customerData) {
    const response = await apiClient.put(`/contacts/customers/${id}/`, customerData);
    return response.data;
  }

  async deleteCustomer(id) {
    const response = await apiClient.delete(`/contacts/customers/${id}/`);
    return response.data;
  }

  // Vendor endpoints
  async getVendors() {
    const response = await apiClient.get('/contacts/vendors/');
    return response.data;
  }

  async getVendor(id) {
    const response = await apiClient.get(`/contacts/vendors/${id}/`);
    return response.data;
  }

  async createVendor(vendorData) {
    const response = await apiClient.post('/contacts/vendors/', vendorData);
    return response.data;
  }

  async updateVendor(id, vendorData) {
    const response = await apiClient.put(`/contacts/vendors/${id}/`, vendorData);
    return response.data;
  }

  async deleteVendor(id) {
    const response = await apiClient.delete(`/contacts/vendors/${id}/`);
    return response.data;
  }
}

export default new ContactsService();
