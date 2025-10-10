<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Projects</h1>
        <p class="page-subtitle">Track project progress, budgets, and client relationships.</p>
      </div>
      <div class="toolbar-group">
        <div class="toolbar-search">
          <UiFormField label="Search">
            <input
              v-model="searchTerm"
              type="search"
              placeholder="Search projects..."
              @input="filterProjects"
            />
          </UiFormField>
        </div>
        <UiFormField label="Status">
          <select v-model="statusFilter" @change="filterProjects">
            <option value="all">All projects</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
            <option value="on-hold">On hold</option>
          </select>
        </UiFormField>
        <UiButton icon="+" variant="primary" @click="openCreate">
          New project
        </UiButton>
      </div>
    </header>

    <UiCard title="Project list" subtitle="Manage your active and completed projects.">
      <template #actions>
        <span class="table-meta">{{ filteredProjects.length }} projects</span>
      </template>

      <div v-if="loading" class="table-empty">Loading projects…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="filteredProjects.length" class="table-container">
        <table class="data-table projects-table">
          <thead>
            <tr>
              <th>Project name</th>
              <th>Customer</th>
              <th>Start date</th>
              <th>End date</th>
              <th class="is-numeric">Budget</th>
              <th>Status</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in filteredProjects" :key="project.id">
              <td>
                <div class="project-name">{{ project.project_name }}</div>
                <div class="project-meta">{{ project.description || 'No description' }}</div>
              </td>
              <td>{{ project.customer?.name || '—' }}</td>
              <td>{{ formatDate(project.start_date) }}</td>
              <td>{{ formatDate(project.end_date) }}</td>
              <td class="is-numeric">{{ formatCurrency(project.budget) }}</td>
              <td>
                <UiStatusBadge :status="statusVariant(project.status)">
                  {{ project.status }}
                </UiStatusBadge>
              </td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editProject(project)">
                  Edit
                </UiButton>
                <UiButton size="sm" variant="danger" @click="deleteProject(project.id)">
                  Delete
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No projects match your filters.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save project"
      :primary-loading="saving"
      @primary="save"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Project name" required>
            <input v-model="form.project_name" required />
          </UiFormField>
          <UiFormField label="Customer">
            <input v-model="form.customer_name" placeholder="Client name" />
          </UiFormField>
          <UiFormField label="Start date">
            <input v-model="form.start_date" type="date" />
          </UiFormField>
          <UiFormField label="End date">
            <input v-model="form.end_date" type="date" />
          </UiFormField>
          <UiFormField label="Budget" hint="Optional project budget">
            <input v-model.number="form.budget" type="number" step="0.01" min="0" />
          </UiFormField>
          <UiFormField label="Status">
            <select v-model="form.status">
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="on-hold">On hold</option>
            </select>
          </UiFormField>
        </div>
        <UiFormField label="Description">
          <textarea v-model="form.description" rows="3" placeholder="Project details..." />
        </UiFormField>
      </form>
    </UiModal>
  </div>
</template>

<script>
import projectsService from '@/services/projectsService';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';
import UiStatusBadge from '@/components/ui/UiStatusBadge.vue';

export default {
  name: 'ProjectsView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
    UiStatusBadge,
  },
  data() {
    return {
      projects: [],
      filteredProjects: [],
      searchTerm: '',
      statusFilter: 'all',
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    modalTitle() {
      return this.form.id ? 'Edit project' : 'New project';
    },
  },
  async mounted() {
    await this.fetchProjects();
  },
  methods: {
    defaultForm() {
      return {
        id: null,
        project_name: '',
        customer_name: '',
        start_date: '',
        end_date: '',
        budget: null,
        status: 'active',
        description: '',
      };
    },
    async fetchProjects() {
      this.loading = true;
      this.error = '';
      try {
        const response = await projectsService.getProjects();
        const payload = Array.isArray(response) ? response : response.data || [];
        this.projects = payload.map((project) => ({
          ...project,
          id: project.id ?? project.project_id,
        }));
        this.filteredProjects = [...this.projects];
      } catch (error) {
        console.error('Error fetching projects:', error);
        this.error = 'Unable to load projects right now.';
      } finally {
        this.loading = false;
      }
    },
    filterProjects() {
      let filtered = [...this.projects];

      // Filter by status
      if (this.statusFilter !== 'all') {
        filtered = filtered.filter((project) =>
          project.status?.toLowerCase() === this.statusFilter.toLowerCase()
        );
      }

      // Filter by search term
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter((project) =>
          project.project_name?.toLowerCase().includes(term) ||
          project.customer_name?.toLowerCase().includes(term) ||
          project.description?.toLowerCase().includes(term)
        );
      }

      this.filteredProjects = filtered;
    },
    openCreate() {
      this.form = this.defaultForm();
      this.showModal = true;
    },
    editProject(project) {
      this.form = {
        id: project.id,
        project_name: project.project_name || '',
        customer_name: project.customer_name || '',
        start_date: project.start_date || '',
        end_date: project.end_date || '',
        budget: project.budget ?? null,
        status: project.status || 'active',
        description: project.description || '',
      };
      this.showModal = true;
    },
    async deleteProject(projectId) {
      if (!projectId) return;

      const confirmed = window.confirm('Delete this project? This action cannot be undone.');
      if (!confirmed) return;

      try {
        await projectsService.deleteProject(projectId);
        this.projects = this.projects.filter((project) => project.id !== projectId);
        this.filterProjects();
      } catch (error) {
        console.error('Error deleting project:', error);
        this.error = 'Unable to delete that project.';
      }
    },
    async save() {
      if (!this.form.project_name) {
        return;
      }

      this.saving = true;
      const payload = {
        project_name: this.form.project_name,
        customer_name: this.form.customer_name || undefined,
        start_date: this.form.start_date || undefined,
        end_date: this.form.end_date || undefined,
        budget: this.form.budget ?? undefined,
        status: this.form.status,
        description: this.form.description || undefined,
      };

      try {
        if (this.form.id) {
          await projectsService.updateProject(this.form.id, payload);
        } else {
          await projectsService.createProject(payload);
        }

        await this.fetchProjects();
        this.showModal = false;
        this.form = this.defaultForm();
      } catch (error) {
        console.error('Error saving project:', error);
        this.error = 'Unable to save that project.';
      } finally {
        this.saving = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '—';
      return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(dateString));
    },
    formatCurrency(amount) {
      if (amount == null || amount === '') return '—';
      return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(amount);
    },
    statusVariant(status) {
      if (!status) return 'info';
      const variants = {
        active: 'success',
        completed: 'info',
        'on-hold': 'warning',
      };
      return variants[status.toLowerCase()] || 'info';
    },
  },
};
</script>

<style scoped>
.toolbar-search :deep(.ui-form-field) {
  min-width: 220px;
}

.toolbar-group :deep(.ui-form-field) {
  min-width: 140px;
}

.projects-table .actions-col {
  width: 160px;
}

.project-name {
  font-weight: 600;
  color: var(--color-text);
}

.project-meta {
  color: var(--color-text-muted);
  font-size: 0.82rem;
  margin-top: 4px;
}

.table-empty--error {
  color: var(--color-danger);
}

.form-grid {
  display: grid;
  gap: 16px;
}

.modal-form {
  padding-top: 4px;
}

@media (min-width: 640px) {
  .form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
