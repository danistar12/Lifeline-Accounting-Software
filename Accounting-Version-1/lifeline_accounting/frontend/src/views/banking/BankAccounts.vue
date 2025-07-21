<template>
  <div class="bank-accounts">
    <h1>Bank Accounts</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="!loading && !error" class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Account Number</th>
          <th>Bank Name</th>
          <th>Created Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="acct in accounts" :key="acct.bank_account_id">
          <td>{{ acct.bank_account_id }}</td>
          <td>{{ acct.account_number }}</td>
          <td>{{ acct.bank_name }}</td>
          <td>{{ acct.created_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'BankAccounts',
  data() {
    return {
      accounts: [],
      loading: false,
      error: null
    };
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await axios.get('/api/banking/accounts/');
      this.accounts = response.data;
    } catch (err) {
      this.error = 'Failed to load bank accounts.';
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
