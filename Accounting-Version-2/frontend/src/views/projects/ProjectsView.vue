<template>
  <div class="projects-container">
    <h1 class="page-title">Projects</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary" @click="showCreateForm = true">New Project</button>
      <div class="filters">
        <input 
          type="text" 
          placeholder="Search projects..." 
          class="search-input" 
          v-model="searchTerm"
          @input="filterProjects"
        />
        <select class="filter-select" v-model="statusFilter" @change="filterProjects">
          <option value="all">All Projects</option>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
          <option value="on-hold">On Hold</option>
        </select>
      </div>
    </div>
    
    <div class="card">
      <div class="card-body">
        <table class="projects-table">
          <thead>
            <tr>
              <th>Project Name</th>
              <th>Customer</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Budget</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in filteredProjects" :key="project.project_id">
              <td>{{ project.name }}</td>
              <td>{{ project.customer_name || 'N/A' }}</td>
              <td>{{ formatDate(project.start_date) }}</td>
              <td>{{ formatDate(project.end_date) }}</td>
              <td>${{ project.budget ? project.budget.toFixed(2) : '0.00' }}</td>
              <td>
                <span :class="getStatusClass(project.status)">
                  {{ project.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline" @click="editProject(project)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteProject(project.project_id)">Delete</button>
              </td>
            </tr>
            <tr v-if="filteredProjects.length === 0">
              <td colspan="7" class="text-center">No projects found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import projectsService from '@/services/projectsService'

export default {
  name: 'ProjectsView',
  data() {
    return {
      projects: [],
      filteredProjects: [],
      searchTerm: '',
      statusFilter: 'all',
      showCreateForm: false,
      loading: false
    }
  },
  async mounted() {
    await this.fetchProjects()
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true
        const response = await projectsService.getProjects()
        this.projects = response.data
        this.filteredProjects = [...this.projects]
      } catch (error) {
        console.error('Error fetching projects:', error)
      } finally {
        this.loading = false
      }
    },
    filterProjects() {
      let filtered = [...this.projects]
      
      // Filter by status
      if (this.statusFilter !== 'all') {
        filtered = filtered.filter(project => 
          project.status.toLowerCase() === this.statusFilter.toLowerCase()
        )
      }
      
      // Filter by search term
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(project => 
          project.name.toLowerCase().includes(term) ||
          (project.customer_name && project.customer_name.toLowerCase().includes(term))
        )
      }
      
      this.filteredProjects = filtered
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    },
    getStatusClass(status) {
      return {
        'status-active': status.toLowerCase() === 'active',
        'status-completed': status.toLowerCase() === 'completed',
        'status-on-hold': status.toLowerCase() === 'on-hold'
      }
    },
    editProject(project) {
      // TODO: Implement edit functionality
      console.log('Edit project:', project)
    },
    async deleteProject(projectId) {
      if (confirm('Are you sure you want to delete this project?')) {
        try {
          await projectsService.deleteProject(projectId)
          await this.fetchProjects() // Refresh the list
        } catch (error) {
          console.error('Error deleting project:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
.projects-container {
  padding: 20px;
}
.page-title {
  font-size: 1.8rem;
  color: #2a5298;
  margin-bottom: 24px;
}
.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.btn-primary {
  background-color: #2a5298;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
}
.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
.filters {
  display: flex;
  gap: 10px;
}
.search-input, .filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.projects-table {
  width: 100%;
  border-collapse: collapse;
}
.projects-table th,
.projects-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.projects-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}
.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}
.btn-sm {
  padding: 4px 8px;
  font-size: 0.875rem;
}
.btn-outline {
  background: white;
  border: 1px solid #2a5298;
  color: #2a5298;
}
.btn-danger {
  background-color: #dc3545;
  color: white;
}
.text-center {
  text-align: center;
}
.status-active {
  color: #28a745;
  font-weight: 600;
}
.status-completed {
  color: #007bff;
  font-weight: 600;
}
.status-on-hold {
  color: #ffc107;
  font-weight: 600;
}
</style>
