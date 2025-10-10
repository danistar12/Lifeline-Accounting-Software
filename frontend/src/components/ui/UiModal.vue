<template>
  <transition name="fade">
    <div v-if="modelValue" class="ui-modal__backdrop" @click.self="close">
      <div class="ui-modal" :class="`ui-modal--${size}`">
        <header class="ui-modal__header">
          <h3 class="ui-modal__title">{{ title }}</h3>
          <button class="ui-modal__close" @click="close" aria-label="Close">×</button>
        </header>

        <section class="ui-modal__body">
          <slot />
        </section>

        <footer v-if="showFooter" class="ui-modal__footer">
          <UiButton variant="ghost" @click="close">
            {{ dismissLabel }}
          </UiButton>
          <UiButton
            v-if="primaryLabel"
            :variant="primaryVariant"
            :loading="primaryLoading"
            @click="$emit('primary')"
          >
            {{ primaryLabel }}
          </UiButton>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
import UiButton from './UiButton.vue'

export default {
  name: 'UiModal',
  components: { UiButton },
  props: {
    modelValue: Boolean,
    title: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md'
    },
    dismissLabel: {
      type: String,
      default: 'Cancel'
    },
    primaryLabel: String,
    primaryVariant: {
      type: String,
      default: 'primary'
    },
    primaryLoading: Boolean
  },
  emits: ['update:modelValue', 'primary'],
  computed: {
    showFooter() {
      return this.dismissLabel || this.primaryLabel
    }
  },
  methods: {
    close() {
      this.$emit('update:modelValue', false)
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.ui-modal__backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: grid;
  place-items: center;
  z-index: 1200;
  padding: 24px;
}

.ui-modal {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: 0 25px 60px rgba(15, 23, 42, 0.25);
  width: min(640px, 100%);
  max-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.ui-modal--sm {
  width: min(420px, 100%);
}

.ui-modal--lg {
  width: min(860px, 100%);
}

.ui-modal__header,
.ui-modal__footer {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.ui-modal__footer {
  border-bottom: none;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.ui-modal__title {
  margin: 0;
  font-size: 1.2rem;
  color: var(--color-text);
}

.ui-modal__close {
  background: transparent;
  border: none;
  font-size: 1.6rem;
  line-height: 1;
  cursor: pointer;
  color: var(--color-text-muted);
}

.ui-modal__body {
  padding: 24px;
  overflow-y: auto;
}
</style>
