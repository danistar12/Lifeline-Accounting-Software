<template>
  <div class="projects-container">
    <h1 class="page-title">Projects</h1>
    
    <div class="toolbar">
      <button class="btn btn-primary">New Project</button>
      <div class="filters">
        <input type="text" placeholder="Search projects..." class="search-input" />
        <select class="filter-select">
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
              <th>Client</th>
              <th>Start Date</th>
              <th>Due Date</th>
              <th>Budget</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- Database fields from Project model will populate here -->
            <!-- project_id, name, client_id, start_date, end_date, budget, status -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectsView',
  data() {
    return {
      projects: [] // Will be populated from API
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
</style>
