import { defineStore } from 'pinia'
import router from '@/router'

// 动态导入所有的视图组件， ES推荐使用
const viewsModules = import.meta.glob('@/views/**/*.vue')

export function dynamicImport(dynamicViewsModules, component) {
  const keys = Object.keys(dynamicViewsModules);
  const matchKeys = keys.filter((key) => {
    const k = key.replace(/\/src\/views|../, '');
    return k.startsWith(`${component}`) || k.startsWith(`/${component}`);
  });

  if (matchKeys?.length === 1) {
      const matchKey = matchKeys[0];
      return dynamicViewsModules[matchKey];
  }
  if (matchKeys?.length > 1) {
      return false;
  }
}

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

      const result = []

      // 处理菜单数据，转换为路由格式
      menuTree.forEach(item => {
          const tmp = {...item}
          // 使用静态路径映射替代动态导入
          // console.log(`@/views/${item.component}.vue`)
          // 原菜单名称修改为组件名称，因为keep-alive需要组件名称，因此将路由的name字段设置为组件名称
          tmp.name = tmp.component_name
          tmp.component = dynamicImport(viewsModules ,tmp.component)
          // item.component = () => import(`@/views/${item.component}.vue`)
          // item.component = (resolve) => require([`@/views/${item.component}.vue`],resolve)
        
        if (tmp.children) {
          tmp.children = this.generateRoutes(tmp.children)
        }
        
        result.push(tmp)
      })

      // 返回系统路由配置，确保它能被正确添加到路由中
      return result
    },
    
    /**
     * 添加动态路由
     */
    async addDynamicRoutes(menuTree) {
      if (this.isRoutesAdded) {
        return
      }
      
      // 生成路由配置
      const routes = this.generateRoutes(menuTree)

      // // 添加路由
      routes.forEach(route => {
        // 系统路由已经是相对路径，直接添加到根路由的children中
        router.addRoute('Layout', route)
      })
      this.isRoutesAdded = true
    },
    
    /**
     * 更新路由信息
     */
    updateRoutes() {
      // 这里可以根据实际需求实现路由更新逻辑
      // 例如，当菜单数据发生变化时，更新路由信息
      // 你可能需要使用 Vuex 或其他状态管理库来存储和获取菜单数据
      this.resetRouteState()
      this.addDynamicRoutes()
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
      },
  }
})