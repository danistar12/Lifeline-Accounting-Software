<template>
  <div class="payments-container">
    <h1 class="page-title">Payments</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary" @click="showCreateForm = true">New Payment</button>
      <div class="filters">
        <input 
          type="text" 
          placeholder="Search payments..." 
          class="search-input" 
          v-model="searchTerm"
          @input="filterPayments"
        />
        <select class="filter-select" v-model="typeFilter" @change="filterPayments">
          <option value="all">All Payments</option>
          <option value="AR">Accounts Receivable</option>
          <option value="AP">Accounts Payable</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="payments-table">
          <thead>
            <tr>
              <th>Payment #</th>
              <th>Date</th>
              <th>Type</th>
              <th>Amount</th>
              <th>Reference</th>
              <th>Method</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payment in filteredPayments" :key="payment.payment_id">
              <td>{{ payment.payment_id }}</td>
              <td>{{ formatDate(payment.payment_date) }}</td>
              <td>{{ payment.type === 'AR' ? 'Receivable' : 'Payable' }}</td>
              <td>${{ payment.amount.toFixed(2) }}</td>
              <td>{{ payment.reference_number || 'N/A' }}</td>
              <td>{{ payment.payment_method || 'N/A' }}</td>
              <td>
                <span :class="getStatusClass(payment.status)">
                  {{ payment.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline" @click="editPayment(payment)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deletePayment(payment.payment_id)">Delete</button>
              </td>
            </tr>
            <tr v-if="filteredPayments.length === 0">
              <td colspan="8" class="text-center">No payments found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import paymentsService from '@/services/paymentsService'

export default {
  name: 'PaymentsView',
  data() {
    return {
      payments: [],
      filteredPayments: [],
      searchTerm: '',
      typeFilter: 'all',
      showCreateForm: false,
      loading: false
    }
  },
  async mounted() {
    await this.fetchPayments()
  },
  methods: {
    async fetchPayments() {
      try {
        this.loading = true
        // Fetch both AR and AP payments
        const [arResponse, apResponse] = await Promise.all([
          paymentsService.getARPayments(),
          paymentsService.getAPPayments()
        ])
        
        // Combine and mark the type
        const arPayments = arResponse.data.map(p => ({ ...p, type: 'AR' }))
        const apPayments = apResponse.data.map(p => ({ ...p, type: 'AP' }))
        
        this.payments = [...arPayments, ...apPayments]
        this.filteredPayments = [...this.payments]
      } catch (error) {
        console.error('Error fetching payments:', error)
      } finally {
        this.loading = false
      }
    },
    filterPayments() {
      let filtered = [...this.payments]
      
      // Filter by type
      if (this.typeFilter !== 'all') {
        filtered = filtered.filter(payment => payment.type === this.typeFilter)
      }
      
      // Filter by search term
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(payment => 
          payment.payment_id.toString().includes(term) ||
          (payment.reference_number && payment.reference_number.toLowerCase().includes(term)) ||
          (payment.payment_method && payment.payment_method.toLowerCase().includes(term))
        )
      }
      
      this.filteredPayments = filtered
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    getStatusClass(status) {
      return {
        'status-pending': status === 'Pending',
        'status-completed': status === 'Completed',
        'status-failed': status === 'Failed'
      }
    },
    editPayment(payment) {
      // TODO: Implement edit functionality
      console.log('Edit payment:', payment)
    },
    async deletePayment(paymentId) {
      if (confirm('Are you sure you want to delete this payment?')) {
        try {
          // Determine which service to use based on the payment type
          const payment = this.payments.find(p => p.payment_id === paymentId)
          if (payment.type === 'AR') {
            await paymentsService.deleteARPayment(paymentId)
          } else {
            await paymentsService.deleteAPPayment(paymentId)
          }
          await this.fetchPayments() // Refresh the list
        } catch (error) {
          console.error('Error deleting payment:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
.payments-container {
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
.filters {
  display: flex;
  gap: 10px;
}
.search-input, .filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.payments-table {
  width: 100%;
  border-collapse: collapse;
}
.payments-table th,
.payments-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.payments-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}
.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}
.btn-sm {
  padding: 4px 8px;
  font-size: 0.875rem;
}
.btn-outline {
  background: white;
  border: 1px solid #2a5298;
  color: #2a5298;
}
.btn-danger {
  background-color: #dc3545;
  color: white;
}
.text-center {
  text-align: center;
}
.status-pending {
  color: #ffc107;
  font-weight: 600;
}
.status-completed {
  color: #28a745;
  font-weight: 600;
}
.status-failed {
  color: #dc3545;
  font-weight: 600;
}
</style>
