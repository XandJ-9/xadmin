<template>
  <el-aside :width="sidebarWidth">
    <div class="logo" :class="{ 'collapsed': isCollapse }">{{ isCollapse ? 'X' : 'Xadmin' }}</div>
    <el-menu
      :default-active="$route.path"
      class="el-menu-vertical"
      :collapse="isCollapse"
      background-color="#ffffff"
      text-color="#303133"
      active-text-color="#409EFF"
      router
    >
      <template v-for="route in showMenuRoutes" :key="route.path">
        <sub-menu :route="route" />
      </template>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import SubMenu from '@/layout/SubMenuItem.vue'

const router = useRouter()
const menuRoutes = router.options.routes
  .find(route => route.path === '/' && route.children)
  ?.children || []

const showMenuRoutes = menuRoutes.filter(route => route.meta?.hidden !== true)

defineProps({
  isCollapse: {
    type: Boolean,
    required: true
  },
  sidebarWidth: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.el-aside {
  height: 100vh;
  background-color: #ffffff;
  border-right: 1px solid #e6e6e6;
  transition: width 0.3s;
  padding: 0;
  margin: 0;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.el-menu {
  border-right: none;
  padding: 0;
  margin: 0;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  border-bottom: 1px solid #e6e6e6;
  transition: all 0.3s;
  white-space: nowrap;
  overflow: hidden;
}

.logo.collapsed {
  font-size: 24px;
}
</style>