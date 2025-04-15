<template>
  <div class="layout-container">
    <Sidebar :is-collapse="isCollapse" :sidebar-width="sidebarWidth"/>
    <div class="main-container" :style="{ width: mainWidth}">
    <el-header>
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
    <tag-view />
    <app-main/>
  </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
import AppMain from './components/AppMain.vue'
import { ref, computed, provide, onMounted } from 'vue'
import TagView from './components/TagView.vue'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const isCollapse = ref(false)
const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')
const username = ref('')

const userStore = useUserStore()

onMounted(() => {
  // const user = localStorage.getItem('user')
  // if (user) {
  //   const userData = JSON.parse(user)
  //   username.value = userData.username
  // }
  username.value = userStore.getUserInfo.username
})


const mainWidth = computed(() => {
  // return `calc(100vw - ${sidebarWidth})`
  return isCollapse.value? 'calc(100vw - 64px)' : 'calc(100vw - 200px)'
})


const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleLogout = () => {
  localStorage.removeItem('token')
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

.el-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.fold-btn {
  font-size: 20px;
  cursor: pointer;
  color: #303133;
}

.fold-btn:hover {
  color: #409EFF;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  cursor: pointer;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  color: #303133;
}

.main-container {
  position: fixed;
  right: 0;
  top: 0;
  transition: width 0.3s;
  width: 100%;
  
}
</style>