<template>
  <div class="tccs-page">

    <!-- Header -->
    <div class="page-header card">
      <div class="header-content">
        <div>
          <h1 class="page-title">Controle de TCCs</h1>
          <p class="page-subtitle">
            Cadastre novos trabalhos, altere status e acesse os arquivos PDF.
          </p>
        </div>

        <button class="primary-button" @click="goToTCCForm">
          + Cadastrar novo TCC
        </button>
      </div>
    </div>

    <!-- Lista -->
    <section class="card list-section">

      <div class="list-header">
        <span class="entity-count">{{ tccs.length }} registros</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Título</th>
              <th>Aluno</th>
              <th>Orientador</th>
              <th>Status</th>
              <th>Arquivo</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="tcc in tccs" :key="tcc.id">

              <td class="tcc-title-cell">{{ tcc.titulo }}</td>
              <td>{{ alunoMap[tcc.aluno] || tcc.aluno }}</td>
              <td>{{ professorMap[tcc.orientador] || tcc.orientador }}</td>

              <!-- STATUS CLICK-TO-EDIT -->
              <td>
                <div class="status-cell">

                  <!-- badge -->
                  <span
                    v-if="editingStatus !== tcc.id"
                    :class="['badge', statusClass(tcc.status)]"
                    @click="openStatus(tcc.id)"
                    style="cursor:pointer"
                  >
                    {{ statusLabel(tcc.status) }}
                  </span>

                  <!-- dropdown -->
                  <select
                    v-else
                    v-model="editStatus[tcc.id]"
                    @change="saveStatus(tcc)"
                    @blur="closeStatus"
                    class="status-select"
                  >
                    <option
                      v-for="opt in statusOptions"
                      :key="opt.value"
                      :value="opt.value"
                    >
                      {{ opt.label }}
                    </option>
                  </select>

                </div>
              </td>

              <td>
                <a
                  v-if="tcc.arquivo"
                  :href="tcc.arquivo"
                  target="_blank"
                  class="pdf-link"
                >
                  📥 PDF
                </a>
                <span v-else>—</span>
              </td>

            </tr>

            <tr v-if="tccs.length === 0">
              <td colspan="5" class="center-cell">
                Nenhum TCC cadastrado.
              </td>
            </tr>

          </tbody>
        </table>
      </div>

    </section>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchList, patchItem } from '../services/api'

export default {
  setup() {
    const router = useRouter()

    const tccs = ref([])
    const alunos = ref([])
    const professores = ref([])

    const alunoMap = ref({})
    const professorMap = ref({})

    const editStatus = ref({})
    const editingStatus = ref(null)

    const statusOptions = [
      { value: '0', label: 'Em Elaboração' },
      { value: '1', label: 'Enviado' },
      { value: '2', label: 'Aprovado' },
      { value: '3', label: 'Reprovado' },
    ]

    const goToTCCForm = () => {
      router.push('/tccs/novo')
    }

    const loadAuxiliaryData = async () => {
      const [ar, pr] = await Promise.all([
        fetchList('/alunos/'),
        fetchList('/professores/'),
      ])

      alunos.value = ar.results || ar
      professores.value = pr.results || pr

      alunoMap.value = Object.fromEntries(
        alunos.value.map(a => [a.id, `${a.nome} (${a.matricula})`])
      )

      professorMap.value = Object.fromEntries(
        professores.value.map(p => [p.id, p.nome])
      )
    }

    const loadTCCs = async () => {
      const res = await fetchList('/tccs/')
      tccs.value = res.results || res

      tccs.value.forEach(t => {
        editStatus.value[t.id] = String(t.status)
      })
    }

    onMounted(async () => {
      await Promise.all([loadAuxiliaryData(), loadTCCs()])
    })

    /* STATUS INLINE */
    const openStatus = (id) => {
      editingStatus.value = id
    }

    const closeStatus = () => {
      editingStatus.value = null
    }

    const saveStatus = async (tcc) => {
      await patchItem(`/tccs/${tcc.id}/`, {
        status: editStatus.value[tcc.id],
      })

      editingStatus.value = null
      await loadTCCs()
    }

    const statusClass = (s) => {
      switch (String(s)) {
        case '2': return 'badge--approved'
        case '1': return 'badge--sent'
        case '3': return 'badge--rejected'
        default: return 'badge--draft'
      }
    }

    const statusLabel = (s) =>
      statusOptions.find(o => o.value === String(s))?.label || s

    return {
      tccs,
      alunoMap,
      professorMap,
      editStatus,
      editingStatus,
      statusOptions,
      goToTCCForm,
      openStatus,
      closeStatus,
      saveStatus,
      statusClass,
      statusLabel,
    }
  },
}
</script>