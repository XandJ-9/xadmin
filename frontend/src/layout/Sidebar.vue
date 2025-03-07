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
      <el-menu-item index="/dashboard">
        <el-icon><DataBoard /></el-icon>
        <span>Dashboard</span>
      </el-menu-item>
      <el-menu-item index="/users">
        <el-icon><User /></el-icon>
        <span>用户管理</span>
      </el-menu-item>
      <el-menu-item index="/roles">
        <el-icon><Setting /></el-icon>
        <span>角色管理</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { User, Setting, DataBoard } from '@element-plus/icons-vue'

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