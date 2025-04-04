import { defineStore } from 'pinia'
import { useMenuStore } from './menu'
import router from '@/router'

/**
 * 路由状态管理
 */
export const useRouteStore = defineStore('route', {
  state: () => ({
    // 动态路由是否已添加
    isRoutesAdded: false
  }),
  
  getters: {
    /**
     * 获取路由添加状态
     */
    getRoutesAddedStatus: (state) => state.isRoutesAdded
  },
  
  actions: {
    /**
     * 根据菜单数据生成路由配置
     * @param {Array} menuTree 树形结构的菜单数据
     * @returns {Array} 路由配置数组
     */
    generateRoutes(menuTree) {
      // 这里可以根据实际需求实现路由生成逻辑
      // 当前项目已经有静态路由配置，此处可以根据权限过滤或动态添加路由
      return []
    },
    
    /**
     * 添加动态路由
     */
    async addDynamicRoutes() {
      if (this.isRoutesAdded) {
        return
      }
      
      // 获取菜单数据
      const menuStore = useMenuStore()
      if (!menuStore.isLoaded) {
        await menuStore.fetchUserMenus()
      }
      
      // 生成路由配置
      const routes = this.generateRoutes(menuStore.getMenuTree)
      
      console.log('routes', routes)
      
      // 添加路由
      routes.forEach(route => {
        router.addRoute(route)
      })
      
      this.isRoutesAdded = true
    },
    
    /**
     * 重置路由状态
     */
    resetRouteState() {
      this.isRoutesAdded = false
      // 这里可以添加移除动态路由的逻辑
    }
  }
})