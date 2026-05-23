<template>
  <EntityView
    title="Professores"
    apiPath="/professores/"
    :columns="columns"
    :relatedMaps="{ departamento: departamentosMap }"
    searchField="nome"
  />
</template>

<script>
import { onMounted, ref } from 'vue';
import EntityView from '../components/EntityView.vue';
import { fetchList } from '../services/api';

export default {
  components: { EntityView },
  setup() {
    const departamentosMap = ref({})
    const columns = [
      { key: 'nome', label: 'Nome' },
      { key: 'departamento', label: 'Departamento' },
    ]

    const loadDepartamentos = async () => {
      const dados = await fetchList('/departamentos/')
      departamentosMap.value = (dados.results || dados).reduce((acc, departamento) => {
        acc[departamento.id] = departamento.nome
        return acc
      }, {})
    }

    onMounted(loadDepartamentos)
    return { columns, departamentosMap }
  },
}
</script>
