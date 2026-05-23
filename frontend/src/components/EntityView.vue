<template>
  <section class="card entity-card">

    <div class="entity-header">
      <div class="entity-title-group">
        <h2 class="entity-title">{{ title }}</h2>
        <span v-if="items.length" class="entity-count">{{ items.length }} registros</span>
      </div>
      <div class="search-wrap">
        <span class="search-icon-prefix">🔍</span>
        <input
          class="search-input search-input--prefixed"
          v-model="query"
          @input="fetchData"
          :placeholder="`Buscar ${title.toLowerCase()}...`"
        />
      </div>
    </div>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td :colspan="columns.length" class="center-cell">
              <span class="loading-text">Carregando...</span>
            </td>
          </tr>

          <template v-else>
            <tr v-for="item in items" :key="item.id">
              <td v-for="col in columns" :key="col.key">
                <template v-if="col.key === 'status'">
                  <span :class="['badge', statusClass(item[col.key])]">
                    {{ item.status_display || item[col.key] }}
                  </span>
                </template>
                <template v-else-if="relatedMaps[col.key]">
                  {{ relatedMaps[col.key][item[col.key]] || item[col.key] }}
                </template>
                <template v-else>{{ item[col.key] }}</template>
              </td>
            </tr>

            <tr v-if="items.length === 0">
              <td :colspan="columns.length" class="center-cell">
                <div class="empty-state">
                  <span class="empty-icon">🔎</span>
                  <span>Nenhum registro encontrado</span>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

  </section>
</template>

<script>
import { ref, watchEffect } from 'vue'
import { fetchList } from '../services/api'

export default {
  props: {
    title:       { type: String,  required: true },
    apiPath:     { type: String,  required: true },
    columns:     { type: Array,   required: true },
    relatedMaps: { type: Object,  default: () => ({}) },
    searchField: { type: String,  default: '' },
  },

  setup(props) {
    const items   = ref([])
    const query   = ref('')
    const loading = ref(false)

    const fetchData = async () => {
      loading.value = true
      try {
        const params = props.searchField && query.value ? { search: query.value } : {}
        const res    = await fetchList(props.apiPath, params)
        items.value  = res.results || res
      } catch (e) {
        console.error('Erro ao carregar dados:', e)
        items.value = []
      } finally {
        loading.value = false
      }
    }

    watchEffect(fetchData)

    const statusClass = (s) => {
      switch (String(s)) {
        case '2': return 'badge--approved'
        case '1': return 'badge--sent'
        case '3': return 'badge--rejected'
        default:  return 'badge--draft'
      }
    }

    return { items, query, loading, fetchData, statusClass }
  },
}
</script>

<style scoped>
.entity-card { display: flex; flex-direction: column; gap: 20px; }

.entity-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.entity-title-group { display: flex; align-items: baseline; gap: 10px; }

.entity-title { font-size: 1.1rem; font-weight: 700; color: var(--text-1); }

.entity-count {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-3);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 2px 10px;
  border-radius: 999px;
}

.search-wrap { position: relative; display: flex; align-items: center; }

.search-icon-prefix {
  position: absolute;
  left: 12px;
  font-size: 0.88rem;
  pointer-events: none;
  line-height: 1;
}

.search-input--prefixed { padding-left: 36px; min-width: 240px; }

.center-cell { text-align: center; padding: 40px 16px !important; }

.loading-text { color: var(--text-3); font-size: 0.9rem; }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: var(--text-3);
  font-size: 0.9rem;
}
.empty-icon { font-size: 2rem; }
</style>
