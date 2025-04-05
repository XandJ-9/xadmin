<template>
  <el-container class="main-container" :style="{ width: mainWidth }">
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
    
    <keep-alive>
      <tag-view />
    </keep-alive>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { computed, ref, onMounted } from 'vue'
import TagView from './TagView.vue'
import { useUserStore } from '@/store/user'
const props = defineProps({
  isCollapse: {
    type: Boolean,
    required: true
  },
  sidebarWidth: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:isCollapse'])

const router = useRouter()
const username = ref('管理员')

onMounted(() => {
  const user = localStorage.getItem('user')
  if (user) {
    const userData = JSON.parse(user)
    username.value = userData.username
  }
})

const mainWidth = computed(() => {
  return `calc(100vw - ${props.sidebarWidth})`
})

const toggleCollapse = () => {
  console.log('toggleCollapse',props.isCollapse)
  emit('update:isCollapse', !props.isCollapse)
}

const handleLogout = () => {
  localStorage.removeItem('token')
  const userStore = useUserStore()
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
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
  border: 1px solid #e6e6e6;
  padding: 0;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.main-container {
  position: fixed;
  right: 0;
  top: 0;
  transition: width 0.3s;
}
</style>