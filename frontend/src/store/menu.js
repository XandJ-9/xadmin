import { defineStore } from 'pinia'
import request from '@/utils/request'
import { listToTree } from '@/utils/treeUtils'

/**
 * 菜单和路由状态管理
 */
export const useMenuStore = defineStore('menu', {
  state: () => ({
    // 原始菜单数据（扁平结构）
    menuList: [],
    // 树形结构的菜单数据
    menuTree: [],
    // 是否已加载菜单数据
    loaded: false
  }),
  
  getters: {
    /**
     * 获取树形结构的菜单数据
     */
    getMenuTree: (state) => state.menuTree,
    
    /**
     * 获取扁平结构的菜单数据
     */
    getMenuList: (state) => state.menuList,
    
    /**
     * 判断菜单数据是否已加载
     */
    isLoaded: (state) => state.loaded
  },
  
  actions: {
    /**
     * 设置菜单数据
     * @param {Array} menuList 扁平结构的菜单数据
     */
    setMenus(menuList) {
      this.menuList = menuList
      this.menuTree = listToTree(menuList)
      this.loaded = true
    },
    
    /**
     * 从服务器获取用户菜单数据
     */
    async fetchUserMenus() {
      try {
        const response = await request.get('/api/menus/user_menus/')
        const menuList = response.data
        this.setMenus(menuList)
        return this.menuTree
      } catch (error) {
        console.error('获取用户菜单失败:', error)
        return []
      }
    },
    
    /**
     * 重置菜单状态
     */
    resetMenuState() {
      this.menuList = []
      this.menuTree = []
      this.loaded = false
    }
  }
})