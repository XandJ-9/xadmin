import axios from 'axios'
import { useUserStore } from '@/store/user'
import { API_CONFIG, USER_STORAGE_KEYS, HTTP_STATUS, ERROR_MESSAGES } from './config'
import { ElLoading, ElMessage } from 'element-plus'
import { saveAs } from 'file-saver'

const request = axios.create(API_CONFIG)

// 请求拦截器
request.interceptors.request.use(
  config => {
    // const token = localStorage.getItem(USER_STORAGE_KEYS.TOKEN)
    // const user = JSON.parse(localStorage.getItem(USER_STORAGE_KEYS.USER) || '{}')

    const userStore = useUserStore()
    const token = userStore.getToken
    const role = userStore.getRole

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    if (role) {
      config.headers['X-User-Role'] = role
    }

    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
// request.interceptors.response.use(
//   response => {
//     // 如果是登录请求且成功，使用router进行导航
//     if (response.config.url.includes('/login/') && response.status === 200) {
//         const router = window._router
//         if (router) {
//           router.push('/dashboard')
//         }
//       }
//       return response
//   },
//   error => {
//     console.error('响应错误:', error)
//     if (error.response) {
//       switch (error.response.status) {
//         case HTTP_STATUS.UNAUTHORIZED:
//           // 未授权，清除用户信息并跳转到登录页
//           // localStorage.removeItem(USER_STORAGE_KEYS.TOKEN)
//           // localStorage.removeItem(USER_STORAGE_KEYS.USER)
//           // window.location.href = '/login'
//           ElMessage.error(ERROR_MESSAGES.UNAUTHORIZED)
//           break
//         case HTTP_STATUS.FORBIDDEN:
//             ElMessage.error(ERROR_MESSAGES.FORBIDDEN)
//           break
//         case HTTP_STATUS.BAD_REQUEST:
//             ElMessage.error(ERROR_MESSAGES.BAD_REQUEST)
//           break
//         default:
//             ElMessage.error(ERROR_MESSAGES.DEFAULT)
//           break
//       }
//     } else {
//       ElMessage(ERROR_MESSAGES.NETWORK_ERROR)
//     }
//     return Promise.reject(error)
//   }
// )


export function download(url, method, params = {}, filename='文件导出.xlsx') {
    const downloadLoadingInstance = ElLoading.service({ text: "正在下载数据，请稍候", spinner: "el-icon-loading", background: "rgba(0, 0, 0, 0.7)", })
    return request({
        url: url,
        method: method,
        params: params, 
        responseType: 'blob'
    }).then(async res => {
      let xlsxName = window.decodeURI(res.headers['content-disposition'].split('=')[1]);
      let fileName = xlsxName || `${filename}.xlsx`;
      if (res) {
          const blob = new Blob([res.data], { type: 'charset=utf-8' });
          saveAs(blob, fileName);

        //   使用a标签下载
        //   const elink = document.createElement('a')
        //   elink.download = fileName
        //   elink.style.display = 'none'
        //   elink.href = URL.createObjectURL(blob)
        //   document.body.appendChild(elink)
        //   elink.click()
        //   URL.revokeObjectURL(elink.href) // 释放URL 对象0
        //   document.body.removeChild(elink);
      }
      downloadLoadingInstance.close();
    }).catch((r) => {
      console.error(r)
      ElMessage.error('下载文件出现错误，请联系管理员！')
      downloadLoadingInstance.close();
    })
  }


export default request