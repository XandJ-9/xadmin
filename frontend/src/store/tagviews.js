import { defineStore } from "pinia"

export const useTagViewsStore = defineStore('tagviews', {
  state: () => ({
    visitedViews: [{
      name: 'Dashboard',
      path: '/dashboard',
      title: '首页',
      query: {}
    }]
  }),
  actions: {
    // 添加访问过的路由到visitedViews数组
    addVisitedView(view) {
      if (this.visitedViews.some(v => v.path === view.path)) return
      
      if (view.meta && view.meta.needTagview) {
        this.visitedViews.push(
          Object.assign({}, view, {
            title: view.meta.title || 'no-name'
          })
        )
      }
    },
    
    // 删除visitedViews中的某个路由
    delVisitedView(view) {
      // 首页不允许删除
      if (view.path === '/dashboard') return
      
      const index = this.visitedViews.findIndex(v => v.path === view.path)
      if (index > -1) {
        this.visitedViews.splice(index, 1)
      }
      return [...this.visitedViews]
    },
    
    // 关闭其他标签页，只保留当前和首页
    delOthersVisitedViews(view) {
      this.visitedViews = this.visitedViews.filter(v => {
        return v.path === '/dashboard' || v.path === view.path
      })
      return [...this.visitedViews]
    },
    
    // 关闭所有标签页，只保留首页
    delAllVisitedViews() {
      this.visitedViews = this.visitedViews.filter(v => v.path === '/dashboard')
      return [...this.visitedViews]
    },
    
    // 更新标签页，用于刷新页面
    updateVisitedView(view) {
      for (let v of this.visitedViews) {
        if (v.path === view.path) {
          v = Object.assign(v, view)
          break
        }
      }
    }
  }
})