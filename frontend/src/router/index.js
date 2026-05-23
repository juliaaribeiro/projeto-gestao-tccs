import { createRouter, createWebHistory } from 'vue-router'
import AlunosView from '../views/AlunosView.vue'
import CursosView from '../views/CursosView.vue'
import DashboardView from '../views/DashboardView.vue'
import DepartamentosView from '../views/DepartamentosView.vue'
import ProfessoresView from '../views/ProfessoresView.vue'
import TCCsView from '../views/TCCsView.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: DashboardView },
  { path: '/alunos', name: 'Alunos', component: AlunosView },
  { path: '/professores', name: 'Professores', component: ProfessoresView },
  { path: '/cursos', name: 'Cursos', component: CursosView },
  { path: '/departamentos', name: 'Departamentos', component: DepartamentosView },
  { path: '/tccs', name: 'TCCs', component: TCCsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
