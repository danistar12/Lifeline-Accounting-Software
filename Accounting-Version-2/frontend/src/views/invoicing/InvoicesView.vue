<template>
  <div class="invoices-container">
    <h1 class="page-title">Invoices</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Invoice</button>
      <div class="filters">
        <input type="text" placeholder="Search invoices..." class="search-input" />
        <select class="filter-select">
          <option value="all">All Invoices</option>
          <option value="draft">Draft</option>
          <option value="sent">Sent</option>
          <option value="paid">Paid</option>
          <option value="overdue">Overdue</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="invoices-table">
          <thead>
            <tr>
              <th>Invoice #</th>
              <th>Customer</th>
              <th>Issue Date</th>
              <th>Due Date</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Database fields from Invoice model will populate here -->
            <!-- invoice_id, customer_id, number, issue_date, due_date, amount, status -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InvoicesView',
  data() {
    return {
      invoices: [] // Will be populated from API
    }
  }
}
</script>

<style scoped>
.invoices-container {
  padding: 20px;
}
.page-title {
  font-size: 1.8rem;
  color: #2a5298;
  margin-bottom: 24px;
}
</style>
