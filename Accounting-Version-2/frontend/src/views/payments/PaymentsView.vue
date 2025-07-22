<template>
  <div class="payments-container">
    <h1 class="page-title">Payments</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Payment</button>
      <div class="filters">
        <input type="text" placeholder="Search payments..." class="search-input" />
        <select class="filter-select">
          <option value="all">All Payments</option>
          <option value="incoming">Incoming</option>
          <option value="outgoing">Outgoing</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="payments-table">
          <thead>
            <tr>
              <th>Payment #</th>
              <th>Date</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Reference</th>
              <th>Method</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Database fields from Payment model will populate here -->
            <!-- payment_id, date, type, amount, reference, method, status -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentsView',
  data() {
    return {
      payments: [] // Will be populated from API
    }
  }
}
</script>

<style scoped>
.payments-container {
  padding: 20px;
}
.page-title {
  font-size: 1.8rem;
  color: #2a5298;
  margin-bottom: 24px;
}
.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.btn-primary {
  background-color: #2a5298;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
}
.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
</style>
