'use strict'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'

// import path from 'path'

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    // base: '/', // 设置基础路径
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    build: {
        // 指定输出结果
        // 后端项目直接访问静态文件
        outDir: '../backend_django/statics/',
    },
    server: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                // rewrite: (path) => path.replace(/^\/api/, '')
            }
        },
        // historyApiFallback: true // 启用HTML5 History API回退
    }
})
