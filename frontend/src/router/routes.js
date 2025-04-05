import { User, Setting, DataBoard, Collection, Edit } from '@element-plus/icons-vue'

export const dynamicRoutes = [
  {
  path: 'system',
  name: 'System',
  meta: {
    icon: Setting,
    title: '系统管理'
  },
  children: [
    {
      path:'system-role',
      name: 'SystemRole',
      component: () => import('@/views/system/Roles.vue'),
      meta: {
        icon: Setting,
        title: '角色管理'
      }
    },
    {
      path:'system-user',
      name: 'SystemUser',
      component: () => import('@/views/system/Users.vue'),
      meta: {
        icon: Setting,
        title: '用户管理'
      }
    },
    {
      path:'system-menu',
      name: 'SystemMenu',
      component: () => import('@/views/system/Menu.vue'),
      meta: {
        icon: Setting,
        title: '菜单管理'
      }
    },
    {
      path: 'system-config',
      name: 'SystemConfig',
      component: () => import('@/views/system/Config.vue'),
      meta: {
        icon: Setting,
        title: '系统配置'
      }
    },
    {
      path: 'system-log',
      name: 'SystemLog',
      component: () => import('@/views/system/Log.vue'),
      meta: {
        icon: Setting,
        title: '系统日志'
      }
    }
  ]
  }
]