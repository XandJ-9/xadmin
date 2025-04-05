import { defineStore } from 'pinia'
import { useMenuStore } from './menu'
import router from '@/router'
import { dynamicRoutes } from '../router/routes'
/**
 * 路由状态管理
 */
export const useRouteStore = defineStore('route', {
  state: () => ({
    // 动态路由是否已添加
    isRoutesAdded: false,
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

      // 处理菜单数据，转换为路由格式
      menuTree.forEach(item => {
        if (item.children) {
          item.children.forEach(child => {
            child.path = child.path
            child.component = () => import(`@/views/${child.component}.vue`)
          })
        }
      })

      console.log('menuTree', menuTree)
      // 返回系统路由配置，确保它能被正确添加到路由中
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
      
      // // 添加路由
      dynamicRoutes.forEach(route => {
        // 系统路由已经是相对路径，直接添加到根路由的children中
        router.addRoute('Layout', route)
      })

      this.isRoutesAdded = true
    },
    
    /**
     * 重置路由状态
     */
    resetRouteState() {
      // 重置菜单状态
      const menuStore = useMenuStore()
      menuStore.resetMenuState()
      this.isRoutesAdded = false
      // 这里可以添加移除动态路由的逻辑
    }
  }
})