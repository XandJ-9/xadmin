import { defineStore } from 'pinia'
import request from '@/utils/request'
import { getToken, removeToken, setToken } from '@/utils/auth'

/**
 * 用户状态管理
 */
export const useUserStore = defineStore('user', {
  state: () => ({
    // 用户token
    token: '',
    // 是否已登录
    isLoggedIn: false,
    role: '',
    username: ''
  }),
  
  getters: {

    getUsername: (state) => state.username,
    
    getRole: (state) => state.role,

    getUserToken: (state) => state.token,
    
    getLoginStatus: (state) => state.isLoggedIn
  },
  
  actions: {
    /**
     * 设置用户信息和token
     * @param {Object} userData 用户数据对象，包含token和user信息
     */
    setUserData({ username, role }) {
    
        // 更新状态
        this.username = username
        this.role = role
        this.isLoggedIn = true
      // 保存到本地存储
      // localStorage.setItem('token', token)
      // localStorage.setItem('user', JSON.stringify(user))
    },
    setUserToken(token) {
        this.token = token
        localStorage.setItem('token', token)
        setToken(token)
    },
    /**
     * 用户登录
     * @param {Object} loginData 登录表单数据
     */
    async login(loginData) {
        try {
            // 发送登录请求
            const response = await request.post('/api/login', loginData)
            const { token, user } = response.data
            
            // 保存用户数据
            this.setUserData({ username: user.username, role: user.role_info.name })
            this.setUserToken(token)

            // 获取登录路由

            return {
                success: true,
                message: '登录成功'
            }
        } catch (error) {
          return { 
            success: false, 
            message: error.response?.data?.error || '登录失败，请稍后重试'
          }
        }
      },
    
    getUserInfo() {
        request.get('/api/users/getUserInfo/').then(response => {
            const userInfo = response.data.user
            this.setUserData({ username: userInfo.username, role: userInfo.role_info.name})
        })
    },
    
    /**
     * 用户注销
     */
    logout() {
        // 清除状态
        this.token = ''
        this.username = ''
        this.role = ''
        this.isLoggedIn = false
      
        // 清除本地存储
        removeToken()
        // localStorage.removeItem('token')
        // localStorage.removeItem('user')
        }
  }
})