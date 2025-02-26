import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import MainPage from '../views/MainPage.vue'
import CarDetail from '../views/CarDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/main',
    name: 'MainPage',
    component: MainPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/car/:id',
    name: 'CarDetail',
    component: CarDetail,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/')
  } else {
    next()
  }
})

export default router
