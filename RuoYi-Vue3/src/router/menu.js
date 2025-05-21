import Layout from '@/layout'

export const menu = 
    {
      path: '/system',
      component: Layout,
      redirect: '/system/user',
      name: 'System',
      permissions: ['*:*:*'],
      meta: { title: '系统管理', icon: 'system' },
      children: [
        {
          path: 'user',
          component: () => import('@/views/system/user/index'),
          name: 'User',
          permissions: ['*:*:*'],
          meta: { title: '用户管理' }
        },
        {
          path: 'role',
          component: () => import('@/views/system/role/index'),
          name: 'Role',
          permissions: ['*:*:*'],
          meta: { title: '角色管理' }
        },
        {
          path: 'menu',
          component: () => import('@/views/system/menu/index'),
          name: 'Menu',
          permissions: ['*:*:*'],
          meta: { title: '菜单管理' }
        },
        {
          path: 'dict',
          component: () => import('@/views/system/dict/index'),
          name: 'Dict',
          permissions: ['*:*:*'],
          meta: { title: '字典管理' }
        }
      ]
  
    }
