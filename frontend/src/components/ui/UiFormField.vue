<template>
  <label class="ui-form-field" :class="{ 'has-error': error }">
    <div class="ui-form-field__label">
      <span>
        {{ label }}
        <span v-if="required" class="required">*</span>
      </span>
      <slot name="label-extra" />
    </div>
    <div class="ui-form-field__control">
      <slot />
    </div>
    <p v-if="hint && !error" class="helper-text">{{ hint }}</p>
    <p v-if="error" class="error-text">{{ error }}</p>
  </label>
</template>

<script>
export default {
  name: 'UiFormField',
  props: {
    label: {
      type: String,
      required: true
    },
    hint: String,
    error: String,
    required: Boolean
  }
}
</script>

<style scoped>
.ui-form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.ui-form-field__label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text);
  font-weight: 500;
}

.required {
  color: var(--color-danger);
  margin-left: 2px;
}

.ui-form-field__control :deep(input),
.ui-form-field__control :deep(select),
.ui-form-field__control :deep(textarea) {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 0.95rem;
  transition: border-color var(--transition-base), box-shadow var(--transition-base);
}

.ui-form-field__control :deep(input:focus),
.ui-form-field__control :deep(select:focus),
.ui-form-field__control :deep(textarea:focus) {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.has-error :deep(input),
.has-error :deep(select),
.has-error :deep(textarea) {
  border-color: var(--color-danger);
}
</style>
