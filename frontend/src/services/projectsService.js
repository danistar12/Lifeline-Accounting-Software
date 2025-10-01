import apiClient from './apiClient';

class ProjectsService {
  // Project endpoints
  async getProjects() {
    const response = await apiClient.get('/projects/projects/');
    return response.data;
  }

  async getProject(id) {
    const response = await apiClient.get(`/projects/projects/${id}/`);
    return response.data;
  }

  async createProject(projectData) {
    const response = await apiClient.post('/projects/projects/', projectData);
    return response.data;
  }

  async updateProject(id, projectData) {
    const response = await apiClient.put(`/projects/projects/${id}/`, projectData);
    return response.data;
  }

  async deleteProject(id) {
    const response = await apiClient.delete(`/projects/projects/${id}/`);
    return response.data;
  }

  // Time Entry endpoints
  async getTimeEntries(projectId = null) {
    const url = projectId ? `/projects/time-entries/?project=${projectId}` : '/projects/time-entries/';
    const response = await apiClient.get(url);
    return response.data;
  }

  async getTimeEntry(id) {
    const response = await apiClient.get(`/projects/time-entries/${id}/`);
    return response.data;
  }

  async createTimeEntry(timeEntryData) {
    const response = await apiClient.post('/projects/time-entries/', timeEntryData);
    return response.data;
  }

  async updateTimeEntry(id, timeEntryData) {
    const response = await apiClient.put(`/projects/time-entries/${id}/`, timeEntryData);
    return response.data;
  }

  async deleteTimeEntry(id) {
    const response = await apiClient.delete(`/projects/time-entries/${id}/`);
    return response.data;
  }
}

export default new ProjectsService();
