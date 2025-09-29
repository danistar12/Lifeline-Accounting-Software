<template>
  <div class="general-ledger">
    <h1>General Ledger</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!loading && !error">
      <table v-if="data && data.entries && data.entries.length" class="report-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Account</th>
            <th>Description</th>
            <th>Debit</th>
            <th>Credit</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, idx) in data.entries" :key="idx">
            <td>{{ entry.date }}</td>
            <td>{{ entry.account }}</td>
            <td>{{ entry.description }}</td>
            <td class="amount">{{ formatCurrency(entry.debit) }}</td>
            <td class="amount">{{ formatCurrency(entry.credit) }}</td>
            <td class="amount">{{ formatCurrency(entry.balance) }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else>No ledger entries available.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'GeneralLedger',
  data() {
    return {
      data: null,
      loading: false,
      error: null
    };
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await axios.get('/api/reports/general-ledger/');
      this.data = response.data;
    } catch (err) {
      this.error = 'Failed to load general ledger.';
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatCurrency(amount) {
      if (typeof amount !== 'number') return amount;
      return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
    }
  }
};
</script>

<style scoped>
.error { color: red; }
.report-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.report-table th, .report-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e9ecef;
  text-align: left;
}
.report-table th {
  background: #f8f9fa;
  font-size: 1.1rem;
  color: #2c3e50;
}
.report-table .amount {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
</style>