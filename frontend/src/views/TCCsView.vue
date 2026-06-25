<template>
  <div class="tccs-page">

    <!-- Page header -->
    <div class="page-header card">
      <div>
        <h1 class="page-title">Controle de TCCs</h1>
        <p class="page-subtitle">Cadastre novos trabalhos, altere status e acesse os arquivos PDF.</p>
      </div>
    </div>

    <div class="tccs-layout">

      <!-- ── Form ── -->
      <section class="card form-section">
        <h3 class="section-title">
          <span>➕</span> Novo TCC
        </h3>
        <div class="alert">
          Digite o nome do aluno e dos professores. Se algum nome ainda não estiver
          cadastrado, os campos extras necessários vão aparecer automaticamente.
        </div>

        <form class="form-grid form-two-col" @submit.prevent="createTCC">
          <label class="col-span-2">
            Título
            <input v-model="form.titulo" required placeholder="Título do trabalho de conclusão de curso" />
          </label>

          <label class="col-span-2">
            Resumo
            <textarea v-model="form.resumo" required placeholder="Descreva brevemente o trabalho..." />
          </label>

          <label class="col-span-2">
            Palavras-chave
            <input v-model="form.palavras_chave" required placeholder="Ex: inteligência artificial, machine learning" />
          </label>

          <label>
            Tipo
            <select v-model="form.tipo" required>
              <option disabled value="">Selecione</option>
              <option v-for="opt in tipoOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </label>

          <label>
            Idioma
            <select v-model="form.idioma" required>
              <option disabled value="">Selecione</option>
              <option v-for="opt in idiomaOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </label>

          <label>
            Semestre de Defesa
            <select v-model="form.semestre_letivo_defesa" required>
              <option disabled value="">Selecione</option>
              <option v-for="s in semestreOptions" :key="s" :value="s">{{ s }}</option>
            </select>
          </label>

          <label>
            Status inicial
            <select v-model="form.status" required>
              <option disabled value="">Selecione</option>
              <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </label>

          <!-- ── Pessoas (texto livre, maiúsculas, criação automática) ── -->
          <PersonPicker
            ref="alunoPicker"
            label="Aluno"
            tipo="aluno"
            v-model="form.aluno"
            :opcoes="alunos"
            :cursos="cursos"
            placeholder="Nome do aluno"
          />

          <PersonPicker
            ref="orientadorPicker"
            label="Orientador"
            tipo="professor"
            v-model="form.orientador"
            :opcoes="professores"
            :departamentos="departamentos"
            placeholder="Nome do orientador"
          />

          <PersonPicker
            ref="coorientadorPicker"
            label="Coorientador (opcional)"
            tipo="professor"
            v-model="form.coorientador"
            :opcoes="professores"
            :departamentos="departamentos"
            placeholder="Nome do coorientador"
          />

          <PersonPicker
            ref="presidentePicker"
            label="Presidente da Banca"
            tipo="professor"
            v-model="form.presidente"
            :opcoes="professores"
            :departamentos="departamentos"
            placeholder="Nome do presidente"
          />

          <PersonPicker
            ref="membro1Picker"
            label="1º Membro da Banca"
            tipo="professor"
            v-model="form.primeiro_membro"
            :opcoes="professores"
            :departamentos="departamentos"
            placeholder="Nome do 1º membro"
          />

          <PersonPicker
            ref="membro2Picker"
            label="2º Membro da Banca"
            tipo="professor"
            v-model="form.segundo_membro"
            :opcoes="professores"
            :departamentos="departamentos"
            placeholder="Nome do 2º membro"
          />

          <label class="col-span-2">
            Arquivo PDF
            <input type="file" accept="application/pdf" @change="handleFileUpload" />
          </label>

          <button class="primary-button col-span-2" type="submit" :disabled="submitting">
            {{ submitting ? '⏳ Salvando...' : '✓ Cadastrar TCC' }}
          </button>
        </form>
      </section>

      <!-- ── List ── -->
      <section class="card list-section">
        <div class="list-header">
          <h3 class="section-title">
            <span>📋</span> Lista de TCCs
          </h3>
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
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tcc in tccs" :key="tcc.id">
                <td class="tcc-title-cell">{{ tcc.titulo }}</td>
                <td>{{ alunoMap[tcc.aluno] || tcc.aluno }}</td>
                <td>{{ professorMap[tcc.orientador] || tcc.orientador }}</td>
                <td>
                  <div class="status-cell">
                    <span :class="['badge', statusClass(tcc.status)]">
                      {{ tcc.status_display || statusLabel(tcc.status) }}
                    </span>
                    <select class="status-select" v-model="editStatus[tcc.id]">
                      <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
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
                    rel="noopener noreferrer"
                    class="pdf-link"
                  >
                    📥 PDF
                  </a>
                  <span v-else>
                    —
                  </span>
                </td>
                <td>
                  <button class="secondary-button" @click="updateStatus(tcc)">Salvar</button>
                </td>
              </tr>
              <tr v-if="tccs.length === 0">
                <td colspan="6" class="center-cell">
                  <div class="empty-state">
                    <span>📭</span>
                    <span>Nenhum TCC cadastrado.</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { fetchList, patchItem, postItem } from '../services/api'
