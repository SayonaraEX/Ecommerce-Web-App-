// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Shop/Shop.vue'
import AuthDashboard from '../components/Authentication/Auth_dasboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Shop',
      component: Home
    },
    {
      path: '/auth', 
      name: 'auth-dashboard', 
      component: AuthDashboard 
    }
  ]
})

export default router