import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import LeadsView from '@/views/lead/LeadsView.vue'
import AddLeadView from '@/views/lead/AddLeadView.vue'
import LeadDetailView from '@/views/lead/LeadDetailView.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/leads',
    name: 'Leads',
    component: LeadsView,
  },
  {
    path: '/leads/add',
    name: 'AddLead',
    component: AddLeadView,
  },
  {
    path: '/leads/:id',
    name: 'LeadDetail',
    component: LeadDetailView,
  },
]

const router = createRouter({
  history: createWebHistory('/backoffice'),
  routes,
})

export default router
