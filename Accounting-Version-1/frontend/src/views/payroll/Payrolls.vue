<template>
  <div>
    <h1>Payrolls</h1>
    <!-- Add payroll form -->
    <form @submit.prevent="addPayroll">
      <input v-model="newPayroll.run_date" type="date" required>
      <input v-model="newPayroll.pay_period_start" type="date" required>
      <input v-model="newPayroll.pay_period_end" type="date" required>
      <button type="submit">Add Payroll</button>
    </form>

    <!-- Payrolls table -->
    <table>
      <thead>
        <tr>
          <th>Run Date</th>
          <th>Pay Period Start</th>
          <th>Pay Period End</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payroll in payrolls" :key="payroll.payroll_id">
          <td>{{ payroll.run_date }}</td>
          <td>{{ payroll.pay_period_start }}</td>
          <td>{{ payroll.pay_period_end }}</td>
          <td>
            <button @click="editPayroll(payroll)">Edit</button>
            <button @click="deletePayroll(payroll.payroll_id)">Delete</button>
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
      payrolls: [],
      newPayroll: {
        run_date: '',
        pay_period_start: '',
        pay_period_end: ''
      }
    };
  },
  methods: {
    fetchPayrolls() {
      axios.get('/api/payroll/payrolls/')
        .then(response => {
          this.payrolls = response.data;
        })
        .catch(error => {
          console.error('Error fetching payrolls:', error);
        });
    },
    addPayroll() {
      axios.post('/api/payroll/payrolls/', this.newPayroll)
        .then(response => {
          this.payrolls.push(response.data);
          this.newPayroll = { run_date: '', pay_period_start: '', pay_period_end: '' };
        })
        .catch(error => {
          console.error('Error adding payroll:', error);
        });
    },
    editPayroll(payroll) {
      // Implementation for editing a payroll
    },
    deletePayroll(payrollId) {
      axios.delete(`/api/payroll/payrolls/${payrollId}/`)
        .then(() => {
          this.payrolls = this.payrolls.filter(payroll => payroll.payroll_id !== payrollId);
        })
        .catch(error => {
          console.error('Error deleting payroll:', error);
        });
    }
  },
  mounted() {
    this.fetchPayrolls();
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
