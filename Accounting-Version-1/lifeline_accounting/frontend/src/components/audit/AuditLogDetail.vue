<template>
  <div class="audit-log-detail">
    <div class="modal fade show" tabindex="-1" style="display: block;">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Audit Log Details</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="close"></button>
          </div>
          
          <div class="modal-body">
            <div v-if="loading" class="text-center p-5">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            
            <div v-else-if="error" class="alert alert-danger">
              {{ error }}
            </div>
            
            <div v-else-if="!auditLog" class="alert alert-info">
              Log details not found.
            </div>
            
            <div v-else>
              <!-- Basic Information -->
              <div class="card mb-3">
                <div class="card-body">
                  <h6 class="card-subtitle mb-2 text-muted">Basic Information</h6>
                  
                  <dl class="row mb-0">
                    <dt class="col-sm-3">Timestamp</dt>
                    <dd class="col-sm-9">{{ formatDate(auditLog.timestamp) }}</dd>
                    
                    <dt class="col-sm-3">User</dt>
                    <dd class="col-sm-9">
                      {{ auditLog.user_name || (auditLog.user ? auditLog.user.username : 'System') }}
                    </dd>
                    
                    <dt class="col-sm-3">Company</dt>
                    <dd class="col-sm-9">{{ auditLog.company.name }}</dd>
                    
                    <dt class="col-sm-3">Action</dt>
                    <dd class="col-sm-9">
                      <span :class="getActionBadgeClass(auditLog.action_type)">
                        {{ formatActionType(auditLog.action_type) }}
                      </span>
                    </dd>
                    
                    <dt class="col-sm-3">Description</dt>
                    <dd class="col-sm-9">{{ auditLog.action_description }}</dd>
                    
                    <dt class="col-sm-3">Entity Type</dt>
                    <dd class="col-sm-9">{{ auditLog.model_name || 'N/A' }}</dd>
                    
                    <dt class="col-sm-3">Entity ID</dt>
                    <dd class="col-sm-9">{{ auditLog.object_id || 'N/A' }}</dd>
                    
                    <dt class="col-sm-3">IP Address</dt>
                    <dd class="col-sm-9">{{ auditLog.ip_address || 'N/A' }}</dd>
                  </dl>
                </div>
              </div>
              
              <!-- Changes -->
              <div v-if="auditLog.changes && auditLog.changes.length > 0" class="card mb-3">
                <div class="card-body">
                  <h6 class="card-subtitle mb-3 text-muted">Changes</h6>
                  
                  <div class="table-responsive">
                    <table class="table table-sm table-bordered">
                      <thead class="table-light">
                        <tr>
                          <th>Field</th>
                          <th>Before</th>
                          <th>After</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(change, index) in auditLog.changes" :key="index">
                          <td><strong>{{ change.field }}</strong></td>
                          <td><code>{{ formatValue(change.before) }}</code></td>
                          <td><code>{{ formatValue(change.after) }}</code></td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <!-- Additional Details -->
              <div v-if="auditLog.details" class="card mb-3">
                <div class="card-body">
                  <h6 class="card-subtitle mb-2 text-muted">Additional Details</h6>
                  <pre class="details-pre">{{ auditLog.details }}</pre>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="close">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'AuditLogDetail',
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  computed: {
    ...mapState('audit', ['auditLog', 'loading', 'error'])
  },
  methods: {
    ...mapActions('audit', ['fetchAuditLog']),
    close() {
      this.$emit('close');
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).format(date);
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
    formatValue(value) {
      if (value === null || value === undefined) {
        return 'null';
      }
      
      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2);
      }
      
      return String(value);
    }
  },
  watch: {
    id: {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchAuditLog(newId);
        }
      }
    }
  }
};
</script>

<style scoped>
.modal-backdrop {
  z-index: 1040;
}

.modal {
  z-index: 1050;
  background-color: rgba(0, 0, 0, 0.5);
}

dt {
  font-weight: 600;
}

.details-pre {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 10px;
  font-size: 0.85rem;
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
}

.badge {
  font-weight: normal;
  padding: 4px 8px;
}

code {
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
