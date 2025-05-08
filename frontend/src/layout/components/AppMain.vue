<template>
  <section>
        <router-view #default="{ Component, route }">
            <keep-alive :include="tagsViewStore.cachedViews">
                <component :is="Component" :key="route.fullPath"/>
            </keep-alive>
        </router-view>
  </section>
</template>

<script setup>
import { useTagsViewStore } from '@/store/modules/tagsView'

const tagsViewStore = useTagsViewStore()

</script>

<style scoped>





</style>