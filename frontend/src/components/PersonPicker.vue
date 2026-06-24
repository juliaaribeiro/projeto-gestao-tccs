<template>
  <div class="person-picker">
    <label>
      {{ label }}
      <div class="picker-input-wrap">
        <input
          v-model="query"
          type="text"
          :placeholder="placeholder"
          autocomplete="off"
          @input="onInput"
          @focus="showList = true"
          @blur="onBlur"
        />
        <span v-if="selectedId" class="picker-check" title="Selecionado">✓</span>
      </div>

      <ul v-if="showList && suggestions.length" class="picker-suggestions">
        <li
          v-for="s in suggestions"
          :key="s.id"
          @mousedown.prevent="selecionar(s)"
        >
          {{ s.nome }}
          <span v-if="tipo === 'aluno'" class="picker-sub">({{ s.matricula }})</span>
        </li>
      </ul>
    </label>

    <!-- Campo extra (curso ou departamento) só aparece quando o nome digitado é novo.
         Também é texto livre — não precisa já estar cadastrado. -->
    <div v-if="isNovo" class="picker-extra">
      <span class="picker-extra-hint">🆕 "{{ query }}" ainda não está cadastrado(a). Preencha para criar:</span>

      <template v-if="tipo === 'aluno'">
        <label>
          Curso
          <div class="picker-input-wrap">
            <input
              v-model="extra.cursoNome"
              type="text"
              placeholder="Digite o curso (ex: Ciência da Computação)"
              autocomplete="off"
              @input="onExtraInput"
              @focus="showExtraList = true"
              @blur="onExtraBlur"
            />
          </div>
          <ul v-if="showExtraList && extraSuggestions.length" class="picker-suggestions">
            <li
              v-for="c in extraSuggestions"
              :key="c.id"
              @mousedown.prevent="selecionarExtra(c)"
            >
              {{ c.nome }}
            </li>
          </ul>
        </label>
        <label>
          Matrícula <span class="picker-optional">(opcional — gerada automaticamente se vazio)</span>
          <input v-model="extra.matricula" placeholder="Ex: 2023012345" />
        </label>
      </template>

      <template v-else>
        <label>
          Departamento
          <div class="picker-input-wrap">
            <input
              v-model="extra.departamentoNome"
              type="text"
              placeholder="Digite o departamento (ex: Ciência da Computação)"
              autocomplete="off"
              @input="onExtraInput"
              @focus="showExtraList = true"
              @blur="onExtraBlur"
            />
          </div>
          <ul v-if="showExtraList && extraSuggestions.length" class="picker-suggestions">
            <li
              v-for="d in extraSuggestions"
              :key="d.id"
              @mousedown.prevent="selecionarExtra(d)"
            >
              {{ d.nome }}
            </li>
          </ul>
        </label>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { postItem } from '../services/api'

