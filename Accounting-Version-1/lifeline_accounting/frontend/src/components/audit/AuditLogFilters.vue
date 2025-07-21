<template>
  <div class="audit-log-filters">
    <form @submit.prevent="applyFilters">
      <div class="row g-3">
        <!-- Search -->
        <div class="col-md-4">
          <label for="searchInput" class="form-label">Search</label>
          <input
            id="searchInput"
            v-model="filters.search"
            type="text"
            class="form-control"
            placeholder="Search in descriptions..."
          >
        </div>
        
        <!-- Action Type -->
        <div class="col-md-4">
          <label for="actionTypeSelect" class="form-label">Action Type</label>
          <select
            id="actionTypeSelect"
            v-model="filters.action_type"
            class="form-select"
          >
            <option value="">All Actions</option>
            <option
              v-for="type in actionTypes"
              :key="type.value"
              :value="type.value"
            >
              {{ type.text }}
            </option>
          </select>
        </div>
        
        <!-- Date Range -->
        <div class="col-md-4">
          <label for="startDateInput" class="form-label">Start Date</label>
          <input
            id="startDateInput"
            v-model="filters.start_date"
            type="date"
            class="form-control"
          >
        </div>
        
        <div class="col-md-4">
          <label for="endDateInput" class="form-label">End Date</label>
          <input
            id="endDateInput"
            v-model="filters.end_date"
            type="date"
            class="form-control"
          >
        </div>
        
        <!-- Filter Buttons -->
        <div class="col-md-4 d-flex align-items-end">
          <div class="button-group">
            <button type="submit" class="btn btn-primary">Apply Filters</button>
            <button type="button" @click="resetFilters" class="btn btn-outline-secondary ms-2">
              Reset
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AuditLogFilters',
  props: {
    actionTypes: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      filters: {
        search: '',
        action_type: '',
        start_date: '',
        end_date: ''
      }
    };
  },
  methods: {
    applyFilters() {
      this.$emit('filter-changed', { ...this.filters });
    },
    resetFilters() {
      this.filters = {
        search: '',
        action_type: '',
        start_date: '',
        end_date: ''
      };
      this.$emit('filter-changed', { ...this.filters });
    }
  }
};
</script>

<style scoped>
.audit-log-filters {
  margin-bottom: 20px;
}

.button-group {
  padding-bottom: 6px;
}
</style>
