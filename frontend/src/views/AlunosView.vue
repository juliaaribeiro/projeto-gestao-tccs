<template>
  <EntityView
    title="Alunos"
    apiPath="/alunos/"
    :columns="columns"
    :relatedMaps="{ curso: cursosMap }"
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
    const cursosMap = ref({})
    const columns = [
      { key: 'nome', label: 'Nome' },
      { key: 'matricula', label: 'Matrícula' },
      { key: 'curso', label: 'Curso' },
    ]

    const loadCourses = async () => {
      const cursos = await fetchList('/cursos/')
      cursosMap.value = (cursos.results || cursos).reduce((acc, curso) => {
        acc[curso.id] = curso.nome
        return acc
      }, {})
    }

    onMounted(loadCourses)

    return { columns, cursosMap }
  },
}
</script>
