<template>
  <section :class="cardClass">
    <header v-if="hasHeader" class="ui-card__header">
      <div class="ui-card__titles">
        <slot name="title">
          <h3 v-if="title" class="ui-card__title">{{ title }}</h3>
        </slot>
        <p v-if="subtitle" class="ui-card__subtitle">{{ subtitle }}</p>
      </div>
      <div class="ui-card__actions">
        <slot name="actions" />
      </div>
    </header>

    <div class="ui-card__body" :style="bodyPadding">
      <slot />
    </div>

    <footer v-if="$slots.footer" class="ui-card__footer">
      <slot name="footer" />
    </footer>
  </section>
</template>

<script>
export default {
  name: 'UiCard',
  props: {
    title: String,
    subtitle: String,
    padding: {
      type: String,
      default: '24px'
    },
    variant: {
      type: String,
      default: 'default'
    }
  },
  computed: {
    bodyPadding() {
      return { padding: this.padding }
    },
    hasHeader() {
      return this.title || this.subtitle || this.$slots.title || this.$slots.actions
    },
    cardClass() {
      return ['ui-card', `ui-card--${this.variant}`]
    }
  }
}
</script>

<style scoped>
.ui-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  border: 1px solid rgba(209, 213, 219, 0.4);
  display: flex;
  flex-direction: column;
}

.ui-card--muted {
  background: var(--color-surface-muted);
  box-shadow: none;
}

.ui-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
}

.ui-card__title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--color-text);
}

.ui-card__subtitle {
  margin: 6px 0 0;
  color: var(--color-text-muted);
  font-size: 0.95rem;
}

.ui-card__actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.ui-card__body {
  width: 100%;
}

.ui-card__footer {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-surface-muted);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}
</style>
