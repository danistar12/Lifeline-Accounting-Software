
<template>
  <div class="page-shell">
    <header class="page-toolbar">
      <div>
        <h1 class="page-title">Subscriptions</h1>
        <p class="page-subtitle">Manage customer subscriptions and plans.</p>
      </div>
      <div class="toolbar-group">
        <UiButton icon="+" variant="primary" @click="openCreate">New subscription</UiButton>
      </div>
    </header>

    <UiCard title="Subscriptions" subtitle="Active and historical customer subscriptions.">
      <template #actions>
        <UiButton size="sm" variant="secondary" :loading="loading" @click="fetchSubscriptions">Refresh</UiButton>
      </template>

      <div v-if="loading" class="table-empty">Loading subscriptions…</div>
      <div v-else-if="error" class="table-empty table-empty--error">{{ error }}</div>
      <div v-else-if="subscriptions.length" class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Customer</th>
              <th>Plan</th>
              <th>Billing Cycle</th>
              <th>Renewal Date</th>
              <th>Status</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sub in subscriptions" :key="sub.SubscriptionID || sub.subscription_id">
              <td>{{ sub.CustomerID?.Name || sub.customer?.name || sub.customer_name || '—' }}</td>
              <td>{{ sub.PlanName || sub.plan_name }}</td>
              <td>{{ sub.BillingCycle || sub.billing_cycle }}</td>
              <td>{{ formatDate(sub.RenewalDate || sub.renewal_date) }}</td>
              <td>{{ sub.Status || sub.status }}</td>
              <td class="actions-col">
                <UiButton size="sm" variant="ghost" @click="editSubscription(sub)">Edit</UiButton>
                <UiButton size="sm" variant="danger" @click="deleteSubscription(sub.SubscriptionID || sub.subscription_id)">Delete</UiButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="table-empty">No subscriptions found.</div>
    </UiCard>

    <UiModal
      v-model="showModal"
      :title="modalTitle"
      primary-label="Save subscription"
      :primary-loading="saving"
      @primary="saveSubscription"
    >
      <form class="modal-form" @submit.prevent>
        <div class="form-grid">
          <UiFormField label="Customer" required>
            <input v-model="form.customer_name" required placeholder="Customer name" />
          </UiFormField>
          <UiFormField label="Plan name" required>
            <input v-model="form.plan_name" required placeholder="Plan name" />
          </UiFormField>
        </div>
        <UiFormField label="Billing cycle" required>
          <input v-model="form.billing_cycle" required placeholder="Monthly/Annual" />
        </UiFormField>
        <UiFormField label="Renewal date" required>
          <input v-model="form.renewal_date" required type="date" />
        </UiFormField>
        <UiFormField label="Status" required>
          <select v-model="form.status" required>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </UiFormField>
      </form>
    </UiModal>
  </div>
</template>

<script>
import axios from 'axios';
import UiButton from '@/components/ui/UiButton.vue';
import UiCard from '@/components/ui/UiCard.vue';
import UiModal from '@/components/ui/UiModal.vue';
import UiFormField from '@/components/ui/UiFormField.vue';
import { normalizeArray } from '@/services/normalizeApi.js';

export default {
  name: 'SubscriptionsView',
  components: { UiButton, UiCard, UiModal, UiFormField },
  data() {
    return {
      subscriptions: [],
      loading: false,
      error: '',
      showModal: false,
      modalTitle: 'New Subscription',
      saving: false,
      form: {
        customer_name: '',
        plan_name: '',
        billing_cycle: '',
        renewal_date: '',
        status: 'Active',
      },
      editingId: null,
    };
  },
  methods: {
    async fetchSubscriptions() {
      this.loading = true;
      this.error = '';
      try {
        const res = await axios.get('/api/subscriptions/', {
          headers: { 'X-Company-ID': this.$store.state.company?.id }
        });
        this.subscriptions = normalizeArray(res.data);
      } catch (err) {
        this.error = err?.response?.data?.detail || 'Failed to load subscriptions.';
      } finally {
        this.loading = false;
      }
    },
    openCreate() {
      this.form = {
        customer_name: '',
        plan_name: '',
        billing_cycle: '',
        renewal_date: '',
        status: 'Active',
      };
      this.editingId = null;
      this.modalTitle = 'New Subscription';
      this.showModal = true;
    },
    editSubscription(sub) {
      this.form = {
        customer_name: sub.CustomerID?.Name || sub.customer?.name || sub.customer_name || '',
        plan_name: sub.PlanName || sub.plan_name || '',
        billing_cycle: sub.BillingCycle || sub.billing_cycle || '',
        renewal_date: sub.RenewalDate || sub.renewal_date || '',
        status: sub.Status || sub.status || 'Active',
      };
      this.editingId = sub.SubscriptionID || sub.subscription_id;
      this.modalTitle = 'Edit Subscription';
      this.showModal = true;
    },
    async saveSubscription() {
      this.saving = true;
      try {
        const payload = { ...this.form };
        let res;
        if (this.editingId) {
          res = await axios.put(`/api/subscriptions/${this.editingId}/`, payload, {
            headers: { 'X-Company-ID': this.$store.state.company?.id }
          });
        } else {
          res = await axios.post('/api/subscriptions/', payload, {
            headers: { 'X-Company-ID': this.$store.state.company?.id }
          });
        }
        this.showModal = false;
        this.fetchSubscriptions();
      } catch (err) {
        this.error = err?.response?.data?.detail || 'Failed to save subscription.';
      } finally {
        this.saving = false;
      }
    },
    async deleteSubscription(id) {
      if (!confirm('Delete this subscription?')) return;
      try {
        await axios.delete(`/api/subscriptions/${id}/`, {
          headers: { 'X-Company-ID': this.$store.state.company?.id }
        });
        this.fetchSubscriptions();
      } catch (err) {
        this.error = err?.response?.data?.detail || 'Failed to delete subscription.';
      }
    },
    formatDate(date) {
      if (!date) return '—';
      return new Date(date).toLocaleDateString();
    },
  },
  mounted() {
    this.fetchSubscriptions();
  },
};
</script>

<style scoped>
.page-shell { padding: 2rem; }
.page-toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.page-title { font-size: 2rem; font-weight: 700; }
.page-subtitle { color: #666; margin-top: 0.25rem; }
.toolbar-group { display: flex; gap: 1rem; }
.table-container { margin-top: 1rem; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.75rem 1rem; border-bottom: 1px solid #eee; }
.actions-col { width: 120px; text-align: right; }
.table-empty { padding: 2rem; text-align: center; color: #888; }
.table-empty--error { color: #c00; }
.modal-form { display: flex; flex-direction: column; gap: 1rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
</style>