export default {
  props: {
    label:    { type: String, required: true },
    tipo:     { type: String, required: true },
    modelValue: { type: [Number, String], default: '' },
    opcoes:   { type: Array, default: () => [] },
    cursos:   { type: Array, default: () => [] },
    departamentos: { type: Array, default: () => [] },
    placeholder: { type: String, default: 'Digite o nome...' },
  },
  emits: ['update:modelValue', 'criado'],

  setup(props, { emit }) {
    const query       = ref('')
    const showList     = ref(false)
    const selectedId   = ref(props.modelValue || '')
    const isNovo       = ref(false)
    const suggestions  = ref([])

    const extra = ref({ matricula: '', cursoNome: '', departamentoNome: '' })
    const showExtraList    = ref(false)
    const extraSuggestions = ref([])
    const extraSelectedId  = ref('')

    const onInput = () => {
      query.value = query.value.toUpperCase()
      selectedId.value = ''
      emit('update:modelValue', '')
      isNovo.value = false

      const termo = query.value.trim()
      if (!termo) {
        suggestions.value = []
        return
      }
      suggestions.value = props.opcoes.filter(o =>
        o.nome.toUpperCase().includes(termo)
      ).slice(0, 8)

      const existeExato = props.opcoes.some(o => o.nome.toUpperCase() === termo)
      isNovo.value = !existeExato
    }

    const selecionar = (item) => {
      query.value = item.nome
      selectedId.value = item.id
      isNovo.value = false
      showList.value = false
      emit('update:modelValue', item.id)
    }

    const onBlur = () => {
      setTimeout(() => { showList.value = false }, 120)
    }

    const listaExtra = () => props.tipo === 'aluno' ? props.cursos : props.departamentos

    const onExtraInput = () => {
      const campo = props.tipo === 'aluno' ? 'cursoNome' : 'departamentoNome'
      extra.value[campo] = extra.value[campo].toUpperCase()
      extraSelectedId.value = ''

      const termo = extra.value[campo].trim()
      if (!termo) {
        extraSuggestions.value = []
        return
      }
      extraSuggestions.value = listaExtra().filter(o =>
        o.nome.toUpperCase().includes(termo)
      ).slice(0, 8)
    }

    const selecionarExtra = (item) => {
      const campo = props.tipo === 'aluno' ? 'cursoNome' : 'departamentoNome'
      extra.value[campo] = item.nome
      extraSelectedId.value = item.id
      showExtraList.value = false
    }

    const onExtraBlur = () => {
      setTimeout(() => { showExtraList.value = false }, 120)
    }

    const confirmar = async () => {
      const nome = query.value.trim().toUpperCase()
      if (!nome) return null

      if (selectedId.value) return selectedId.value

      const payload = { nome }
      if (props.tipo === 'aluno') {
        payload.matricula = extra.value.matricula
        payload.curso_nome = extra.value.cursoNome
      } else {
        payload.departamento_nome = extra.value.departamentoNome
      }

      const path = props.tipo === 'aluno' ? '/alunos/buscar_ou_criar/' : '/professores/buscar_ou_criar/'
      const resultado = await postItem(path, payload)
      selectedId.value = resultado.id
      emit('update:modelValue', resultado.id)
      emit('criado', resultado)
      return resultado.id
    }

    const limpar = () => {
      query.value = ''
      selectedId.value = ''
      isNovo.value = false
      extra.value = { matricula: '', cursoNome: '', departamentoNome: '' }
      extraSelectedId.value = ''
    }

    watch(() => props.modelValue, (v) => {
      if (!v) { query.value = ''; selectedId.value = '' }
    })

    return {
      query, showList, selectedId, isNovo, suggestions, extra,
      showExtraList, extraSuggestions,
      onInput, selecionar, onBlur, confirmar, limpar,
      onExtraInput, selecionarExtra, onExtraBlur,
    }
  },
}
</script>

<style scoped>
.person-picker { position: relative; display: flex; flex-direction: column; gap: 8px; }
.picker-input-wrap { position: relative; }
.picker-check {
  position: absolute; right: 10px; top: 50%; transform: translateY(-50%);
  color: var(--green, #22c55e); font-weight: 700;
}
.picker-suggestions {
  position: absolute; top: 100%; left: 0; right: 0; z-index: 30;
  background: var(--surface-2, #1a1a2e);
  border: 1px solid var(--border-hover, #3a3a55);
  border-radius: 8px; margin-top: 4px; max-height: 180px;
  overflow-y: auto; list-style: none; padding: 4px;
}
.picker-suggestions li { padding: 8px 10px; border-radius: 6px; cursor: pointer; font-size: 0.88rem; }
.picker-suggestions li:hover { background: var(--surface-3, #25253a); }
.picker-sub { color: var(--text-3, #888); font-size: 0.8rem; margin-left: 4px; }
.picker-optional { color: var(--text-3, #888); font-size: 0.74rem; font-weight: 400; }
.picker-extra {
  display: flex; flex-direction: column; gap: 10px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px dashed rgba(99, 102, 241, 0.35);
  border-radius: 8px; padding: 10px; margin-top: 4px; position: relative;
}
.picker-extra-hint { font-size: 0.78rem; color: var(--text-2, #aaa); }
</style>