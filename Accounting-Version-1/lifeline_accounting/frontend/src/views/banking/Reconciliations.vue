<template>
  <div class="reconciliations">
    <h1>Reconciliation Entries</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="!loading && !error" class="table">
      <thead>
        <tr>
          <th>Entry ID</th>
          <th>Statement Line ID</th>
          <th>GL Transaction ID</th>
          <th>Reconciled Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in entries" :key="entry.entry_id">
          <td>{{ entry.entry_id }}</td>
          <td>{{ entry.statement_line }}</td>
          <td>{{ entry.gl_transaction }}</td>
          <td>{{ entry.reconciled_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Reconciliations',
  data() {
    return {
      entries: [],
      loading: false,
      error: null
    };
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await axios.get('/api/banking/reconciliations/');
      this.entries = response.data;
    } catch (err) {
      this.error = 'Failed to load reconciliation entries.';
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
