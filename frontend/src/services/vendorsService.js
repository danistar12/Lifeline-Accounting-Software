import apiClient from './apiClient';

class VendorsService {
  async getVendors() {
    const response = await apiClient.get('/vendors/');
    return response.data;
  }

  async getVendor(id) {
    const response = await apiClient.get(`/vendors/${id}/`);
    return response.data;
  }

  async createVendor(data) {
    const response = await apiClient.post('/vendors/', data);
    return response.data;
  }

  async updateVendor(id, data) {
    const response = await apiClient.put(`/vendors/${id}/`, data);
    return response.data;
  }

  async deleteVendor(id) {
    const response = await apiClient.delete(`/vendors/${id}/`);
    return response.data;
  }
}

export default new VendorsService();
