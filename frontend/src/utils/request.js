import axios from 'axios'
import { API_CONFIG, USER_STORAGE_KEYS, HTTP_STATUS, ERROR_MESSAGES } from './config'

const request = axios.create(API_CONFIG)

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem(USER_STORAGE_KEYS.TOKEN)
    const user = JSON.parse(localStorage.getItem(USER_STORAGE_KEYS.USER) || '{}')

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    if (user.role) {
      config.headers['X-User-Role'] = user.role
    }

    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 如果是登录请求且成功，使用router进行导航
    if (response.config.url.includes('/login/') && response.status === 200) {
      const router = window._router
      if (router) {
        router.push('/dashboard')
      }
    }
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case HTTP_STATUS.UNAUTHORIZED:
          // 未授权，清除用户信息并跳转到登录页
          localStorage.removeItem(USER_STORAGE_KEYS.TOKEN)
          localStorage.removeItem(USER_STORAGE_KEYS.USER)
          window.location.href = '/login'
          break
        case HTTP_STATUS.FORBIDDEN:
          alert(ERROR_MESSAGES.FORBIDDEN)
          break
        default:
              alert(ERROR_MESSAGES.DEFAULT)
      }
    } else {
      alert(ERROR_MESSAGES.NETWORK_ERROR)
    }
    return Promise.reject(error)
  }
)

export default request