<template>
  <div class="app-main" >
    
    <el-main>
        <router-view v-slot="{ Component }" :key="key">
            <keep-alive :include="cachedViews">
                <component :is="Component" />
            </keep-alive>
        </router-view>
    </el-main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTagViewsStore } from '@/store/tagviews'
import { useRoute } from 'vue-router'

const tagViewsStore = useTagViewsStore()

// 从visitedViews中提取组件名称，用于keep-alive的include属性
const cachedViews = computed(() => {
  return tagViewsStore.visitedViews.map(view => view.name)
})

// 动态设置组件的key，用于keep-alive的include属性
const route = useRoute()
const key = computed(() => {
  return route.path
})
</script>

<style scoped>



.el-main {
  background-color: #f5f7fa;
  border:none;
  padding: 0;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.app-main {
  height: 100%;
}

</style>