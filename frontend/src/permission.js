import router from './router/index'
import { useUserStore } from '@/store/user'
import { useMenuStore } from '@/store/menu'
import { useRouteStore } from '@/store/route'

// 不需要登录就可以访问的路由
const whiteList = ['/login', '/register']

/**
 * 全局路由守卫
 * 处理权限验证和动态路由加载
 */
router.beforeEach(async (to, from, next) => {

//   // 获取store
//   const userStore = useUserStore()
//   const menuStore = useMenuStore()
  const routeStore = useRouteStore()
  await routeStore.addDynamicRoutes()
  next()
  /*
  // 判断用户是否已登录
  if (userStore.getLoginStatus) {
    // 已登录状态下访问登录页，重定向到首页
    if (to.path === '/login') {
      next({ path: '/dashboard' })
    } else {
      // 判断是否已获取用户菜单数据
      if (menuStore.isLoaded) {
        try {
          
          // 添加动态路由
          await routeStore.addDynamicRoutes()
          
          // 重新导航到目标路由，确保能匹配到新添加的路由
          next({ ...to, replace: true })
        } catch (error) {
          // 获取菜单失败，可能是token过期，清除用户信息并重定向到登录页
          userStore.logout()
          next(`/login?redirect=${to.path}`)
        }
      } else {
        // 已获取菜单数据，直接放行
        next()
      }
    }
  } else {
    // 未登录状态下，判断是否为白名单路由
    if (whiteList.includes(to.path)) {
      // 白名单路由，直接放行
      next()
    } else {
      // 非白名单路由，重定向到登录页
      next(`/login?redirect=${to.path}`)
    }
  }
  */
})

export default router