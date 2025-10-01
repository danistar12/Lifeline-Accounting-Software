import apiClient from '@/services/apiClient';

/**
 * Service for interacting with the audit logs API
 */
export default {
  /**
   * Get a list of audit logs with optional filters
   * @param {Object} params - Query parameters
   * @param {Number} params.page - Page number for pagination
   * @param {Number} params.pageSize - Number of items per page
   * @param {String} params.action_type - Filter by action type
   * @param {String} params.user - Filter by user ID
   * @param {String} params.company - Filter by company ID
   * @param {String} params.search - Search term for filtering
   * @param {String} params.start_date - Filter by start date (YYYY-MM-DD)
   * @param {String} params.end_date - Filter by end date (YYYY-MM-DD)
   * @returns {Promise} Promise resolving to audit log list response
   */
  getAuditLogs(params = {}) {
    return apiClient.get('/audit/', { params });
  },

  /**
   * Get a single audit log by ID
   * @param {Number} id - The audit log ID
   * @returns {Promise} Promise resolving to audit log detail
   */
  getAuditLog(id) {
    return apiClient.get(`/audit/${id}/`);
  },

  /**
   * Get available action types for filtering
   * @returns {Array} Array of action types
   */
  getActionTypes() {
    return [
      { value: 'create', text: 'Create' },
      { value: 'update', text: 'Update' },
      { value: 'delete', text: 'Delete' },
      { value: 'login', text: 'Login' },
      { value: 'logout', text: 'Logout' },
      { value: 'view', text: 'View' },
      { value: 'export', text: 'Export' },
      { value: 'import', text: 'Import' },
      { value: 'other', text: 'Other' },
    ];
  }
};
