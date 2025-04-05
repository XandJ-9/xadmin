import { defineStore } from 'pinia'
import request from '@/utils/request'

/**
 * 用户状态管理
 */
export const useUserStore = defineStore('user', {
  state: () => ({
    // 用户信息
    userInfo: JSON.parse(localStorage.getItem('user') || '{}'),
    // 用户token
    token: localStorage.getItem('token') || '',
    // 是否已登录
    isLoggedIn: !!localStorage.getItem('token')
  }),
  
  getters: {
    /**
     * 获取用户信息
     */
    getUserInfo: (state) => state.userInfo,
    
    /**
     * 获取用户token
     */
    getToken: (state) => state.token,
    
    /**
     * 判断用户是否已登录
     */
    getLoginStatus: (state) => state.isLoggedIn
  },
  
  actions: {
    /**
     * 设置用户信息和token
     * @param {Object} userData 用户数据对象，包含token和user信息
     */
    setUserData(userData) {
      const { token, user } = userData
      
      // 更新状态
      this.token = token
      this.userInfo = user
      this.isLoggedIn = true
      
      // 保存到本地存储
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
    },
    
    /**
     * 用户登录
     * @param {Object} loginData 登录表单数据
     */
    async login(loginData) {
      try {
        // 发送登录请求
        const response = await request.post('/api/users/login/', loginData)
        const userData = response.data
        
        // 保存用户数据
        this.setUserData(userData)
        
        return { success: true }
      } catch (error) {
        console.error('登录失败', error)
        return { 
          success: false, 
          error: error.response?.data?.error || '登录失败，请稍后重试'
        }
      }
    },
    
    /**
     * 用户注销
     */
    logout() {
      // 清除状态
      this.token = ''
      this.userInfo = {}
      this.isLoggedIn = false
      
      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})