<template>
  <div class="bills-container">
    <h1 class="page-title">Bills</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Bill</button>
      <div class="filters">
        <input type="text" placeholder="Search bills..." class="search-input" />
        <select class="filter-select">
          <option value="all">All Bills</option>
          <option value="unpaid">Unpaid</option>
          <option value="paid">Paid</option>
          <option value="overdue">Overdue</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="bills-table">
          <thead>
            <tr>
              <th>Bill #</th>
              <th>Vendor</th>
              <th>Issue Date</th>
              <th>Due Date</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Database fields from Bill model will populate here -->
            <!-- bill_id, vendor_id, number, issue_date, due_date, amount, status -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BillsView',
  data() {
    return {
      bills: [] // Will be populated from API
    }
  }
}
</script>

<style scoped>
.bills-container {
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
