<template>
  <div class="payments-ap-container">
    <h1 class="page-title">Made Payments</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Payment</button>
      <div class="filters">
        <input type="text" placeholder="Search payments..." class="search-input" />
        <select class="filter-select">
          <option value="all">All Payments</option>
          <option value="pending">Pending</option>
          <option value="completed">Completed</option>
          <option value="scheduled">Scheduled</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="payments-table">
          <thead>
            <tr>
              <th>Payment #</th>
              <th>Vendor</th>
              <th>Bill #</th>
              <th>Date</th>
              <th>Amount</th>
              <th>Method</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>PAY-AP-001</td>
              <td>Office Supplies Co</td>
              <td>BILL-2025-001</td>
              <td>Jul 10, 2025</td>
              <td>$450.00</td>
              <td>ACH Transfer</td>
              <td><span class="badge badge-success">Completed</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
              </td>
            </tr>
            <tr>
              <td>PAY-AP-002</td>
              <td>Cloud Services Inc</td>
              <td>BILL-2025-003</td>
              <td>Jul 12, 2025</td>
              <td>$1,200.00</td>
              <td>Credit Card</td>
              <td><span class="badge badge-success">Completed</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
              </td>
            </tr>
            <tr>
              <td>PAY-AP-003</td>
              <td>Consulting Partners LLC</td>
              <td>BILL-2025-007</td>
              <td>Jul 25, 2025</td>
              <td>$3,800.00</td>
              <td>Check</td>
              <td><span class="badge badge-info">Scheduled</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div class="pagination">
          <button class="btn btn-sm">&laquo; Previous</button>
          <span class="page-info">Page 1 of 1</span>
          <button class="btn btn-sm">Next &raquo;</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentsAPView',
  data() {
    return {
      // Data will be populated from API calls
    };
  },
  methods: {
    // Methods to handle payment actions
  }
};
</script>

<style scoped>
.payments-ap-container {
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
  cursor: pointer;
  font-weight: 500;
}

.filters {
  display: flex;
  gap: 12px;
}

.search-input, .filter-select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  min-width: 200px;
}

.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-body {
  padding: 20px;
}

.payments-table {
  width: 100%;
  border-collapse: collapse;
}

.payments-table th {
  text-align: left;
  padding: 14px 20px;
  border-bottom: 2px solid #eee;
  color: #555;
  font-weight: 600;
}

.payments-table td {
  padding: 14px 20px;
  border-bottom: 1px solid #eee;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.badge-success {
  background-color: #dcf5e8;
  color: #0d9152;
}

.badge-warning {
  background-color: #fff4de;
  color: #be8114;
}

.badge-info {
  background-color: #deefff;
  color: #1475be;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 4px;
}

.btn-outline {
  border: 1px solid #2a5298;
  color: #2a5298;
  background: transparent;
  cursor: pointer;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-info {
  color: #666;
}
</style>
