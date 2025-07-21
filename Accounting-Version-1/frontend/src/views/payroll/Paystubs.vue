<template>
  <div>
    <h1>Paystubs</h1>
    <!-- Add paystub form -->
    <form @submit.prevent="addPaystub">
      <select v-model="newPaystub.payroll" required>
        <option v-for="payroll in payrolls" :key="payroll.payroll_id" :value="payroll.payroll_id">{{ payroll.run_date }}</option>
      </select>
      <select v-model="newPaystub.employee" required>
        <option v-for="employee in employees" :key="employee.employee_id" :value="employee.employee_id">{{ employee.first_name }} {{ employee.last_name }}</option>
      </select>
      <input v-model="newPaystub.gross_pay" placeholder="Gross Pay" required>
      <input v-model="newPaystub.net_pay" placeholder="Net Pay" required>
      <button type="submit">Add Paystub</button>
    </form>

    <!-- Paystubs table -->
    <table>
      <thead>
        <tr>
          <th>Payroll</th>
          <th>Employee</th>
          <th>Gross Pay</th>
          <th>Net Pay</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="paystub in paystubs" :key="paystub.paystub_id">
          <td>{{ paystub.payroll }}</td>
          <td>{{ paystub.employee }}</td>
          <td>{{ paystub.gross_pay }}</td>
          <td>{{ paystub.net_pay }}</td>
          <td>
            <button @click="editPaystub(paystub)">Edit</button>
            <button @click="deletePaystub(paystub.paystub_id)">Delete</button>
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
      paystubs: [],
      payrolls: [],
      employees: [],
      newPaystub: {
        payroll: '',
        employee: '',
        gross_pay: '',
        net_pay: ''
      }
    };
  },
  methods: {
    fetchPaystubs() {
      axios.get('/api/payroll/paystubs/')
        .then(response => {
          this.paystubs = response.data;
        })
        .catch(error => {
          console.error('Error fetching paystubs:', error);
        });
    },
    fetchPayrolls() {
      axios.get('/api/payroll/payrolls/')
        .then(response => {
          this.payrolls = response.data;
        })
        .catch(error => {
          console.error('Error fetching payrolls:', error);
        });
    },
    fetchEmployees() {
      axios.get('/api/payroll/employees/')
        .then(response => {
          this.employees = response.data;
        })
        .catch(error => {
          console.error('Error fetching employees:', error);
        });
    },
    addPaystub() {
      axios.post('/api/payroll/paystubs/', this.newPaystub)
        .then(response => {
          this.paystubs.push(response.data);
          this.newPaystub = { payroll: '', employee: '', gross_pay: '', net_pay: '' };
        })
        .catch(error => {
          console.error('Error adding paystub:', error);
        });
    },
    editPaystub(paystub) {
      // Implementation for editing a paystub
    },
    deletePaystub(paystubId) {
      axios.delete(`/api/payroll/paystubs/${paystubId}/`)
        .then(() => {
          this.paystubs = this.paystubs.filter(paystub => paystub.paystub_id !== paystubId);
        })
        .catch(error => {
          console.error('Error deleting paystub:', error);
        });
    }
  },
  mounted() {
    this.fetchPaystubs();
    this.fetchPayrolls();
    this.fetchEmployees();
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
