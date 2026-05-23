<template>
  <section class="chart-card">
    <header class="chart-header">
      <h3 class="chart-title">{{ title }}</h3>
      <span v-if="totalCount" class="chart-total">{{ totalCount }} total</span>
    </header>

    <div class="chart-wrap" :style="{ height: chartHeight }">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <!-- Legend for doughnut -->
    <div v-if="type === 'doughnut' && labels.length" class="doughnut-legend">
      <div v-for="(label, i) in labels" :key="label" class="legend-item">
        <span class="legend-dot" :style="{ background: palette[i % palette.length] }"></span>
        <span class="legend-label">{{ label }}</span>
        <span class="legend-value">
          {{ values[i] }}
          <span class="legend-pct">({{ pct(i) }}%)</span>
        </span>
      </div>
    </div>
  </section>
</template>

<script>
import { Chart, registerables } from 'chart.js'
import { computed, onMounted, ref, watch } from 'vue'

Chart.register(...registerables)

export default {
  props: {
    title:      { type: String,  required: true },
    labels:     { type: Array,   required: true },
    values:     { type: Array,   required: true },
    type:       { type: String,  default: 'bar' },   // 'bar' | 'doughnut'
    horizontal: { type: Boolean, default: false },
  },

  setup(props) {
    const chartCanvas = ref(null)
    let chartInstance = null

    const palette = [
      '#a5b4fc', '#34d399', '#fbbf24', '#fb7185',
      '#67e8f9', '#c084fc', '#86efac', '#fdba74',
      '#6ee7b7', '#f9a8d4',
    ]

    const barColors = [
      'rgba(99,102,241,0.82)', 'rgba(139,92,246,0.82)', 'rgba(6,182,212,0.82)',
      'rgba(16,185,129,0.82)', 'rgba(245,158,11,0.82)', 'rgba(244,63,94,0.75)',
    ]

    const totalCount = computed(() => {
      const s = props.values.reduce((a, b) => a + b, 0)
      return s || null
    })

    const pct = (i) => {
      if (!totalCount.value) return 0
      return Math.round((props.values[i] / totalCount.value) * 100)
    }

    const chartHeight = computed(() => {
      if (props.type === 'doughnut') return '220px'
      if (props.horizontal) return Math.max(240, props.labels.length * 36) + 'px'
      return '260px'
    })

    const renderChart = () => {
      if (!chartCanvas.value) return
      if (chartInstance) { chartInstance.destroy(); chartInstance = null }

      const isDoughnut = props.type === 'doughnut'

      chartInstance = new Chart(chartCanvas.value, {
        type: isDoughnut ? 'doughnut' : 'bar',
        data: {
          labels: props.labels,
          datasets: [{
            label: 'Quantidade',
            data: props.values,
            backgroundColor: isDoughnut
              ? palette.slice(0, props.labels.length)
              : props.horizontal
                ? barColors.map(c => c.replace('0.82)', '0.75)'))
                : barColors,
            borderColor: isDoughnut
              ? palette.slice(0, props.labels.length).map(c => c + '55')
              : 'transparent',
            borderWidth: isDoughnut ? 2 : 0,
            borderRadius: isDoughnut ? 0 : 7,
            maxBarThickness: 44,
            hoverOffset: isDoughnut ? 8 : 0,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: props.horizontal ? 'y' : 'x',
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(10,16,30,0.96)',
              titleColor: '#f0f6ff',
              bodyColor: '#94a3b8',
              borderColor: 'rgba(99,102,241,0.3)',
              borderWidth: 1,
              padding: 12,
              cornerRadius: 10,
              callbacks: {
                label: (ctx) => {
                  if (isDoughnut && totalCount.value) {
                    const p = Math.round((ctx.raw / totalCount.value) * 100)
                    return `  ${ctx.raw} trabalhos  (${p}%)`
                  }
                  return `  ${ctx.raw} trabalhos`
                },
              },
            },
          },
          scales: isDoughnut ? {} : {
            x: {
              ticks: { color: '#4b6080', font: { size: 12 } },
              grid: { display: props.horizontal, color: 'rgba(148,163,184,0.06)' },
              border: { display: false },
            },
            y: {
              beginAtZero: true,
              ticks: { color: '#4b6080', precision: 0, font: { size: 12 } },
              grid: { color: 'rgba(148,163,184,0.06)', display: !props.horizontal },
              border: { display: false },
            },
          },
          cutout: isDoughnut ? '68%' : undefined,
          animation: { duration: 600, easing: 'easeOutQuart' },
        },
      })
    }

    onMounted(renderChart)
    watch(() => [props.labels, props.values], renderChart, { deep: true })

    return { chartCanvas, palette, totalCount, pct, chartHeight }
  },
}
</script>

<style scoped>
.chart-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: border-color 0.2s;
}
.chart-card:hover { border-color: var(--border-hover); }

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.chart-title {
  font-size: 0.93rem;
  font-weight: 700;
  color: var(--text-1);
}

.chart-total {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-3);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 3px 10px;
  border-radius: 999px;
  white-space: nowrap;
}

.chart-wrap { position: relative; }

/* ── Doughnut legend ── */
.doughnut-legend {
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  flex: 1;
  font-size: 0.83rem;
  color: var(--text-2);
}

.legend-value {
  font-size: 0.83rem;
  font-weight: 700;
  color: var(--text-1);
}

.legend-pct {
  font-weight: 400;
  color: var(--text-3);
  margin-left: 3px;
}
</style>
