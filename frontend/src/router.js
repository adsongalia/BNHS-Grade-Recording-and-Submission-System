import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue' 
import TeacherDashboard from './components/TeacherDashboard.vue'
import PrincipalDashboard from './components/PrincipalDashboard.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/teacher-dashboard', component: TeacherDashboard },
  { path: '/principal-dashboard', component: PrincipalDashboard }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})