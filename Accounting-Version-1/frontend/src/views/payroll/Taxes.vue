<template>
  <div>
    <h1>Taxes</h1>
    <!-- Add tax form -->
    <form @submit.prevent="addTax">
      <select v-model="newTax.paystub" required>
        <option v-for="paystub in paystubs" :key="paystub.paystub_id" :value="paystub.paystub_id">{{ paystub.paystub_id }}</option>
      </select>
      <input v-model="newTax.tax_name" placeholder="Tax Name" required>
      <input v-model="newTax.tax_amount" placeholder="Tax Amount" required>
      <button type="submit">Add Tax</button>
    </form>

    <!-- Taxes table -->
    <table>
      <thead>
        <tr>
          <th>Paystub</th>
          <th>Tax Name</th>
          <th>Tax Amount</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tax in taxes" :key="tax.tax_id">
          <td>{{ tax.paystub }}</td>
          <td>{{ tax.tax_name }}</td>
          <td>{{ tax.tax_amount }}</td>
          <td>
            <button @click="editTax(tax)">Edit</button>
            <button @click="deleteTax(tax.tax_id)">Delete</button>
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
      taxes: [],
      paystubs: [],
      newTax: {
        paystub: '',
        tax_name: '',
        tax_amount: ''
      }
    };
  },
  methods: {
    fetchTaxes() {
      axios.get('/api/payroll/taxes/')
        .then(response => {
          this.taxes = response.data;
        })
        .catch(error => {
          console.error('Error fetching taxes:', error);
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
    addTax() {
      axios.post('/api/payroll/taxes/', this.newTax)
        .then(response => {
          this.taxes.push(response.data);
          this.newTax = { paystub: '', tax_name: '', tax_amount: '' };
        })
        .catch(error => {
          console.error('Error adding tax:', error);
        });
    },
    editTax(tax) {
      console.log('Editing tax:', tax);
      // Add logic to edit tax here
    },
    deleteTax(taxId) {
      axios.delete(`/api/payroll/taxes/${taxId}/`)
        .then(() => {
          this.taxes = this.taxes.filter(tax => tax.tax_id !== taxId);
        })
        .catch(error => {
          console.error('Error deleting tax:', error);
        });
    }
  },
  mounted() {
    this.fetchTaxes();
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
