<template>
  <div class="bank-statement-lines">
    <h1>Bank Statement Lines</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="!loading && !error" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Date</th>
          <th>Description</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="line in lines" :key="line.statement_line_id">
          <td>{{ line.statement_line_id }}</td>
          <td>{{ line.date }}</td>
          <td>{{ line.description }}</td>
          <td>{{ line.amount }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'BankStatementLines',
  data() {
    return {
      lines: [],
      loading: false,
      error: null
    };
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await axios.get('/api/banking/statement-lines/');
      this.lines = response.data;
    } catch (err) {
      this.error = 'Failed to load statement lines.';
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { border: 1px solid #ddd; padding: 8px; }
.error { color: red; }
</style>
