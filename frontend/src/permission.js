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
    // 获取store
    const userStore = useUserStore()
    const menuStore = useMenuStore()
    const routeStore = useRouteStore()
  // 检查是否为白名单路由（登录、注册等不需要验证的页面）
  if (whiteList.includes(to.path)) {
    // 白名单路由直接放行
    return next()
  }
  
  // 检查用户是否已登录
  const isLoggedIn = userStore.getLoginStatus
  
  // 未登录状态下，重定向到登录页
  if (!isLoggedIn) {
    console.log('未登录或登录失败...')
    return next(`/login?redirect=${to.path}`)
  }
  
  // 已登录状态下访问登录页，重定向到首页
  if (to.path === '/login') {
    return next({ path: '/dashboard' })
  }
  
  // 检查动态路由是否已加载
    if (!routeStore.getRoutesAddedStatus) {
      console.log('动态路由未加载')
    try {
      // 确保菜单数据已加载
      if (!menuStore.isLoaded) {
        await menuStore.fetchUserMenus()
      }
      
      // 添加动态路由
      await routeStore.addDynamicRoutes()

      // console.log('动态路由已加载', router.getRoutes())
      
      // 重新导航到目标路由，确保能匹配到新添加的路由
      return next({ ...to, replace: true })
    } catch (error) {
      console.error('加载动态路由失败:', error)
      // 加载失败，可能是token过期，清除用户信息并重定向到登录页
      userStore.logout()
      return next(`/login?redirect=${to.path}`)
    }
  }
    // 判断访问的路由是否在动态路由中,
    // 需要修改使用正则匹配
  if(router.resolve(to).matched.length === 0) {
    next('/404')
  } else {
    next()
  }
  // 其他情况，直接放行
  // console.log('路由', router.getRoutes())
  // next()
}
)

export default router