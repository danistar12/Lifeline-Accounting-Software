<template>
  <div class="vendors-container">
    <h1 class="page-title">Vendors</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Vendor</button>
      <div class="filters">
        <input type="text" placeholder="Search vendors..." class="search-input" />
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="vendors-table">
          <thead>
            <tr>
              <th>Vendor Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Balance Due</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Database fields from Vendor model will populate here -->
            <!-- vendor_id, name, email, phone, address, tax_id, balance -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VendorsView',
  data() {
    return {
      vendors: [] // Will be populated from API
    }
  }
}
</script>

<style scoped>
.vendors-container {
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
