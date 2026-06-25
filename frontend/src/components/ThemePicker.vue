<template>
  <div class="theme-picker">
    <span class="theme-picker__label">Fundo</span>
    <button
      v-for="s in swatches"
      :key="s.key"
      class="theme-picker__swatch"
      :class="{ active: current === s.key }"
      :style="{ background: s.color }"
      :title="s.label"
      :aria-label="'Fundo ' + s.label"
      @click="pick(s.key)"
    />
  </div>
</template>

<script>
import { ref, watchEffect } from 'vue'

const STORAGE_KEY = 'tcc-bg-theme'

export default {
  setup() {
    const saved = localStorage.getItem(STORAGE_KEY) || 'slate'
    const current = ref(saved)

    const swatches = [
      { key: 'white', color: '#ffffff', label: 'Branco'    },
      { key: 'slate', color: '#f4f6f9', label: 'Cinza-azul'},
      { key: 'warm',  color: '#faf8f5', label: 'Creme'     },
      { key: 'blue',  color: '#eef3fa', label: 'Azul claro'},
      { key: 'green', color: '#f0f7f0', label: 'Verde claro'},
      { key: 'stone', color: '#f5f3ef', label: 'Pedra'     },
    ]

    const pick = (key) => {
      current.value = key
      localStorage.setItem(STORAGE_KEY, key)
    }

    watchEffect(() => {
      document.documentElement.setAttribute('data-bg', current.value)
    })

    return { swatches, current, pick }
  },
}
</script>
