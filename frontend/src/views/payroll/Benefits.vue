<template>
  <div>
    <h1>Benefits</h1>
    <!-- Add benefit form -->
    <form @submit.prevent="addBenefit">
      <select v-model="newBenefit.paystub" required>
        <option v-for="paystub in paystubs" :key="paystub.paystub_id" :value="paystub.paystub_id">{{ paystub.paystub_id }}</option>
      </select>
      <input v-model="newBenefit.benefit_name" placeholder="Benefit Name" required>
      <input v-model="newBenefit.benefit_amount" placeholder="Benefit Amount" required>
      <button type="submit">Add Benefit</button>
    </form>

    <!-- Benefits table -->
    <table>
      <thead>
        <tr>
          <th>Paystub</th>
          <th>Benefit Name</th>
          <th>Benefit Amount</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="benefit in benefits" :key="benefit.benefit_id">
          <td>{{ benefit.paystub }}</td>
          <td>{{ benefit.benefit_name }}</td>
          <td>{{ benefit.benefit_amount }}</td>
          <td>
            <button @click="editBenefit(benefit)">Edit</button>
            <button @click="deleteBenefit(benefit.benefit_id)">Delete</button>
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
      benefits: [],
      paystubs: [],
      newBenefit: {
        paystub: '',
        benefit_name: '',
        benefit_amount: ''
      }
    };
  },
  methods: {
    fetchBenefits() {
      axios.get('/api/payroll/benefits/')
        .then(response => {
          this.benefits = response.data;
        })
        .catch(error => {
          console.error('Error fetching benefits:', error);
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
    addBenefit() {
      axios.post('/api/payroll/benefits/', this.newBenefit)
        .then(response => {
          this.benefits.push(response.data);
          this.newBenefit = { paystub: '', benefit_name: '', benefit_amount: '' };
        })
        .catch(error => {
          console.error('Error adding benefit:', error);
        });
    },
    editBenefit(benefit) {
      axios.put(`/api/payroll/benefits/${benefit.benefit_id}/`, benefit)
        .then(response => {
          const index = this.benefits.findIndex(b => b.benefit_id === benefit.benefit_id);
          if (index !== -1) {
            this.benefits.splice(index, 1, response.data);
          }
        })
        .catch(error => {
          console.error('Error editing benefit:', error);
        });
    },
    deleteBenefit(benefitId) {
      axios.delete(`/api/payroll/benefits/${benefitId}/`)
        .then(() => {
          this.benefits = this.benefits.filter(benefit => benefit.benefit_id !== benefitId);
        })
        .catch(error => {
          console.error('Error deleting benefit:', error);
        });
    }
  },
  mounted() {
    this.fetchBenefits();
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
