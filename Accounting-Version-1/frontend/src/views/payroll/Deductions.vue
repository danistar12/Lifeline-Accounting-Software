<template>
  <div>
    <h1>Deductions</h1>
    <!-- Add deduction form -->
    <form @submit.prevent="addDeduction">
      <select v-model="newDeduction.paystub" required>
        <option v-for="paystub in paystubs" :key="paystub.paystub_id" :value="paystub.paystub_id">{{ paystub.paystub_id }}</option>
      </select>
      <input v-model="newDeduction.deduction_name" placeholder="Deduction Name" required>
      <input v-model="newDeduction.deduction_amount" placeholder="Deduction Amount" required>
      <button type="submit">Add Deduction</button>
    </form>

    <!-- Deductions table -->
    <table>
      <thead>
        <tr>
          <th>Paystub</th>
          <th>Deduction Name</th>
          <th>Deduction Amount</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="deduction in deductions" :key="deduction.deduction_id">
          <td>{{ deduction.paystub }}</td>
          <td>{{ deduction.deduction_name }}</td>
          <td>{{ deduction.deduction_amount }}</td>
          <td>
            <button @click="editDeduction(deduction)">Edit</button>
            <button @click="deleteDeduction(deduction.deduction_id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      deductions: [],
      paystubs: [],
      newDeduction: {
        paystub: '',
        deduction_name: '',
        deduction_amount: ''
      }
    };
  },
  methods: {
    fetchDeductions() {
      axios.get('/api/payroll/deductions/')
        .then(response => {
          this.deductions = response.data;
        })
        .catch(error => {
          console.error('Error fetching deductions:', error);
        });
    },
    fetchPaystubs() {
      axios.get('/api/payroll/paystubs/')
        .then(response => {
          this.paystubs = response.data;
        })
        .catch(error => {
          console.error('Error fetching paystubs:', error);
        });
    },
    addDeduction() {
      axios.post('/api/payroll/deductions/', this.newDeduction)
        .then(response => {
          this.deductions.push(response.data);
          this.newDeduction = { paystub: '', deduction_name: '', deduction_amount: '' };
        })
        .catch(error => {
          console.error('Error adding deduction:', error);
        });
    },
    editDeduction(deduction) {
      axios.put(`/api/payroll/deductions/${deduction.deduction_id}/`, deduction)
        .then(response => {
          const index = this.deductions.findIndex(d => d.deduction_id === deduction.deduction_id);
          if (index !== -1) {
            this.deductions.splice(index, 1, response.data);
          }
        })
        .catch(error => {
          console.error('Error editing deduction:', error);
        });
    },
    deleteDeduction(deductionId) {
      axios.delete(`/api/payroll/deductions/${deductionId}/`)
        .then(() => {
          this.deductions = this.deductions.filter(deduction => deduction.deduction_id !== deductionId);
        })
        .catch(error => {
          console.error('Error deleting deduction:', error);
        });
    }
  },
  mounted() {
    this.fetchDeductions();
    this.fetchPaystubs();
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background-color: #f2f2f2;
}
</style>
