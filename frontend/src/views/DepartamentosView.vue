<template>
  <EntityView
    title="Departamentos"
    apiPath="/departamentos/"
    :columns="columns"
    :relatedMaps="{ unidade_academica: unidadesMap }"
    searchField="search"
  />
</template>

<script>
import { onMounted, ref } from 'vue';
import EntityView from '../components/EntityView.vue';
import { fetchList } from '../services/api';

export default {
  components: { EntityView },
  setup() {
    const unidadesMap = ref({})
    const columns = [
      { key: 'nome', label: 'Nome' },
      { key: 'sigla', label: 'Sigla' },
      { key: 'unidade_academica', label: 'Unidade Acadêmica' },
    ]

    const loadUnidades = async () => {
      const response = await fetchList('/unidades-academicas/')
      unidadesMap.value = (response.results || response).reduce((acc, unidade) => {
        acc[unidade.id] = unidade.nome
        return acc
      }, {})
    }

    onMounted(loadUnidades)
    return { columns, unidadesMap }
  },
}
</script>
