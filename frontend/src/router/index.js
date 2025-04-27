import { createRouter, createWebHistory } from 'vue-router'
import { DataBoard } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

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
  },
  {
    path: '/404',
    name: '404',
    component: () => import('@/views/NotFound.vue')
  },
  {
    path: '/redirect',
    name: 'Redirect',
    component: () => import('@/views/Redirect.vue')
  }
]

const asyncRoutes = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/index.vue'),
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {
          icon: DataBoard,
          title: 'Dashboard',
          needTagview: true
        }
      }
    ]
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



// router.beforeEach((to, from, next) => {
//   // const token = localStorage.getItem('token')
//   const userStore = useUserStore()
//   const token = userStore.getToken
//   if (to.path === '/login' || to.path === '/register') {
//     next()
//   } else if (!token) {
//     next('/login')
//   } else {
//     next()
//   }
// })

export default router