import apiClient from './api';

class PaymentsService {
  // Invoice endpoints
  async getInvoices() {
    const response = await apiClient.get('/payments/invoices/');
    return response.data;
  }

  async getInvoice(id) {
    const response = await apiClient.get(`/payments/invoices/${id}/`);
    return response.data;
  }

  async createInvoice(invoiceData) {
    const response = await apiClient.post('/payments/invoices/', invoiceData);
    return response.data;
  }

  async updateInvoice(id, invoiceData) {
    const response = await apiClient.put(`/payments/invoices/${id}/`, invoiceData);
    return response.data;
  }

  async deleteInvoice(id) {
    const response = await apiClient.delete(`/payments/invoices/${id}/`);
    return response.data;
  }

  // Bill endpoints
  async getBills() {
    const response = await apiClient.get('/payments/bills/');
    return response.data;
  }

  async getBill(id) {
    const response = await apiClient.get(`/payments/bills/${id}/`);
    return response.data;
  }

  async createBill(billData) {
    const response = await apiClient.post('/payments/bills/', billData);
    return response.data;
  }

  async updateBill(id, billData) {
    const response = await apiClient.put(`/payments/bills/${id}/`, billData);
    return response.data;
  }

  async deleteBill(id) {
    const response = await apiClient.delete(`/payments/bills/${id}/`);
    return response.data;
  }

  // Payment endpoints
  async getPayments() {
    const response = await apiClient.get('/payments/payments/');
    return response.data;
  }

  async getPayment(id) {
    const response = await apiClient.get(`/payments/payments/${id}/`);
    return response.data;
  }

  async createPayment(paymentData) {
    const response = await apiClient.post('/payments/payments/', paymentData);
    return response.data;
  }

  async updatePayment(id, paymentData) {
    const response = await apiClient.put(`/payments/payments/${id}/`, paymentData);
    return response.data;
  }

  async deletePayment(id) {
    const response = await apiClient.delete(`/payments/payments/${id}/`);
    return response.data;
  }
}

export default new PaymentsService();
