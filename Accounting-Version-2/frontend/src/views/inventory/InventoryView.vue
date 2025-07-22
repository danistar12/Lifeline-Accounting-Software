<template>
  <div class="inventory-container">
    <h1 class="page-title">Inventory Management</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Item</button>
      <div class="filters">
        <input type="text" placeholder="Search inventory..." class="search-input" />
        <select class="filter-select">
          <option value="all">All Items</option>
          <option value="in-stock">In Stock</option>
          <option value="low-stock">Low Stock</option>
          <option value="out-of-stock">Out of Stock</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="inventory-table">
          <thead>
            <tr>
              <th>Item Name</th>
              <th>SKU</th>
              <th>Category</th>
              <th>Qty In Stock</th>
              <th>Unit Price</th>
              <th>Value</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Office Chair - Premium</td>
              <td>FRN-001</td>
              <td>Furniture</td>
              <td>24</td>
              <td>$189.99</td>
              <td>$4,559.76</td>
              <td><span class="badge badge-success">In Stock</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
                <button class="btn btn-sm btn-outline">Edit</button>
              </td>
            </tr>
            <tr>
              <td>Standing Desk - Adjustable</td>
              <td>FRN-023</td>
              <td>Furniture</td>
              <td>12</td>
              <td>$349.99</td>
              <td>$4,199.88</td>
              <td><span class="badge badge-success">In Stock</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
                <button class="btn btn-sm btn-outline">Edit</button>
              </td>
            </tr>
            <tr>
              <td>Wireless Mouse - Pro</td>
              <td>ELC-045</td>
              <td>Electronics</td>
              <td>3</td>
              <td>$59.99</td>
              <td>$179.97</td>
              <td><span class="badge badge-warning">Low Stock</span></td>
              <td>
                <button class="btn btn-sm btn-outline">View</button>
                <button class="btn btn-sm btn-outline">Edit</button>
              </td>
            </tr>
            <tr>
              <td>Premium Headset</td>
              <td>ELC-078</td>
              <td>Electronics</td>
              <td>0</td>
              <td>$129.99</td>
              <td>$0.00</td>
              <td><span class="badge badge-danger">Out of Stock</span></td>
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
    
    <div class="card mt-20">
      <div class="card-header">
        <h2 class="card-title">Recent Inventory Adjustments</h2>
      </div>
      <div class="card-body">
        <table class="adjustments-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Item</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Reason</th>
              <th>Adjusted By</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Jul 20, 2025</td>
              <td>Wireless Mouse - Pro</td>
              <td><span class="badge badge-info">Receive</span></td>
              <td>+5</td>
              <td>Purchase Order #12345</td>
              <td>Jane Smith</td>
            </tr>
            <tr>
              <td>Jul 19, 2025</td>
              <td>Premium Headset</td>
              <td><span class="badge badge-primary">Sell</span></td>
              <td>-2</td>
              <td>Invoice #INV-2025-089</td>
              <td>System</td>
            </tr>
            <tr>
              <td>Jul 18, 2025</td>
              <td>Office Chair - Premium</td>
              <td><span class="badge badge-info">Receive</span></td>
              <td>+10</td>
              <td>Purchase Order #12340</td>
              <td>John Doe</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InventoryView',
  data() {
    return {
      // Data will be populated from API calls
    };
  },
  methods: {
    // Methods to handle inventory actions
  }
};
</script>

<style scoped>
.inventory-container {
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
  margin-bottom: 24px;
}

.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.card-title {
  margin: 0;
  font-size: 1.2rem;
  color: #2a5298;
}

.card-body {
  padding: 20px;
}

.inventory-table, .adjustments-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table th, .adjustments-table th {
  text-align: left;
  padding: 14px 20px;
  border-bottom: 2px solid #eee;
  color: #555;
  font-weight: 600;
}

.inventory-table td, .adjustments-table td {
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

.badge-danger {
  background-color: #ffe8e8;
  color: #cf3636;
}

.badge-info {
  background-color: #deefff;
  color: #1475be;
}

.badge-primary {
  background-color: #e0e8ff;
  color: #2a5298;
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

.mt-20 {
  margin-top: 20px;
}
</style>
