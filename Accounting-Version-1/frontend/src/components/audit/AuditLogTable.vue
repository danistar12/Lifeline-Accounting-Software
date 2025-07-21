<template>
  <div class="audit-log-table">
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th scope="col">Time</th>
            <th scope="col">User</th>
            <th scope="col">Action</th>
            <th scope="col">Description</th>
            <th scope="col">IP Address</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ formatDate(log.timestamp) }}</td>
            <td>{{ getUserName(log) }}</td>
            <td>
              <span :class="getActionBadgeClass(log.action_type)">
                {{ formatActionType(log.action_type) }}
              </span>
            </td>
            <td>{{ log.action_description }}</td>
            <td>{{ log.ip_address || 'N/A' }}</td>
            <td>
              <button 
                class="btn btn-sm btn-outline-primary" 
                @click="viewDetails(log.id)"
              >
                Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuditLogTable',
  props: {
    logs: {
      type: Array,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    getUserName(log) {
      if (log.user) {
        return log.user_name || log.user.username;
      }
      return 'System';
    },
    formatActionType(actionType) {
      return actionType.charAt(0).toUpperCase() + actionType.slice(1);
    },
    getActionBadgeClass(actionType) {
      const classes = {
        create: 'badge bg-success',
        update: 'badge bg-primary',
        delete: 'badge bg-danger',
        login: 'badge bg-info',
        logout: 'badge bg-secondary',
        view: 'badge bg-light text-dark',
        export: 'badge bg-warning text-dark',
        import: 'badge bg-warning text-dark',
        other: 'badge bg-secondary'
      };
      return classes[actionType] || classes.other;
    },
    viewDetails(id) {
      this.$emit('view-details', id);
    }
  }
};
</script>

<style scoped>
.audit-log-table {
  font-size: 0.9rem;
}

th {
  white-space: nowrap;
}

.badge {
  font-weight: normal;
  padding: 4px 8px;
}
</style>
