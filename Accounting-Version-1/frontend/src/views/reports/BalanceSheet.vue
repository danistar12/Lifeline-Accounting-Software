<template>
  <div class="balance-sheet">
    <h1>Balance Sheet</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <pre v-if="!loading && !error">{{ data }}</pre>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'BalanceSheet',
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
      const response = await axios.get('/api/reports/balance-sheet/');
      this.data = response.data;
    } catch (err) {
      this.error = 'Failed to load balance sheet.';
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.error { color: red; }
</style>
