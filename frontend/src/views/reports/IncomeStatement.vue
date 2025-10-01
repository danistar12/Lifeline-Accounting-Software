<template>
  <div class="income-statement">
    <h1>Income Statement</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!loading && !error">
      <table v-if="data" class="report-table">
        <thead>
          <tr><th colspan="2">Revenue</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in data.revenue" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="amount">{{ formatCurrency(item.amount) }}</td>
          </tr>
          <tr class="section-total">
            <td><strong>Total Revenue</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.total_revenue) }}</strong></td>
          </tr>
        </tbody>
        <thead>
          <tr><th colspan="2">Expenses</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in data.expenses" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="amount">{{ formatCurrency(item.amount) }}</td>
          </tr>
          <tr class="section-total">
            <td><strong>Total Expenses</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.total_expenses) }}</strong></td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="net-income">
            <td><strong>Net Income</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.net_income) }}</strong></td>
          </tr>
        </tfoot>
      </table>
      <div v-else>No data available.</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'IncomeStatement',
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
      const response = await axios.get('/api/reports/income-statement/');
      this.data = response.data;
    } catch (err) {
      this.error = 'Failed to load income statement.';
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
.report-table .section-total td {
  font-weight: bold;
  background: #f1f3f6;
}
.report-table .net-income td {
  font-weight: bold;
  background: #e6ffe6;
  color: #1a7f37;
  font-size: 1.1rem;
}
</style>
