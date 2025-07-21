<template>
  <div class="audit-logs">
    <div class="page-header">
      <h1>Audit Logs</h1>
      <p class="subtitle">View the history of user actions in the system</p>
    </div>
    
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Filters</h5>
        <AuditLogFilters 
          @filter-changed="onFilterChanged" 
          :actionTypes="actionTypes" 
        />
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="d-flex justify-content-center my-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        
        <div v-else-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
        
        <div v-else-if="auditLogs.length === 0" class="alert alert-info" role="alert">
          No audit logs found matching your criteria.
        </div>
        
        <div v-else>
          <AuditLogTable :logs="auditLogs" @view-details="viewLogDetails" />
          
          <!-- Pagination -->
          <nav aria-label="Audit logs pagination" class="mt-4">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: pagination.page === 1 }">
                <a class="page-link" href="#" @click.prevent="goToPage(pagination.page - 1)">
                  Previous
                </a>
              </li>
              
              <li 
                v-for="pageNum in paginationRange" 
                :key="pageNum" 
                class="page-item"
                :class="{ active: pageNum === pagination.page }"
              >
                <a class="page-link" href="#" @click.prevent="goToPage(pageNum)">
                  {{ pageNum }}
                </a>
              </li>
              
              <li class="page-item" :class="{ disabled: pagination.page === pagination.totalPages }">
                <a class="page-link" href="#" @click.prevent="goToPage(pagination.page + 1)">
                  Next
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
    
    <!-- Log Details Modal -->
    <AuditLogDetail
      v-if="selectedLogId"
      :id="selectedLogId"
      @close="selectedLogId = null"
    />
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import AuditLogFilters from '@/components/audit/AuditLogFilters.vue';
import AuditLogTable from '@/components/audit/AuditLogTable.vue';
import AuditLogDetail from '@/components/audit/AuditLogDetail.vue';

export default {
  name: 'AuditLogList',
  components: {
    AuditLogFilters,
    AuditLogTable,
    AuditLogDetail
  },
  data() {
    return {
      selectedLogId: null
    };
  },
  computed: {
    ...mapState('audit', [
      'auditLogs',
      'loading',
      'error',
      'filters',
      'pagination',
      'actionTypes'
    ]),
    ...mapGetters('audit', [
      'getPagination',
      'getFilters'
    ]),
    paginationRange() {
      const totalPages = this.pagination.totalPages || 1;
      const currentPage = this.pagination.page;
      const range = [];
      
      // Calculate range of pages to show (max 5)
      const maxPages = 5;
      let startPage = Math.max(1, currentPage - Math.floor(maxPages / 2));
      let endPage = startPage + maxPages - 1;
      
      if (endPage > totalPages) {
        endPage = totalPages;
        startPage = Math.max(1, endPage - maxPages + 1);
      }
      
      for (let i = startPage; i <= endPage; i++) {
        range.push(i);
      }
      
      return range;
    }
  },
  methods: {
    ...mapActions('audit', [
      'fetchAuditLogs',
      'updateFilters',
      'updatePage',
      'loadActionTypes'
    ]),
    onFilterChanged(filters) {
      this.updateFilters(filters);
    },
    goToPage(page) {
      if (page < 1 || page > this.pagination.totalPages) return;
      this.updatePage(page);
    },
    viewLogDetails(logId) {
      this.selectedLogId = logId;
    }
  },
  created() {
    this.loadActionTypes();
    this.fetchAuditLogs();
  }
};
</script>

<style scoped>
.audit-logs {
  padding: 20px;
}

.page-header {
  margin-bottom: 25px;
}

.subtitle {
  color: #6c757d;
}
</style>