import PersonPicker from '../components/PersonPicker.vue'

export default {
  components: { PersonPicker },
  setup() {
    const tccs          = ref([])
    const alunos        = ref([])
    const professores   = ref([])
    const cursos         = ref([])
    const departamentos  = ref([])
    const alunoMap      = ref({})
    const professorMap  = ref({})
    const editStatus    = ref({})
    const file           = ref(null)
    const submitting     = ref(false)

    // Refs dos PersonPickers — usados pra confirmar/criar a pessoa antes de enviar o TCC
    const alunoPicker        = ref(null)
    const orientadorPicker    = ref(null)
    const coorientadorPicker  = ref(null)
    const presidentePicker    = ref(null)
    const membro1Picker       = ref(null)
    const membro2Picker       = ref(null)

    const statusOptions = [
      { value: '0', label: 'Em Elaboração' },
      { value: '1', label: 'Enviado'       },
      { value: '2', label: 'Aprovado'      },
      { value: '3', label: 'Reprovado'     },
    ]

    const tipoOptions = [
      { value: 'MONOGRAFIA',        label: 'Monografia'           },
      { value: 'RELATORIO_ESTAGIO', label: 'Relatório de Estágio' },
      { value: 'RELATORIO_TECNICO', label: 'Relatório Técnico'    },
      { value: 'ARTIGO',            label: 'Artigo'               },
    ]

    const idiomaOptions = [
      { value: 'PT', label: 'Português' },
      { value: 'EN', label: 'Inglês'    },
    ]

    const semestreOptions = [
      '2022/1','2022/2','2023/1','2023/2','2024/1','2024/2','2025/1','2025/2','2026/1','2026/2',
    ]

    const emptyForm = () => ({
      titulo: '', resumo: '', palavras_chave: '',
      tipo: '', idioma: '', semestre_letivo_defesa: '',
      aluno: '', orientador: '', coorientador: '',
      presidente: '', primeiro_membro: '', segundo_membro: '',
      status: '0',
    })

    const form = ref(emptyForm())

    /* ── Loaders ── */
    const loadAuxiliaryData = async () => {
      const [ar, pr, cr, dr] = await Promise.all([
        fetchList('/alunos/'), fetchList('/professores/'),
        fetchList('/cursos/'), fetchList('/departamentos/'),
      ])
      alunos.value       = ar.results || ar
      professores.value  = pr.results || pr
      cursos.value        = cr.results || cr
      departamentos.value = dr.results || dr
      alunoMap.value     = alunos.value.reduce((acc, a) => { acc[a.id] = `${a.nome} (${a.matricula})`; return acc }, {})
      professorMap.value = professores.value.reduce((acc, p) => { acc[p.id] = p.nome; return acc }, {})
    }

    const loadTCCs = async () => {
      try {
        const res   = await fetchList('/tccs/')
        tccs.value  = res.results || res
        tccs.value.forEach(t => { editStatus.value[t.id] = String(t.status) })
      } catch (e) { console.error('Erro ao carregar TCCs', e) }
    }

    onMounted(() => Promise.all([loadAuxiliaryData(), loadTCCs()]))

    /* ── Actions ── */
    const handleFileUpload = (e) => { file.value = e.target.files[0] || null }

    const createTCC = async () => {
      submitting.value = true
      try {
        // Confirma/cria cada pessoa antes de montar o payload do TCC.
        // Coorientador é opcional: só confirma se algo foi digitado.
        const [alunoId, orientadorId, presidenteId, membro1Id, membro2Id] = await Promise.all([
          alunoPicker.value.confirmar(),
          orientadorPicker.value.confirmar(),
          presidentePicker.value.confirmar(),
          membro1Picker.value.confirmar(),
          membro2Picker.value.confirmar(),
        ])
        const coorientadorId = coorientadorPicker.value.query
          ? await coorientadorPicker.value.confirmar()
          : ''

        if (!alunoId || !orientadorId || !presidenteId || !membro1Id || !membro2Id) {
          window.alert('Preencha todos os nomes obrigatórios (aluno, orientador e banca completa).')
          return
        }

        form.value.aluno = alunoId
        form.value.orientador = orientadorId
        form.value.coorientador = coorientadorId
        form.value.presidente = presidenteId
        form.value.primeiro_membro = membro1Id
        form.value.segundo_membro = membro2Id

        const fd = new FormData()
        Object.entries(form.value).forEach(([k, v]) => {
          if (v !== '' && v !== null) fd.append(k, v)
        })
        if (file.value) fd.append('arquivo', file.value)

        await postItem('/tccs/', fd, true)
        await Promise.all([loadTCCs(), loadAuxiliaryData()])

        form.value = emptyForm()
        file.value = null
        ;[alunoPicker, orientadorPicker, coorientadorPicker, presidentePicker, membro1Picker, membro2Picker]
          .forEach(p => p.value && p.value.limpar())

        window.alert('TCC cadastrado com sucesso! ✓')
      } catch (e) {
        console.error(e)
        const msg = e.response?.data?.erro || 'Falha ao cadastrar TCC. Verifique os dados.'
        window.alert(msg)
      } finally {
        submitting.value = false
      }
    }

    const updateStatus = async (tcc) => {
      try {
        await patchItem(`/tccs/${tcc.id}/`, { status: editStatus.value[tcc.id] })
        await loadTCCs()
      } catch (e) {
        console.error(e)
        window.alert('Não foi possível atualizar o status.')
      }
    }

    const fileUrl = (path) => path ? `http://127.0.0.1:8000${path}` : ''

    const statusClass = (s) => {
      switch (String(s)) {
        case '2': return 'badge--approved'
        case '1': return 'badge--sent'
        case '3': return 'badge--rejected'
        default:  return 'badge--draft'
      }
    }

    const statusLabel = (s) =>
      statusOptions.find(o => o.value === String(s))?.label || s

    return {
      tccs, alunos, professores, cursos, departamentos, form,
      statusOptions, tipoOptions, idiomaOptions, semestreOptions,
      editStatus, alunoMap, professorMap, submitting,
      alunoPicker, orientadorPicker, coorientadorPicker, presidentePicker, membro1Picker, membro2Picker,
      handleFileUpload, createTCC, updateStatus,
      fileUrl, statusClass, statusLabel,
    }
  },
}
</script>

