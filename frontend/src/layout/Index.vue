<template>
  <div class="app-wrapper" :class="{'hideSidebar': !appStore.getSidebar.opened}">
    <Sidebar class="sidebar-container" />
    <div class="main-container">
    <el-header class="fixed-header">
        <div class="header-left">
            <el-icon class="fold-btn" @click="toggleCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
            </el-icon>
        </div>
        <div class="header-right">
            <el-dropdown>
            <span class="el-dropdown-link">
                {{ username }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </template>
            </el-dropdown>
        </div>
    </el-header>
    <tags-view class="tags-view-container" />
    <app-main class="app-main"/>
  </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
import AppMain from './components/AppMain.vue'
import { ref, computed, onMounted } from 'vue'
import TagsView from './components/TagsView.vue'
import { useUserStore } from '@/store/modules/user'
import { useAppStore } from '@/store/modules/app'
import { useRouter } from 'vue-router'

const router = useRouter()
const isCollapse = ref(false)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')
const username = ref('')

const userStore = useUserStore()
const appStore = useAppStore()
onMounted(() => {
  // const user = localStorage.getItem('user')
  // if (user) {
  //   const userData = JSON.parse(user)
  //   username.value = userData.username
  // }
  username.value = userStore.getUsername
})


const mainWidth = computed(() => {
  // return `calc(100vw - ${sidebarWidth})`
  return isCollapse.value? 'calc(100vw - 64px)' : 'calc(100vw - 200px)'
})


const toggleCollapse = () => {
    appStore.toggleSidebar()
    isCollapse.value = !appStore.getSidebar.opened
}

const handleLogout = () => {
  const userStore = useUserStore()
  userStore.logout()
  router.push('/login')
}


</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}


/* .main-container {
    position: fixed;
    right: 0;
    top: 0;
    transition: width 0.3s;
    width: 100%;
} */

.el-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.fold-btn {
  font-size: 30px;
  cursor: pointer;
  color: #303133;
  padding: 5px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.fold-btn:hover {
  color: #409EFF;
  background-color: rgba(64, 158, 255, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  color: #303133;
  font-size: 14px;
  padding: 5px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.el-dropdown-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
}


</style>

<style lang="scss" scoped>
  @use "@/styles/mixin.scss" as mixin;
  @use "@/styles/variables.scss" as variables;

  .app-wrapper {
    @include mixin.clearfix;
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
    width: calc(100% - #{variables.$sideBarWidth});
    transition: all 0.28s ease;
  }

  .hideSidebar .fixed-header {
    width: calc(100% - 54px)
  }
  .tags-view-container {
    // position: relative;
    height: 40px;
    width: 100%;
    background: #fff;
    border-bottom: 1px solid #e6e6e6;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .08);
    margin-top: 60px;
  }
  .app-main {
    /* 调整内容区域，适应新的header和tagsview高度 */
    min-height: calc(100vh - 90px);
    height: 100%;
    width: 100%;
    position: relative;
    overflow: auto;
    padding: 15px;
    // margin-top: 90px;
    transition: all 0.3s ease;
  }
  .mobile .fixed-header {
    width: 100%;
  }
</style>
