<template>
  <select
    v-if="companies && companies.length"
    class="form-select"
    v-model="selectedCompany"
    @change="updateCompany"
  >
    <!-- Placeholder when no company selected -->
    <option disabled value="">Select Company</option>
    <option
      v-for="company in companies"
      :value="company.company_id"
      :key="company.company_id"
    >
      {{ company.company_name }}
    </option>
  </select>
  <!-- Show loading placeholder if companies not yet loaded -->
  <div v-else-if="isLoggedIn">Loading companies...</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';

export default {
  computed: {
    ...mapGetters(['isLoggedIn']),
    companies() {
      return this.$store.state.user?.companies || [];
    },
    selectedCompany: {
      get() {
        return this.$store.state.selectedCompany.id;
      },
      set(value) {
        this.$store.commit('setSelectedCompany', value);
      },
    },
  },
  methods: {
    ...mapActions(['loadCompanyData']),
    updateCompany() {
      // Set the company ID header for API requests
      axios.defaults.headers.common['X-Company-ID'] = this.selectedCompany;
      // Load company-specific data
      this.loadCompanyData();
    },
  },
  mounted() {
    // If user is logged in but no companies loaded, try to load them
    if (this.isLoggedIn && (!this.companies || this.companies.length === 0)) {
      this.$store.dispatch('loadCompanies');
    }
  }
};
</script>
