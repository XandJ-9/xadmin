import { createRouter, createWebHistory } from 'vue-router'
import { User, Setting, DataBoard, Collection, Edit } from '@element-plus/icons-vue'

const constantRoutes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  }
]

const asyncRoutes = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/index.vue'),
    // children: [
    //   {
    //     path: 'dashboard',
    //     name: 'Dashboard',
    //     component: () => import('@/views/Dashboard.vue'),
    //     meta: {
    //       icon: DataBoard,
    //       title: 'Dashboard'
    //     }
    //   }
    // ]
  }
]


const routes = [
  ...constantRoutes,
  ...asyncRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/login' || to.path === '/register') {
    next()
  } else if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router