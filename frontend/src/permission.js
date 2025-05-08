import router from './router/index'
import { useUserStore } from '@/store/modules/user'
import { useRouteStore } from '@/store/modules/permission'
import { getToken, removeToken } from '@/utils/auth'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style

// 不需要登录就可以访问的路由
const whiteList = ['/login', '/register']


/**
 * 全局路由守卫
 * 处理权限验证和动态路由加载
 */
router.beforeEach(async (to, from, next) => {
    NProgress.start()
    // 获取store
    const routeStore = useRouteStore()

    // 检查用户是否已登录
    const loginToken = getToken()

    if (loginToken) {

        // 检查动态路由是否已加载
        if (!routeStore.getRoutesAddedStatus) {
            try {
                // 获取用户信息
                const userStore = useUserStore()
                await userStore.getUserInfo()
                // 添加动态路由
                await routeStore.addDynamicRoutes()
                // 重新导航到目标路由，确保能匹配到新添加的路由
                next({ ...to, replace: true })
            } catch (error) {
                // 加载失败，可能是token过期，清除用户信息并重定向到登录页
                removeToken()
                next(`/login?redirect=${to.path}`)
            }
        } else {
            // 判断访问的路由是否在动态路由中,
            if (router.resolve(to).matched.length === 0) {
                next('/404')
            } else {
                // 已登录状态下访问登录页，重定向到首页
                if (to.path === '/login') {
                    next({ path: '/dashboard' })
                } else {
                    next()
                }
            }
        }
    } else {
        // whiteList.indexOf(to.path) !== -1 
        if (whiteList.includes(to.path)){
            next()
        } else {
            next(`/login?redirect=${to.path}`)
        }
    }
}
)

router.afterEach(() => {
    NProgress.done()
})

export default router