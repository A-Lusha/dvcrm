import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Leads from '@/views/lead/Leads.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/leads',
    name: 'Leads',
    component: Leads,
  },
]

const router = createRouter({
  history: createWebHistory('/backoffice'),
  routes,
})

export default router
