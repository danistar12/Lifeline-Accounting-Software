<template>
  <div class="reports-container">
    <h1>Financial Reports</h1>
    <div class="reports-list">
      <router-link class="report-link" to="/reports/income-statement">
        <div class="report-card">
          <h2>Income Statement</h2>
          <p>View your revenues, expenses, and net income for a period.</p>
        </div>
      </router-link>
      <router-link class="report-link" to="/reports/balance-sheet">
        <div class="report-card">
          <h2>Balance Sheet</h2>
          <p>See your assets, liabilities, and equity at a glance.</p>
        </div>
      </router-link>
      <router-link class="report-link" to="/reports/cash-flow">
        <div class="report-card">
          <h2>Cash Flow Statement</h2>
          <p>Track cash inflows and outflows from operations, investing, and financing.</p>
        </div>
      </router-link>
      <router-link class="report-link" to="/reports/general-ledger">
        <div class="report-card">
          <h2>General Ledger</h2>
          <p>Browse all journal entries and account activity.</p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReportsView',
};
</script>

<style scoped>
.reports-container {
  padding: 2rem;
}
.reports-list {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2rem;
}
.report-link {
  text-decoration: none;
  flex: 1 1 250px;
  min-width: 250px;
  max-width: 350px;
}
.report-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 1.5rem;
  transition: box-shadow 0.2s;
  height: 100%;
}
.report-card:hover {
  box-shadow: 0 4px 16px rgba(44,62,80,0.12);
}
.report-card h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
}
.report-card p {
  color: #555;
  margin: 0;
}
</style>