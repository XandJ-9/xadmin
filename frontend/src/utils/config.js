// API配置
export const API_CONFIG = {
  timeout: 5000
}

// 用户信息相关配置
export const USER_STORAGE_KEYS = {
  TOKEN: 'token',
  USER: 'user'
}

// HTTP状态码配置
export const HTTP_STATUS = {
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403
}

// 错误消息配置
export const ERROR_MESSAGES = {
  BAD_REQUEST: '请求失败，请稍后重试',
  NETWORK_ERROR: '网络错误，请检查您的网络连接',
  FORBIDDEN: '您没有权限访问此资源',
  DEFAULT: '请求失败，请稍后重试'
}