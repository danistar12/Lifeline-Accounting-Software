<template>
  <div class="cash-flow">
    <h1>Cash Flow Statement</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!loading && !error">
      <table v-if="data" class="report-table">
        <thead>
          <tr><th colspan="2">Operating Activities</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in data.operating_activities" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="amount">{{ formatCurrency(item.amount) }}</td>
          </tr>
          <tr class="section-total">
            <td><strong>Net Cash from Operating Activities</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.net_operating) }}</strong></td>
          </tr>
        </tbody>
        <thead>
          <tr><th colspan="2">Investing Activities</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in data.investing_activities" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="amount">{{ formatCurrency(item.amount) }}</td>
          </tr>
          <tr class="section-total">
            <td><strong>Net Cash from Investing Activities</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.net_investing) }}</strong></td>
          </tr>
        </tbody>
        <thead>
          <tr><th colspan="2">Financing Activities</th></tr>
        </thead>
        <tbody>
          <tr v-for="item in data.financing_activities" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="amount">{{ formatCurrency(item.amount) }}</td>
          </tr>
          <tr class="section-total">
            <td><strong>Net Cash from Financing Activities</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.net_financing) }}</strong></td>
          </tr>
        </tbody>
        <tfoot>
          <tr class="net-cash">
            <td><strong>Net Increase in Cash</strong></td>
            <td class="amount"><strong>{{ formatCurrency(data.net_increase) }}</strong></td>
          </tr>
          <tr>
            <td>Beginning Cash Balance</td>
            <td class="amount">{{ formatCurrency(data.beginning_cash) }}</td>
          </tr>
          <tr>
            <td>Ending Cash Balance</td>
            <td class="amount">{{ formatCurrency(data.ending_cash) }}</td>
          </tr>
        </tfoot>
      </table>
      <div v-else>No data available.</div>
    </div>
  methods: {
    formatCurrency(amount) {
      if (typeof amount !== 'number') return amount;
      return amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
    }
  }
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'CashFlow',
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
      const response = await axios.get('/api/reports/cash-flow/');
      this.data = response.data;
    } catch (err) {
      this.error = 'Failed to load cash flow statement.';
    } finally {
      this.loading = false;
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
  .report-table .net-cash td {
    font-weight: bold;
    background: #e6ffe6;
    color: #1a7f37;
    font-size: 1.1rem;
  }
</style>
