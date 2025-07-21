<template>
  <div class="income-statement">
    <h1>Income Statement</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <pre v-if="!loading && !error">{{ data }}</pre>
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
  }
};
</script>

<style scoped>
.error { color: red; }
</style>
