<template>
  <div>
    <h1>Employees</h1>
    <!-- Add employee form -->
    <form @submit.prevent="addEmployee">
      <input v-model="newEmployee.first_name" placeholder="First Name" required>
      <input v-model="newEmployee.last_name" placeholder="Last Name" required>
      <input v-model="newEmployee.email" placeholder="Email" required>
      <input v-model="newEmployee.phone_number" placeholder="Phone Number">
      <input v-model="newEmployee.hire_date" type="date" required>
      <button type="submit">Add Employee</button>
    </form>

    <!-- Employees table -->
    <table>
      <thead>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Email</th>
          <th>Phone Number</th>
          <th>Hire Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in employees" :key="employee.employee_id">
          <td>{{ employee.first_name }}</td>
          <td>{{ employee.last_name }}</td>
          <td>{{ employee.email }}</td>
          <td>{{ employee.phone_number }}</td>
          <td>{{ employee.hire_date }}</td>
          <td>
            <button @click="editEmployee(employee)">Edit</button>
            <button @click="deleteEmployee(employee.employee_id)">Delete</button>
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
      employees: [],
      newEmployee: {
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        hire_date: ''
      }
    };
  },
  methods: {
    fetchEmployees() {
      axios.get('/api/payroll/employees/')
        .then(response => {
          this.employees = response.data;
        })
        .catch(error => {
          console.error('Error fetching employees:', error);
        });
    },
    addEmployee() {
      axios.post('/api/payroll/employees/', this.newEmployee)
        .then(response => {
          this.employees.push(response.data);
          this.newEmployee = { first_name: '', last_name: '', email: '', phone_number: '', hire_date: '' };
        })
        .catch(error => {
          console.error('Error adding employee:', error);
        });
    },
    editEmployee(employee) {
      // Implementation for editing an employee
    },
    deleteEmployee(employeeId) {
      axios.delete(`/api/payroll/employees/${employeeId}/`)
        .then(() => {
          this.employees = this.employees.filter(employee => employee.employee_id !== employeeId);
        })
        .catch(error => {
          console.error('Error deleting employee:', error);
        });
    }
  },
  mounted() {
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
