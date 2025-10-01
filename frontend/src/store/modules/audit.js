import auditService from '@/services/auditService';

const state = {
  auditLogs: [],
  auditLog: null,
  actionTypes: [],
  loading: false,
  error: null,
  pagination: {
    page: 1,
    pageSize: 10,
    totalItems: 0,
    totalPages: 0
  },
  filters: {
    action_type: '',
    user: '',
    search: '',
    start_date: '',
    end_date: ''
  }
};

const getters = {
  getAuditLogs: state => state.auditLogs,
  getAuditLog: state => state.auditLog,
  getActionTypes: state => state.actionTypes,
  isLoading: state => state.loading,
  getError: state => state.error,
  getPagination: state => state.pagination,
  getFilters: state => state.filters
};

const actions = {
  fetchAuditLogs({ commit, state }) {
    commit('SET_LOADING', true);
    
    const params = {
      page: state.pagination.page,
      page_size: state.pagination.pageSize,
      ...state.filters
    };
    
    return auditService.getAuditLogs(params)
      .then(response => {
        commit('SET_AUDIT_LOGS', response.data.results || response.data);
        
        // Handle pagination if API returns it
        if (response.data.count !== undefined) {
          commit('SET_PAGINATION', {
            totalItems: response.data.count,
            totalPages: Math.ceil(response.data.count / state.pagination.pageSize)
          });
        }
        
        commit('SET_LOADING', false);
        commit('SET_ERROR', null);
      })
      .catch(error => {
        commit('SET_LOADING', false);
        commit('SET_ERROR', error.message || 'Failed to fetch audit logs');
        return Promise.reject(error);
      });
  },
  
  fetchAuditLog({ commit }, id) {
    commit('SET_LOADING', true);
    
    return auditService.getAuditLog(id)
      .then(response => {
        commit('SET_AUDIT_LOG', response.data);
        commit('SET_LOADING', false);
        commit('SET_ERROR', null);
      })
      .catch(error => {
        commit('SET_LOADING', false);
        commit('SET_ERROR', error.message || 'Failed to fetch audit log details');
        return Promise.reject(error);
      });
  },
  
  loadActionTypes({ commit }) {
    const actionTypes = auditService.getActionTypes();
    commit('SET_ACTION_TYPES', actionTypes);
  },
  
  updateFilters({ commit, dispatch }, filters) {
    commit('SET_FILTERS', filters);
    commit('SET_PAGE', 1); // Reset to first page when filters change
    return dispatch('fetchAuditLogs');
  },
  
  updatePage({ commit, dispatch }, page) {
    commit('SET_PAGE', page);
    return dispatch('fetchAuditLogs');
  }
};

const mutations = {
  SET_AUDIT_LOGS(state, auditLogs) {
    state.auditLogs = auditLogs;
  },
  
  SET_AUDIT_LOG(state, auditLog) {
    state.auditLog = auditLog;
  },
  
  SET_ACTION_TYPES(state, actionTypes) {
    state.actionTypes = actionTypes;
  },
  
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  
  SET_ERROR(state, error) {
    state.error = error;
  },
  
  SET_PAGE(state, page) {
    state.pagination.page = page;
  },
  
  SET_PAGINATION(state, pagination) {
    state.pagination = {
      ...state.pagination,
      ...pagination
    };
  },
  
  SET_FILTERS(state, filters) {
    state.filters = {
      ...state.filters,
      ...filters
    };
  },
  
  RESET_FILTERS(state) {
    state.filters = {
      action_type: '',
      user: '',
      search: '',
      start_date: '',
      end_date: ''
    };
    state.pagination.page = 1;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