<style scoped>
.tccs-page { display: flex; flex-direction: column; gap: 22px; }

/* ── Page header ── */
.page-header {
  background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(6,182,212,0.07));
  border-color: rgba(99,102,241,0.2);
}
.page-title    { font-size: 1.5rem; font-weight: 800; color: var(--text-1); margin-bottom: 4px; }
.page-subtitle { font-size: 0.9rem; color: var(--text-2); }

/* ── Layout ── */
.tccs-layout {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 22px;
  align-items: start;
}

@media (max-width: 1100px) { .tccs-layout { grid-template-columns: 1fr; } }

/* ── Section titles ── */
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-1);
  margin-bottom: 18px;
}

.form-section  { display: flex; flex-direction: column; }
.list-section  { display: flex; flex-direction: column; gap: 16px; }

.list-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.list-header .section-title { margin-bottom: 0; }

.entity-count {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-3);
  background: var(--surface-2);
  border: 1px solid var(--border);
  padding: 2px 10px;
  border-radius: 999px;
}

/* ── Status cell ── */
.status-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.status-select {
  background: var(--surface-2);
  border: 1px solid var(--border-hover);
  border-radius: var(--radius-s);
  color: var(--text-1);
  padding: 4px 8px;
  font-size: 0.8rem;
  outline: none;
  max-width: 140px;
}
.status-select:focus { border-color: var(--indigo); }

/* ── Table cells ── */
.tcc-title-cell {
  max-width: 240px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-1);
}

.file-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--cyan);
  font-size: 0.85rem;
  font-weight: 600;
  transition: color 0.15s;
}
.file-link:hover { color: var(--indigo); }

.no-file { color: var(--text-3); font-size: 0.9rem; }

.center-cell { text-align: center; padding: 36px !important; }
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: var(--text-3);
  font-size: 0.9rem;
}
</style>