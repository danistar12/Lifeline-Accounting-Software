<template>
  <div class="ar-payments">
    <h1>Accounts Receivable Payments</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="!loading && !error" class="table">
      <thead>
        <tr>
          <th>Payment ID</th>
          <th>Company</th>
          <th>Invoice</th>
          <th>Date</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in payments" :key="p.payment_id">
          <td>{{ p.payment_id }}</td>
          <td>{{ p.company }}</td>
          <td>{{ p.invoice }}</td>
          <td>{{ p.payment_date }}</td>
          <td>{{ p.amount }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ARPayments',
  data() {
    return {
      payments: [],
      loading: false,
      error: null
    };
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await axios.get('/api/ar/ar-payments/');
      this.payments = response.data;
    } catch (err) {
      this.error = 'Failed to load AR payments.';
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}
.error {
  color: red;
}
</style>
