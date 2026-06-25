<template>
  <div class="theme-picker">

    <button
      v-for="s in swatches"
      :key="s.key"
      class="theme-btn"
      :class="{ active: current === s.key }"
      :title="s.label"
      :aria-label="s.label"
      @click="pick(s.key)"
    >
      {{ s.icon }} {{ s.label }}
    </button>
  </div>
</template>

<script>
import { ref, watchEffect } from 'vue'

const STORAGE_KEY = 'tcc-theme'

export default {
  setup() {
    const saved = localStorage.getItem(STORAGE_KEY) || 'light'
    const current = ref(saved)

    const swatches = [
      {
        key: 'light',
        label: 'Claro'
      },
      {
        key: 'dark',
        label: 'Escuro'
      }
    ]

    const pick = (key) => {
      current.value = key
      localStorage.setItem(STORAGE_KEY, key)
    }

    watchEffect(() => {
      document.documentElement.setAttribute(
        'data-theme',
        current.value
      )
    })

    return {
      current,
      swatches,
      pick
    }
  }
}
</script>

<style scoped>
.theme-picker {
  display: flex;
  align-items: center;
  gap: 8px;
}

.theme-picker__label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-2);
}

.theme-btn {
  display: flex;
  align-items: center;
  gap: 6px;

  padding: 6px 12px;

  border: 1px solid var(--border);
  border-radius: var(--radius-m);

  background: var(--surface);
  color: var(--text-1);

  font-size: 0.85rem;
  font-weight: 600;

  cursor: pointer;

  transition: all 0.2s ease;
}

.theme-btn:hover {
  background: var(--primary-pale);
  border-color: var(--primary);
}

.theme-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}
</style>