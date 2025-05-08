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
import { useRoute } from 'vue-router'
import { useTagsViewStore } from '@/store/modules/tagsView'

const tagsViewStore = useTagsViewStore()

// 从visitedViews中提取组件名称，用于keep-alive的include属性
const cachedViews = computed(() => {
  return tagsViewStore.cachedViews
})

</script>

<style scoped>


.app-main {
  /* 调整内容区域，适应新的header和tagsview高度 */
  min-height: calc(100vh - 90px);
  height: 100%;
  width: 100%;
  position: relative;
  overflow: auto;
  padding: 15px;
  margin-top: 90px;
  transition: all 0.3s ease;
}


</style>