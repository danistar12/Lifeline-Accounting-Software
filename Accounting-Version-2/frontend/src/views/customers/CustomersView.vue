<template>
  <div class="customers-container">
    <h1 class="page-title">Customers</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Customer</button>
      <div class="filters">
        <input type="text" placeholder="Search customers..." class="search-input" />
        <select class="filter-select">
          <option value="all">All Customers</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="customers-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Balance</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Acme Corporation</td>
              <td>contact@acmecorp.com</td>
              <td>(555) 123-4567</td>
              <td>$3,750.00</td>
              <td><span class="badge badge-success">Active</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
                <button class="btn btn-sm btn-outline">Edit</button>
              </td>
            </tr>
            <tr>
              <td>TechStart Inc</td>
              <td>info@techstart.com</td>
              <td>(555) 234-5678</td>
              <td>$1,200.00</td>
              <td><span class="badge badge-success">Active</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
                <button class="btn btn-sm btn-outline">Edit</button>
              </td>
            </tr>
            <tr>
              <td>Global Services LLC</td>
              <td>contact@globalservices.com</td>
              <td>(555) 345-6789</td>
              <td>$0.00</td>
              <td><span class="badge badge-neutral">Inactive</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
                <button class="btn btn-sm btn-outline">Edit</button>
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
  name: 'CustomersView',
  data() {
    return {
      // Data will be populated from API calls
    };
  },
  methods: {
    // Methods to handle customer actions
  }
};
</script>

<style scoped>
.customers-container {
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

.customers-table {
  width: 100%;
  border-collapse: collapse;
}

.customers-table th {
  text-align: left;
  padding: 14px 20px;
  border-bottom: 2px solid #eee;
  color: #555;
  font-weight: 600;
}

.customers-table td {
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

.badge-neutral {
  background-color: #eee;
  color: #666;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 4px;
  margin-right: 5px;
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
