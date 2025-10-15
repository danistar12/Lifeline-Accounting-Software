<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Import Files</h1>
        <p class="page-subtitle">Upload and manage data import files.</p>
      </div>
      <div class="toolbar-group">
        <UiButton variant="primary" @click="openUpload">
          Upload File
        </UiButton>
      </div>
    </header>

    <UiCard title="Import History" subtitle="List of uploaded import files and their processing status.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchImports">
          Refresh
        </UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading imports…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="imports.length" class="table-container">
        <table class="data-table imports-table">
          <thead>
            <tr>
              <th>File Name</th>
              <th>Import Type</th>
              <th>Status</th>
              <th>Uploaded</th>
              <th>Records</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="imp in imports" :key="imp.id">
              <td>{{ imp.file_name }}</td>
              <td>{{ imp.import_type }}</td>
              <td>
                <UiStatusBadge :status="getStatusVariant(imp.status)">
                  {{ imp.status }}
                </UiStatusBadge>
              </td>
              <td>{{ formatDate(imp.uploaded_at) }}</td>
              <td>{{ imp.processed_records || '—' }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="viewDetails(imp)">
                  Details
                </UiButton>
                <UiButton
                  v-if="imp.status === 'completed'"
                  size="sm"
                  variant="outline"
                  @click="downloadReport(imp)"
                >
                  Report
                </UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No import files found.</div>
    </UiCard>

    <UiModal
      v-model="showUploadModal"
      title="Upload Import File"
      primary-label="Upload"
      :primary-loading="uploading"
      @primary="uploadFile"
    >
      <form class="modal-form" @submit.prevent>
        <UiFormField label="Import Type" required>
          <select v-model="uploadForm.import_type" required>
            <option value="">Select type</option>
            <option value="customers">Customers</option>
            <option value="vendors">Vendors</option>
            <option value="invoices">Invoices</option>
            <option value="bills">Bills</option>
            <option value="chart_of_accounts">Chart of Accounts</option>
          </select>
        </UiFormField>
        <UiFormField label="File" required>
          <input
            ref="fileInput"
            type="file"
            accept=".csv,.xlsx,.xls"
            @change="handleFileSelect"
            required
          />
        </UiFormField>
        <p class="help-text">
          Supported formats: CSV, Excel (.xlsx, .xls). Maximum file size: 10MB.
        </p>
      </form>
    </UiModal>
  </div>
</template>

<script>
import axios from 'axios';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';
import UiStatusBadge from '@/components/ui/UiStatusBadge.vue';

export default {
  name: 'ImportFilesView',
  components: {
    UiButton,
    UiCard,
    UiFormField,
    UiModal,
    UiStatusBadge,
  },
  data() {
    return {
      imports: [],
      loading: false,
      uploading: false,
      error: '',
      showUploadModal: false,
      uploadForm: {
        import_type: '',
        file: null,
      },
    };
  },
  mounted() {
    this.fetchImports();
  },
  methods: {
    async fetchImports() {
      this.loading = true;
      this.error = '';
      try {
        const response = await axios.get('/api/importer/');
        this.imports = response.data || [];
      } catch (error) {
        console.error('Error fetching imports:', error);
        this.error = 'Unable to load import files.';
      } finally {
        this.loading = false;
      }
    },
    openUpload() {
      this.uploadForm = { import_type: '', file: null };
      this.showUploadModal = true;
    },
    handleFileSelect(event) {
      this.uploadForm.file = event.target.files[0];
    },
    async uploadFile() {
      if (!this.uploadForm.file || !this.uploadForm.import_type) return;

      this.uploading = true;
      const formData = new FormData();
      formData.append('file', this.uploadForm.file);
      formData.append('import_type', this.uploadForm.import_type);

      try {
        await axios.post('/api/importer/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        this.showUploadModal = false;
        this.fetchImports();
        alert('File uploaded successfully. Processing will begin shortly.');
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Failed to upload file.');
      } finally {
        this.uploading = false;
      }
    },
    viewDetails(imp) {
      // TODO: Show detailed processing results
      console.log('View details:', imp);
    },
    downloadReport(imp) {
      // TODO: Download processing report
      console.log('Download report:', imp);
    },
    formatDate(date) {
      if (!date) return '';
      return new Date(date).toLocaleDateString();
    },
    getStatusVariant(status) {
      switch (status) {
        case 'completed':
          return 'success';
        case 'processing':
          return 'info';
        case 'failed':
          return 'danger';
        default:
          return 'warning';
      }
    },
  },
};
</script>

<style scoped>
.help-text {
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 0.5rem;
}
</style>
