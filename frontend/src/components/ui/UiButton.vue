<template>
  <button
    :class="buttonClass"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="spinner"></span>
    <span v-if="icon && !loading" class="btn-icon" aria-hidden="true">{{ icon }}</span>
    <span class="btn-label"><slot /></span>
  </button>
</template>

<script>
export default {
  name: 'UiButton',
  props: {
    variant: {
      type: String,
      default: 'primary'
    },
    size: {
      type: String,
      default: 'md'
    },
    disabled: Boolean,
    loading: Boolean,
    icon: String
  },
  computed: {
    buttonClass() {
      return [
        'ui-button',
        `ui-button--${this.variant}`,
        `ui-button--${this.size}`,
        {
          'is-loading': this.loading,
          'is-disabled': this.disabled || this.loading
        }
      ]
    }
  }
}
</script>

<style scoped>
.ui-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition-base),
    border-color var(--transition-base),
    color var(--transition-base),
    box-shadow var(--transition-base);
  font-size: 0.95rem;
}

.ui-button--md {
  padding: 10px 18px;
}

.ui-button--sm {
  padding: 6px 12px;
  font-size: 0.85rem;
}

.ui-button--lg {
  padding: 14px 22px;
  font-size: 1rem;
}

.ui-button--primary {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
}

.ui-button--primary:hover:not(.is-disabled) {
  background: var(--color-primary-hover);
}

.ui-button--secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border-color: var(--color-border);
}

.ui-button--secondary:hover:not(.is-disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.ui-button--outline {
  background: transparent;
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.ui-button--outline:hover:not(.is-disabled) {
  background: rgba(37, 99, 235, 0.08);
}

.ui-button--ghost {
  background: transparent;
  color: var(--color-text);
}

.ui-button--ghost:hover:not(.is-disabled) {
  background: rgba(15, 23, 42, 0.05);
}

.ui-button--danger {
  background: var(--color-danger);
  color: var(--color-text-inverse);
}

.ui-button--danger:hover:not(.is-disabled) {
  background: #b91c1c;
}

.is-disabled {
  cursor: not-allowed;
  opacity: 0.6;
  box-shadow: none;
}

.spinner {
  width: 16px;
  height: 16px;
  border-radius: 9999px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: rgba(255, 255, 255, 0.9);
  animation: spin 0.9s linear infinite;
}

.ui-button--secondary .spinner,
.ui-button--ghost .spinner,
.ui-button--outline .spinner {
  border-color: rgba(37, 99, 235, 0.2);
  border-top-color: rgba(37, 99, 235, 0.9);
}

.btn-label {
  display: inline-flex;
  align-items: center;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
