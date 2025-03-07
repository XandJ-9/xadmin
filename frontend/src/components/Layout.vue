<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '200px'">
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
        <el-menu-item index="/dashboard/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/roles">
          <el-icon><Setting /></el-icon>
          <span>角色管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-left">
          <el-icon class="fold-btn" @click="isCollapse = !isCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="el-dropdown-link">
              管理员<el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <slot></slot>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { User, Setting, ArrowDown, Expand, Fold } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const isCollapse = ref(false)

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

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

.el-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.fold-btn {
  font-size: 20px;
  cursor: pointer;
  color: #303133;
}

.fold-btn:hover {
  color: #409EFF;
}

.header-right {
  cursor: pointer;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  color: #303133;
}

.el-main {
  background-color: #f5f7fa;
  padding: 0;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.el-container {
  margin-left: 200px;
  transition: margin-left 0.3s;
}

.el-container:has(+ .el-aside[style*="width: 64px"]) {
  margin-left: 64px;
}
</style>