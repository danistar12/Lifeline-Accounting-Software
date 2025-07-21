<template>
  <div class="view-container">
    <h2 class="view-title">Banking</h2>
    <div class="view-card">
      <p>Track transactions and balances.</p>
    </div>
  </div>
</template>

<script setup>
// Add logic here
</script>

<style>
.view-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
.view-title {
  color: #1e3c72;
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 32px;
}
.view-card {
  transition: box-shadow 0.2s, transform 0.2s;
  background: linear-gradient(120deg, #e3eafc 0%, #f8fbff 100%);
  box-shadow: 0 2px 12px rgba(30,60,114,0.08);
  border-radius: 16px;
  padding: 40px 32px;
  margin-bottom: 32px;
  color: #1e3c72;
}
.view-card:hover {
  box-shadow: 0 8px 32px rgba(30,60,114,0.18);
  transform: translateY(-2px) scale(1.03);
  background: linear-gradient(120deg, #2a5298 0%, #1e3c72 100%);
  color: #fff;
}
</style>
