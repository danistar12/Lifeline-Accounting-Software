<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Vendors</h1>
        <p class="page-subtitle">Manage suppliers and vendor contacts.</p>
      </div>
      <div class="toolbar-group">
        <UiButton icon="+" variant="primary" @click="openCreate">New vendor</UiButton>
      </div>
    </header>

    <UiCard title="Vendors" subtitle="List of vendors for the selected company.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchVendors">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading vendors…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="vendors.length" class="table-container">
        <table class="data-table vendors-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vendor in vendors" :key="vendor.VendorID">
              <td>{{ vendor.Name }}</td>
              <td>{{ vendor.Email || '—' }}</td>
              <td>{{ vendor.Phone || '—' }}</td>
              <td>{{ vendor.Address || '—' }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editVendor(vendor)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteVendor(vendor.VendorID)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No vendors found.</div>
    </UiCard>

    <UiModal v-model="showModal" :title="modalTitle" primary-label="Save vendor" :primary-loading="saving" @primary="save">
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Name" required>
            <input v-model="form.Name" required />
          </UiFormField>
          <UiFormField label="Email">
            <input v-model="form.Email" type="email" />
          </UiFormField>
          <UiFormField label="Phone">
            <input v-model="form.Phone" type="tel" />
          </UiFormField>
        </div>
        <UiFormField label="Address">
          <textarea v-model="form.Address" rows="2" placeholder="Street address..." />
        </UiFormField>
        <UiFormField label="Notes">
          <textarea v-model="form.VendorNotes" rows="3" placeholder="Additional notes..." />
        </UiFormField>
      </form>
    </UiModal>
  </div>
</template>

<script>
import VendorsService from '@/services/vendorsService';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import UiModal from '@/components/ui/UiModal.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'VendorsView',
  components: { UiButton, UiCard, UiFormField, UiModal },
  data() {
    return {
      vendors: [],
      loading: false,
      saving: false,
      error: '',
      showModal: false,
      form: this.defaultForm(),
    };
  },
  computed: {
    ...mapGetters(['selectedCompanyId']),
    modalTitle() {
      return this.form.VendorID ? 'Edit vendor' : 'New vendor';
    },
  },
  mounted() {
    this.fetchVendors();
  },
  methods: {
    defaultForm() {
      return { VendorID: null, CompanyID: this.selectedCompanyId ? Number(this.selectedCompanyId) : null, Name: '', Email: '', Phone: '', Address: '', PaymentTerms: '', VendorNotes: '' };
    },
    openCreate() {
      this.form = this.defaultForm();
      this.showModal = true;
    },
    async fetchVendors() {
      this.loading = true;
      this.error = '';
      try {
        const response = await VendorsService.getVendors();
        const vendorsList = Array.isArray(response) ? response : response || [];
        // Filter out vendors with no name or empty name
        this.vendors = vendorsList.filter(vendor => vendor.Name && vendor.Name.trim() !== '');
        console.log('Filtered vendors:', this.vendors);
      } catch (err) {
        console.error('Error fetching vendors:', err);
        this.error = 'Unable to load vendors right now.';
      } finally {
        this.loading = false;
      }
    },
    editVendor(vendor) { this.form = { ...vendor, VendorID: vendor.VendorID ?? vendor.vendor_id ?? null }; this.showModal = true; },
    async deleteVendor(id) { if (!confirm('Delete this vendor?')) return; try { await VendorsService.deleteVendor(id); this.fetchVendors(); } catch (err) { console.error('Error deleting vendor:', err); alert('Failed to delete vendor.'); } },
    async save() {
      if (this.saving) return; // Prevent double submission
      this.saving = true;
      try {
        const payload = { ...this.form };
        if (!payload.CompanyID && this.selectedCompanyId) payload.CompanyID = Number(this.selectedCompanyId);
        const { VendorID, ...body } = payload;
        if (VendorID) await VendorsService.updateVendor(VendorID, body);
        else await VendorsService.createVendor(body);
        this.showModal = false;
        await this.fetchVendors();
      } catch (err) {
        console.error('Error saving vendor:', err);
        alert('Failed to save vendor.');
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
@media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } }
</style>
