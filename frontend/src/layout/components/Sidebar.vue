<template>
  <div class="el-aside">
    <!-- 侧边栏内容 -->
    <div class="logo" :class="{ 'collapsed': isCollapse }">{{ isCollapse ? 'X' : 'Xadmin' }}</div>
    <el-scrollbar wrap-class="scrollbar-wrapper">
    <el-menu
      class="el-menu-vertical"
      :default-active="$route.path"
      :collapse="isCollapse"
      :background-color="menuVariables.menuBg"
        :text-color="menuVariables.menuText"
        :unique-opened="false"
        :active-text-color="menuVariables.menuActiveText"
        :collapse-transition="false"
        mode="vertical"
      router
    >
      <sidebar-item 
        v-for="(route,index) in sidebarRouters" 
        :key="route.path + index"
        :route="route" 
        :base-path="'/'"
        />
    </el-menu>
    </el-scrollbar>
    </div>
</template>

<script setup>
import * as variables from '@/styles/variables.scss'
import { useRouter } from 'vue-router'
import SidebarItem from './SidebarItem.vue'
import { useMenuStore } from '@/store/menu'
import { useAppStore } from '@/store/app'
import { computed } from 'vue'

const menuStore = useMenuStore()
const router = useRouter()
const appStore = useAppStore()
const constantRouters = router.options.routes
  .find(route => route.path === '/' && route.children)
  ?.children || []

const sidebarRouters = [ ...constantRouters, ...menuStore.menuTree ]

const menuVariables = computed(() => variables)

const isCollapse = computed(() => !appStore.getSidebar.opened)

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

<style lang="scss" scoped>
  @import "@/styles/mixin.scss";
  @import "@/styles/variables.scss";

  .app-wrapper {
    @include clearfix;
    position: relative;
    height: 100%;
    width: 100%;

    &.mobile.openSidebar {
      position: fixed;
      top: 0;
    }
  }

  .drawer-bg {
    background: #000;
    opacity: 0.3;
    width: 100%;
    top: 0;
    height: 100%;
    position: absolute;
    z-index: 999;
  }

  .fixed-header {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 9;
    width: calc(100% - #{$sideBarWidth});
    transition: width 0.28s;
  }

  .hideSidebar .fixed-header {
    width: calc(100% - 54px)
  }

  .mobile .fixed-header {
    width: 100%;
  }
</style>
