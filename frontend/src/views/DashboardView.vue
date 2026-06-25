<template>
  <div class="dashboard">

    <!-- Cabeçalho da página -->
    <section class="page-header card">
      <div class="page-header__content">
        <div class="page-header__eyebrow">Visão geral</div>
        <h1 class="page-header__title">Dashboard</h1>
        <p class="page-header__sub">Sistema de Gestão de Trabalhos de Conclusão de Curso</p>
      </div>
      <div class="page-header__meta">
        <span class="page-date">{{ today }}</span>
      </div>
    </section>

    <!-- Stat cards -->
    <div class="stat-cards">
      <div v-for="s in statItems" :key="s.label" class="stat-card">
        <div class="stat-content">
          <div class="stat-label">{{ s.label }}</div>
          <div class="stat-value">{{ s.value ?? '—' }}</div>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <BarChart
        title="TCCs por Status"
        :labels="statusLabels"
        :values="statusValues"
        type="doughnut"
      />
      <BarChart
        title="Top 10 Orientadores"
        :labels="orientadorLabels"
        :values="orientadorValues"
        :horizontal="true"
      />
    </div>

  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import BarChart from '../components/BarChart.vue'
import api, { fetchList } from '../services/api'

export default {
  components: { BarChart },
  setup() {
    const stats  = ref({ total_geral: 0, por_status: {}, por_orientador: {} })
    const counts = ref({ alunos: 0, professores: 0, cursos: 0, departamentos: 0 })

    const today = new Date().toLocaleDateString('pt-BR', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    })

    const loadStats = async () => {
      try {
        const { data } = await api.get('/tccs/estatisticas/')
        stats.value = data
      } catch (e) { console.error('Erro ao carregar estatísticas', e) }
    }

    const loadCounts = async () => {
      try {
        const [a, p, c, d] = await Promise.all([
          fetchList('/alunos/'),
          fetchList('/professores/'),
          fetchList('/cursos/'),
          fetchList('/departamentos/'),
        ])
        counts.value = {
          alunos:        a.count ?? (a.results?.length ?? a.length ?? 0),
          professores:   p.count ?? (p.results?.length ?? p.length ?? 0),
          cursos:        c.count ?? (c.results?.length ?? c.length ?? 0),
          departamentos: d.count ?? (d.results?.length ?? d.length ?? 0),
        }
      } catch (e) { console.error('Erro ao carregar contagens', e) }
    }

    onMounted(() => Promise.all([loadStats(), loadCounts()]))

    const statItems = computed(() => [
      {
        label: 'TCCs', value: stats.value.total_geral,
      },
      {
        label: 'Alunos', value: counts.value.alunos,
      },
      {
        label: 'Professores', value: counts.value.professores,
      },
      {
        label: 'Cursos', value: counts.value.cursos,
      },
      {
        label: 'Departamentos', value: counts.value.departamentos,
      },
    ])

    const statusLabels    = computed(() => Object.keys(stats.value.por_status || {}))
    const statusValues    = computed(() => Object.values(stats.value.por_status || {}))

    const orientadorEntries = computed(() =>
      Object.entries(stats.value.por_orientador || {})
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
    )
    const orientadorLabels = computed(() => orientadorEntries.value.map(([k]) => k))
    const orientadorValues = computed(() => orientadorEntries.value.map(([, v]) => v))

    return {
      stats, counts, statItems, today,
      statusLabels, statusValues,
      orientadorLabels, orientadorValues,
    }
  },
}
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 22px; }

/* ── Page header ── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-left: 4px solid var(--primary);
  border-radius: 0 var(--radius-l) var(--radius-l) 0;
}

.page-header__eyebrow {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--primary);
  margin-bottom: 6px;
}

.page-header__title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-1);
  margin-bottom: 4px;
  letter-spacing: -0.02em;
}

.page-header__sub { color: var(--text-2); font-size: 0.9rem; }

.page-date {
  font-size: 0.78rem;
  color: var(--text-3);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 5px 12px;
  border-radius: 999px;
  white-space: nowrap;
  text-transform: capitalize;
}

/* ── Charts ── */
.charts-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 20px;
  align-items: start;
}

@media (max-width: 920px) {
  .charts-grid { grid-template-columns: 1fr; }
  .page-header__meta { display: none; }
}

.stat-content {
  width: 100%;
  text-align: center;
}

.stat-card {
  justify-content: center;
}

.stat-label {
  font-size: 0.8rem;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 2rem;
}

</style>
