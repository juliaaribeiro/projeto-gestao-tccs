<template>
  <EntityView
    title="Cursos"
    apiPath="/cursos/"
    :columns="columns"
    searchField="nome"
  />
</template>

<script>
import EntityView from '../components/EntityView.vue';

export default {
  components: { EntityView },
  setup() {
    const columns = [
      { key: 'nome', label: 'Nome' },
      { key: 'sigla', label: 'Sigla' },
      { key: 'codigo', label: 'Código' },
    ]

    return { columns }
  },
}
</script>
