<template>
  <div class="dashboard">
    <h2 class="dashboard-title">Welcome to Lifeline Accounting</h2>
    <div class="dashboard-cards">
      <router-link v-for="card in cards" :key="card.label" :to="card.path" class="card-link">
        <div class="card">
          <div class="card-icon">{{ card.icon }}</div>
          <div class="card-content">
            <h3>{{ card.label }}</h3>
            <p>{{ card.desc }}</p>
          </div>
        </div>
      </router-link>
    </div>
    <div class="dashboard-charts">
      <div class="chart-card">
        <h4 class="chart-title">Monthly Revenue</h4>
        <svg class="chart-img" viewBox="0 0 320 120" width="320" height="120">
          <rect x="0" y="0" width="320" height="120" fill="#e3eafc" />
          <polyline points="10,110 60,80 110,90 160,40 210,60 260,30 310,70" fill="none" stroke="#2a5298" stroke-width="4" />
        </svg>
      </div>
      <div class="chart-card">
        <h4 class="chart-title">Expenses Breakdown</h4>
        <svg class="chart-img" viewBox="0 0 320 120" width="320" height="120">
          <rect x="0" y="0" width="320" height="120" fill="#e3eafc" />
          <circle cx="80" cy="60" r="40" fill="#2a5298" opacity="0.3" />
          <circle cx="240" cy="60" r="40" fill="#1e3c72" opacity="0.3" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
const cards = [
  { label: 'Accounts', desc: 'Manage all your accounts efficiently.', icon: '👤', path: '/accounts' },
  { label: 'Banking', desc: 'Track transactions and balances.', icon: '🏦', path: '/banking' },
  { label: 'Documents', desc: 'Upload and manage important files.', icon: '📄', path: '/documents' },
  { label: 'Reports', desc: 'View financial summaries and analytics.', icon: '📊', path: '/reports' },
];
</script>

<style>
.dashboard {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
.dashboard-title {
  color: #1e3c72;
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 32px;
}
.dashboard-cards {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  justify-content: space-between;
}
.card-link {
  text-decoration: none;
  flex: 1;
  min-width: 0;
  display: flex;
}
.card-link .card {
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  background: linear-gradient(120deg, #e3eafc 0%, #f8fbff 100%);
  box-shadow: 0 2px 12px rgba(30,60,114,0.08);
  border-radius: 16px;
  padding: 40px 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  min-width: 220px;
  flex: 1 1 0;
}
.card-link .card:hover {
  box-shadow: 0 8px 32px rgba(30,60,114,0.18);
  transform: translateY(-2px) scale(1.03);
  background: linear-gradient(120deg, #2a5298 0%, #1e3c72 100%);
  color: #fff;
}
.card-link .card:hover .card-content h3,
.card-link .card:hover .card-content p {
  color: #fff;
}
.card-link .card:hover .card-icon {
  background: #e3eafc;
  color: #2a5298;
}
.card-link:focus, .card-link:active {
  outline: none;
}
.card-icon {
  font-size: 2.8rem;
  background: #fff;
  border-radius: 50%;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(30,60,114,0.08);
}
.card-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.3rem;
  color: #1e3c72;
}
.card-content p {
  margin: 0;
  color: #2a5298;
  font-size: 1rem;
}
.dashboard-charts {
  display: flex;
  gap: 40px;
}
.chart-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(30,60,114,0.08);
  flex: 1;
  padding: 32px;
  text-align: center;
}
.chart-title {
  color: #1e3c72;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 12px;
}
.chart-img {
  width: 100%;
  max-width: 320px;
  margin-top: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(30,60,114,0.08);
}
@media (max-width: 900px) {
  .dashboard-cards, .dashboard-charts {
    flex-direction: column;
    gap: 20px;
  }
  .card-link .card {
    min-width: unset;
    padding: 24px 12px;
  }
}
</style>
