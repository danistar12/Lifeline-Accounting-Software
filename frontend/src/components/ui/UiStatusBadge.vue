<template>
  <span :class="badgeClass">
    <slot>{{ label }}</slot>
  </span>
</template>

<script>
export default {
  name: 'UiStatusBadge',
  props: {
    status: {
      type: String,
      default: 'info'
    },
    label: String
  },
  computed: {
    badgeClass() {
      return ['ui-status-badge', `ui-status-badge--${this.status}`]
    }
  }
}
</script>

<style scoped>
.ui-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.ui-status-badge--info {
  background: rgba(37, 99, 235, 0.12);
  color: var(--color-primary);
}

.ui-status-badge--success {
  background: rgba(5, 150, 105, 0.12);
  color: var(--color-success);
}

.ui-status-badge--warning {
  background: rgba(245, 158, 11, 0.12);
  color: var(--color-warning);
}

.ui-status-badge--danger {
  background: rgba(220, 38, 38, 0.12);
  color: var(--color-danger);
}
</style>
