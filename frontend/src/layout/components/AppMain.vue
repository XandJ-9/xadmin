<template>
  <section class="app-main" >
        <router-view #default="{ Component, route }" :key="key">
            <keep-alive :include="cachedViews">
                <component :is="Component" :key="route.fullPath"/>
            </keep-alive>
        </router-view>
  </section>
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


.app-main {
  /* 50= navbar  50  */
  min-height: calc(100vh - 50px);
  width: 100%;
  position: relative;
  overflow: hidden;
}


</style>