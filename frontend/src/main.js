import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
// import './style.css'
import '@/styles/index.scss' // global css
import App from './App.vue'
import store from './store'
import router from './router'
import { download } from '@/utils/request'
// 导入路由权限守卫
import './permission'


const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 提供全局方法
app.provide('download', download)

app.use(store)
app.use(router)
app.use(ElementPlus)
app.mount('#app')