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
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {
          icon: DataBoard,
          title: 'Dashboard'
        }
      },
      // ...systemRoutes
      // {
      //   path: 'system',
      //   name: 'System',
      //   meta: {
      //     icon: Setting,
      //     title: '系统管理'
      //   },
      //   children: [
      //     {
      //       path:'system-role',
      //       name: 'SystemRole',
      //       component: () => import('@/views/system/Roles.vue'),
      //       meta: {
      //         icon: Setting,
      //         title: '角色管理'
      //       }
      //     },
      //     {
      //       path:'system-user',
      //       name: 'SystemUser',
      //       component: () => import('@/views/system/Users.vue'),
      //       meta: {
      //         icon: Setting,
      //         title: '用户管理'
      //       }
      //     },
      //     {
      //       path:'system-menu',
      //       name: 'SystemMenu',
      //       component: () => import('@/views/system/Menu.vue'),
      //       meta: {
      //         icon: Setting,
      //         title: '菜单管理'
      //       }
      //     },
      //     {
      //       path: 'system-config',
      //       name: 'SystemConfig',
      //       component: () => import('@/views/system/Config.vue'),
      //       meta: {
      //         icon: Setting,
      //         title: '系统配置'
      //       }
      //     },
      //     {
      //       path: 'system-log',
      //       name: 'SystemLog',
      //       component: () => import('@/views/system/Log.vue'),
      //       meta: {
      //         icon: Setting,
      //         title: '系统日志'
      //       }
      //     }
      //   ]
      // },
      // {
      //   path: 'datasources',
      //   name: 'Datasources',
      //   component: () => import('@/views/DataSources.vue'),
      //   meta: {
      //     icon: Collection,
      //     title: '数据源管理'
      //   }
      // },
      // {
      //   path: 'dataquery',
      //   redirect: '/dataquery/index',
      //   meta: {
      //     icon: Edit,
      //     title: '数据开发'
      //   },
      //   children: [
      //     {
      //       path: 'index',
      //       name: 'DataQuery',
      //       component: () => import('@/views/dataquery/index.vue'),
      //       meta: {
      //         icon: Edit,
      //         title: '数据查询'
      //       }
      //     },
      //     {
      //       path: 'querylog',
      //       name: 'QueryLog',
      //       component: () => import('@/views/dataquery/QueryLog.vue'),
      //       meta: {
      //         icon: Edit,
      //         title: '查询日志'
      //       }
      //     }
      //   ]
      // },
      // {
      //   path: 'reportmanage',
      //   name: 'ReportManage',
      //   component: () => import('@/views/reportinfo/index.vue'),
      //   meta: {
      //     icon: Edit,
      //     title: '报表信息'
      //   },
      //   children: [
      //     {
      //       path: 'platform',
      //       name: 'Platform',
      //       component: () => import('@/views/reportinfo/PlatformManage.vue'),
      //       meta: {
      //         icon: Edit,
      //         title: '平台管理'
      //       }
      //     },
      //     {
      //       path: 'module',
      //       name: 'Module',
      //       component: () => import('@/views/reportinfo/ModuleManage.vue'),
      //       meta: {
      //         icon: Edit,
      //         title: '模块管理'
      //       }
      //     },
      //     {
      //       path: 'report',
      //       name: 'Report',
      //       component: () => import('@/views/reportinfo/ReportManage.vue'),
      //       meta: {
      //         icon: Edit,
      //         title: '报表设计'
      //       }
      //     },
      //     {
      //       path: 'interface',
      //       name: 'Interface',
      //       component: () => import('@/views/reportinfo/InterfaceManage.vue'),
      //       meta: {
      //         icon: Edit,
      //         title: '接口管理'
      //       }
      //     },
      //     {
      //       path: 'interface-fields/:id',
      //       name: 'InterfaceFields',
      //       component: () => import('@/views/reportinfo/InterfaceFields.vue'),
      //       hidden: true,
      //       meta: {
      //         icon: Edit,
      //         title: '接口字段管理',
      //       }
      //     }
      //   ]
      // }
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