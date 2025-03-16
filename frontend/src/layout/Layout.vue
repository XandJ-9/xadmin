<template>
  <el-container class="layout-container">
    <Sidebar :is-collapse="isCollapse" :sidebar-width="sidebarWidth" />
    <AppMain v-model:is-collapse="isCollapse" :sidebar-width="sidebarWidth" />
  </el-container>
</template>

<script setup>
import Sidebar from './Sidebar.vue'
import AppMain from './AppMain.vue'
import { ref, computed, provide } from 'vue'

const isCollapse = ref(false)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')

// TagView状态管理
const visitedViews = ref([])
const addView = (view) => {
  const isExists = visitedViews.value.some(v => v.path === view.path)
  if (!isExists) {
    visitedViews.value.push({
      name: view.name,
      path: view.path,
      title: view.meta?.title || '未命名',
      query: view.query
    })
  }
}

const delView = (view) => {
  const index = visitedViews.value.findIndex(v => v.path === view.path)
  if (index > -1) {
    visitedViews.value.splice(index, 1)
  }
}

// 提供TagView相关的状态和方法
provide('visitedViews', visitedViews)
provide('addView', addView)
provide('delView', delView)
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

</style>