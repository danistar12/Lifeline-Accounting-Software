
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
            <input v-model="searchTerm" type="search" placeholder="Search projects..." @input="filterProjects" />
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
        <UiButton icon="+" variant="primary" @click="openCreate">New project</UiButton>
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
                <div class="project-name">{{ project.ProjectName || project.project_name }}</div>
                <div class="project-meta">{{ project.Description || project.description || 'No description' }}</div>
              </td>
              <td>{{ project.CustomerName || project.customer?.name || project.customer_name || '—' }}</td>
              <td>{{ formatDate(project.StartDate || project.start_date) }}</td>
              <td>{{ formatDate(project.EndDate || project.end_date) }}</td>
              <td class="is-numeric">{{ formatCurrency(project.Budget ?? project.budget) }}</td>
              <td>
                <UiStatusBadge :status="statusVariant(project.Status || project.status)">
                  {{ project.Status || project.status }}
                </UiStatusBadge>
              </td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editProject(project)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteProject(project.id)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No projects match your filters.</div>
    </UiCard>

    <UiModal v-model="showModal" :title="modalTitle" primary-label="Save project" :primary-loading="saving" @primary="save">
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Project name" required>
            <input v-model="form.ProjectName" required />
          </UiFormField>
          <UiFormField label="Customer">
            <input v-model="form.CustomerName" placeholder="Client name" />
          </UiFormField>
          <UiFormField label="Start date">
            <input v-model="form.StartDate" type="date" />
          </UiFormField>
          <UiFormField label="End date">
            <input v-model="form.EndDate" type="date" />
          </UiFormField>
          <UiFormField label="Budget" hint="Optional project budget">
            <input v-model.number="form.Budget" type="number" step="0.01" min="0" />
          </UiFormField>
          <UiFormField label="Status">
            <select v-model="form.Status">
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="on-hold">On hold</option>
            </select>
          </UiFormField>
        </div>
        <UiFormField label="Description">
          <textarea v-model="form.Description" rows="3" placeholder="Project details..." />
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
        components: { UiButton, UiCard, UiFormField, UiModal, UiStatusBadge },
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
            return { id: null, ProjectName: '', CustomerName: '', StartDate: '', EndDate: '', Budget: null, Status: 'active', Description: '' };
          },
          async fetchProjects() {
            this.loading = true;
            this.error = '';
            try {
              const response = await projectsService.getProjects();
              const payload = Array.isArray(response) ? response : response.data || [];
              this.projects = payload.map((project) => {
                const normalized = { ...project, id: project.id ?? project.project_id ?? project.ProjectID };
                normalized.ProjectName = project.ProjectName ?? project.project_name;
                normalized.CustomerName = project.CustomerName ?? project.customer?.name ?? project.customer_name ?? (project.CustomerID?.Name);
                normalized.StartDate = project.StartDate ?? project.start_date;
                normalized.EndDate = project.EndDate ?? project.end_date;
                normalized.Budget = project.Budget ?? project.budget;
                normalized.Status = project.Status ?? project.status;
                normalized.Description = project.Description ?? project.description;
                return normalized;
              });
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
            if (this.statusFilter !== 'all') {
              filtered = filtered.filter((project) => (project.Status || project.status || '').toLowerCase() === this.statusFilter.toLowerCase());
            }
            if (this.searchTerm) {
              const term = this.searchTerm.toLowerCase();
              filtered = filtered.filter((project) => (project.ProjectName || project.project_name || '').toLowerCase().includes(term) || (project.CustomerName || project.customer_name || '').toLowerCase().includes(term) || (project.Description || project.description || '').toLowerCase().includes(term));
            }
            this.filteredProjects = filtered;
          },
          openCreate() { this.form = this.defaultForm(); this.showModal = true; },
          editProject(project) { this.form = { id: project.id, ProjectName: project.ProjectName || project.project_name || '', CustomerName: project.CustomerName || project.customer_name || '', StartDate: project.StartDate || project.start_date || '', EndDate: project.EndDate || project.end_date || '', Budget: project.Budget ?? project.budget ?? null, Status: project.Status || project.status || 'active', Description: project.Description || project.description || '' }; this.showModal = true; },
          async deleteProject(projectId) {
            if (!projectId) return;
            if (!window.confirm('Delete this project? This action cannot be undone.')) return;
            try { await projectsService.deleteProject(projectId); this.projects = this.projects.filter((p) => p.id !== projectId); this.filterProjects(); } catch (error) { console.error('Error deleting project:', error); this.error = 'Unable to delete that project.'; }
          },
          async save() {
            if (!this.form.ProjectName) return;
            this.saving = true;
            // send canonical CamelCase plus legacy snake_case for transition
            const payload = {
              ProjectName: this.form.ProjectName,
              CustomerName: this.form.CustomerName || undefined,
              StartDate: this.form.StartDate || undefined,
              EndDate: this.form.EndDate || undefined,
              Budget: this.form.Budget ?? undefined,
              Status: this.form.Status,
              Description: this.form.Description || undefined,
              project_name: this.form.ProjectName,
              customer_name: this.form.CustomerName || undefined,
              start_date: this.form.StartDate || undefined,
              end_date: this.form.EndDate || undefined,
              budget: this.form.Budget ?? undefined,
              status: this.form.Status,
              description: this.form.Description || undefined,
            };
            try { if (this.form.id) await projectsService.updateProject(this.form.id, payload); else await projectsService.createProject(payload); await this.fetchProjects(); this.showModal = false; this.form = this.defaultForm(); } catch (error) { console.error('Error saving project:', error); this.error = 'Unable to save that project.'; } finally { this.saving = false; }
          },
          formatDate(dateString) { if (!dateString) return '—'; return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(dateString)); },
          formatCurrency(amount) { if (amount == null || amount === '') return '—'; return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(amount); },
          statusVariant(status) { if (!status) return 'info'; const variants = { active: 'success', completed: 'info', 'on-hold': 'warning' }; return variants[status.toLowerCase()] || 'info'; },
        },
      };
      </script>

      <style scoped>
      .toolbar-search :deep(.ui-form-field) { min-width: 220px; }
      .toolbar-group :deep(.ui-form-field) { min-width: 140px; }
      .projects-table .actions-col { width: 160px; }
      .project-name { font-weight: 600; color: var(--color-text); }
      .project-meta { color: var(--color-text-muted); font-size: 0.82rem; margin-top: 4px; }
      .table-empty--error { color: var(--color-danger); }
      .form-grid { display: grid; gap: 16px; }
      .modal-form { padding-top: 4px; }
      @media (min-width: 640px) { .form-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
      </style>
              const term = this.searchTerm.toLowerCase();
