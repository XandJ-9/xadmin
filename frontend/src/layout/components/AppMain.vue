<template>
  <section class="app-main" >
        <router-view #default="{ Component, route }">
            <keep-alive :include="tagsViewStore.cachedViews">
                <component :is="Component" :key="route.path"/>
            </keep-alive>
        </router-view>
  </section>
</template>

<script setup>
import { useTagsViewStore } from '@/store/modules/tagsView'

const tagsViewStore = useTagsViewStore()

// 从visitedViews中提取组件名称，用于keep-alive的include属性

</script>

<style scoped>


.app-main {
    /* min-height: calc(100vh - 100px); */
    height: calc(100vh - 120px);
    margin-top: 100px;
    box-sizing: border-box;
    transition: all 0.3s ease;
    overflow: auto;
}

</style>