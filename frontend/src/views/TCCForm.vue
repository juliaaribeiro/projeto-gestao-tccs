<template>
  <section class="card">
    <h3 class="section-title">
      <span>➕</span> Novo TCC
    </h3>

    <div class="alert">
      Digite o nome do aluno e dos professores. Se algum nome ainda não estiver
      cadastrado, os campos extras necessários vão aparecer automaticamente.
    </div>

    <div v-if="successMessage" class="success-message">
        {{ successMessage }}
    </div>

    <form class="form-grid form-two-col" @submit.prevent="onSubmit">

      <!-- Campos básicos -->
      <label class="col-span-2">
        Título
        <input v-model="form.titulo" required />
      </label>

      <label class="col-span-2">
        Resumo
        <textarea v-model="form.resumo" required />
      </label>

      <label class="col-span-2">
        Palavras-chave
        <input v-model="form.palavras_chave" required />
      </label>

      <label>
        Tipo
        <select v-model="form.tipo" required>
          <option disabled value="">Selecione</option>
          <option v-for="opt in tipoOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </label>

      <label>
        Idioma
        <select v-model="form.idioma" required>
          <option disabled value="">Selecione</option>
          <option v-for="opt in idiomaOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </label>

      <label>
        Semestre de Defesa
        <select v-model="form.semestre_letivo_defesa" required>
          <option disabled value="">Selecione</option>
          <option v-for="s in semestreOptions" :key="s" :value="s">
            {{ s }}
          </option>
        </select>
      </label>

      <label>
        Status inicial
        <select v-model="form.status" required>
          <option disabled value="">Selecione</option>
          <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </label>

      <!-- Pessoas -->
      <PersonPicker
        ref="alunoPicker"
        label="Aluno"
        tipo="aluno"
        v-model="form.aluno"
        :opcoes="alunos"
        :cursos="cursos"
      />

      <PersonPicker
        ref="orientadorPicker"
        label="Orientador"
        tipo="professor"
        v-model="form.orientador"
        :opcoes="professores"
        :departamentos="departamentos"
      />

      <PersonPicker
        ref="coorientadorPicker"
        label="Coorientador (opcional)"
        tipo="professor"
        v-model="form.coorientador"
        :opcoes="professores"
        :departamentos="departamentos"
      />

      <PersonPicker
        ref="presidentePicker"
        label="Presidente da Banca"
        tipo="professor"
        v-model="form.presidente"
        :opcoes="professores"
        :departamentos="departamentos"
      />

      <PersonPicker
        ref="membro1Picker"
        label="1º Membro da Banca"
        tipo="professor"
        v-model="form.primeiro_membro"
        :opcoes="professores"
        :departamentos="departamentos"
      />

      <PersonPicker
        ref="membro2Picker"
        label="2º Membro da Banca"
        tipo="professor"
        v-model="form.segundo_membro"
        :opcoes="professores"
        :departamentos="departamentos"
      />

      <!-- Arquivo -->
      <label class="col-span-2">
        Arquivo PDF
        <input type="file" accept="application/pdf" @change="handleFileUpload" />
      </label>

     <button
        class="primary-button col-span-2"
        type="submit"
        :disabled="submitting"
        >
        {{ submitting ? 'Salvando...' : '✓ Cadastrar TCC' }}
     </button>

     <button
        type="button"
        class="primary-button col-span-2"
        @click="goBack"
        >
        ← Voltar
     </button>

    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import PersonPicker from '../components/PersonPicker.vue'
import { fetchList, postItem } from '../services/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  alunos: Array,
  professores: Array,
  cursos: Array,
  departamentos: Array,
})

const emit = defineEmits(['success'])

/* mensagem */
const successMessage = ref('')

/* form */
const form = ref({
  titulo: '',
  resumo: '',
  palavras_chave: '',
  tipo: '',
  idioma: '',
  semestre_letivo_defesa: '',
  aluno: '',
  orientador: '',
  coorientador: '',
  presidente: '',
  primeiro_membro: '',
  segundo_membro: '',
  status: '0',
})

const file = ref(null)
const submitting = ref(false)

/* options */
const tipoOptions = [
  { value: 'MONOGRAFIA', label: 'Monografia' },
  { value: 'RELATORIO_ESTAGIO', label: 'Relatório de Estágio' },
  { value: 'RELATORIO_TECNICO', label: 'Relatório Técnico' },
  { value: 'ARTIGO', label: 'Artigo' },
]

const idiomaOptions = [
  { value: 'PT', label: 'Português' },
  { value: 'EN', label: 'Inglês' },
]

const statusOptions = [
  { value: '0', label: 'Em Elaboração' },
  { value: '1', label: 'Enviado' },
  { value: '2', label: 'Aprovado' },
  { value: '3', label: 'Reprovado' },
]

const semestreOptions = [
  '2022/1','2022/2','2023/1','2023/2',
  '2024/1','2024/2','2025/1','2025/2',
  '2026/1','2026/2',
]

/* pickers */
const alunoPicker = ref(null)
const orientadorPicker = ref(null)
const coorientadorPicker = ref(null)
const presidentePicker = ref(null)
const membro1Picker = ref(null)
const membro2Picker = ref(null)

/* file */
const handleFileUpload = (e) => {
  file.value = e.target.files[0] || null
}

/* reset */
const resetForm = () => {
  form.value = {
    titulo: '',
    resumo: '',
    palavras_chave: '',
    tipo: '',
    idioma: '',
    semestre_letivo_defesa: '',
    aluno: '',
    orientador: '',
    coorientador: '',
    presidente: '',
    primeiro_membro: '',
    segundo_membro: '',
    status: '0',
  }
}

/* voltar */
const goBack = () => {
  router.push('/tccs')
}

/* submit */
const onSubmit = async () => {
  submitting.value = true

  try {
    const [alunoId, orientadorId, presidenteId, m1, m2] = await Promise.all([
      alunoPicker.value.confirmar(),
      orientadorPicker.value.confirmar(),
      presidentePicker.value.confirmar(),
      membro1Picker.value.confirmar(),
      membro2Picker.value.confirmar(),
    ])

    const coorientadorId =
      coorientadorPicker.value?.query
        ? await coorientadorPicker.value.confirmar()
        : ''

    form.value.aluno = alunoId
    form.value.orientador = orientadorId
    form.value.coorientador = coorientadorId
    form.value.presidente = presidenteId
    form.value.primeiro_membro = m1
    form.value.segundo_membro = m2

    const fd = new FormData()
    Object.entries(form.value).forEach(([k, v]) => {
      if (v !== '' && v !== null) fd.append(k, v)
    })

    if (file.value) fd.append('arquivo', file.value)

    await postItem('/tccs/', fd, true)

    successMessage.value = 'TCC cadastrado com sucesso!'

    emit('success')

    resetForm()
    file.value = null

    alunoPicker.value?.limpar()
    orientadorPicker.value?.limpar()
    coorientadorPicker.value?.limpar()
    presidentePicker.value?.limpar()
    membro1Picker.value?.limpar()
    membro2Picker.value?.limpar()

  } catch (err) {
    console.error(err)
    alert('Erro ao cadastrar TCC')
  } finally {
    submitting.value = false
  }
}
</script>