<template>
  <svg :class="['ui-icon', sizeClass]" viewBox="0 0 24 24" role="img" aria-hidden="true" v-bind="attrs">
    <component :is="svgComponent" />
  </svg>
</template>

<script>
import { h } from 'vue';

const icons = {
  revenue: () => h('g', [
    h('path', { d: 'M12 2v6l3-1.5L18 10l-6 3-6-3 3-3.5L12 8V2z' })
  ]),
  expenses: () => h('g', [
    h('path', { d: 'M3 13h18v2H3v-2zm0-6h18v2H3V7zm0 12h18v2H3v-2z' })
  ]),
  profit: () => () => h('g', [
    h('path', { d: 'M12 2l4 8h-3v6h-2v-6H8l4-8z' })
  ]),
  cashflow: () => () => h('g', [
    h('path', { d: 'M3 12c3-5 9-5 12 0 3-5 9-5 12 0' })
  ]),
  eye: () => () => h('g', [
    h('path', { d: 'M12 5c-7 0-11 7-11 7s4 7 11 7 11-7 11-7-4-7-11-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8z' })
  ]),
  bolt: () => () => h('g', [
    h('path', { d: 'M13 2L3 14h7l-1 8L21 10h-7l-1-8z' })
  ]),
  clock: () => () => h('g', [
    h('path', { d: 'M12 1a11 11 0 1 0 0 22 11 11 0 0 0 0-22zm1 11h4v2h-6V6h2v6z' })
  ]),
  pending: () => () => h('g', [
    h('path', { d: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 11V7h-2v7h6v-2h-4z' })
  ]),
  chart: () => () => h('g', [
    h('path', { d: 'M3 3v18h18v-2H5V3H3zm6 12h2v-6H9v6zm4 0h2v-9h-2v9z' })
  ]),
  pie: () => () => h('g', [
    h('path', { d: 'M11 2v10H2a10 10 0 1 0 9-10z' })
  ]),
  invoice: () => () => h('g', [
    h('path', { d: 'M6 2h9a2 2 0 0 1 2 2v14l-3-2-3 2-3-2-3 2V4a2 2 0 0 1 2-2z' })
  ]),
  customer: () => () => h('g', [
    h('path', { d: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0 2c-5 0-9 2.5-9 5v1h18v-1c0-2.5-4-5-9-5z' })
  ])
};

export default {
  name: 'UiIcon',
  props: {
    name: { type: String, required: true },
    size: { type: String, default: 'md' }
  },
  computed: {
    svgComponent() {
      const fn = icons[this.name];
      return fn ? fn() : icons['chart']();
    },
    sizeClass() {
      return `ui-icon--${this.size}`;
    },
    attrs() { return {}; }
  }
};
</script>

<style scoped>
.ui-icon { width: 24px; height: 24px; fill: currentColor; display: inline-block; }
.ui-icon--lg { width: 40px; height: 40px; }
.ui-icon--md { width: 28px; height: 28px; }
.ui-icon--sm { width: 18px; height: 18px; }
</style>
