<template>
  <el-container class="layout-container">
    <Sidebar :is-collapse="isCollapse" :sidebar-width="sidebarWidth" />
    <AppMain v-model:is-collapse="isCollapse" :sidebar-width="sidebarWidth" />
  </el-container>
</template>

<script setup>
import Sidebar from './Sidebar.vue'
import AppMain from './AppMain.vue'
import { ref, computed } from 'vue'

const isCollapse = ref(false)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

</style>