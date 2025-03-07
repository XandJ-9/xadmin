import { createRouter, createWebHistory } from 'vue-router'

const routes = [
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
        path: '/',
        name: 'Layout',
        component: () => import('@/layout/Layout.vue'),
        children: [
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('@/views/Dashboard.vue')
            },
            {
                path: 'users',
                name: 'Users',
                component: () => import('@/views/Users.vue')
            },
            {
                path: 'roles',
                name: 'Roles',
                component: () => import('@/views/Roles.vue')
            }
        ]
    }
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