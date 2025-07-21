// Absolute minimal test
console.log('main.ts starting...');

// Test 1: Direct DOM manipulation
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded');
  const app = document.getElementById('app');
  if (app) {
    app.innerHTML = '<h1 style="color: red; font-size: 3em; text-align: center; margin-top: 100px;">✅ SUCCESS! This means the server is working!</h1><p style="text-align: center; font-size: 1.5em;">If you see this, the issue was with Vue.js, not the server.</p>';
    console.log('HTML injected directly');
  } else {
    console.error('No #app element found!');
  }
});
