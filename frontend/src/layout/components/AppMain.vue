<template>
  <section class="app-main" >
  <router-view v-slot="{ Component, route }">
      <transition name="fade-transform" mode="out-in">
        <keep-alive>
          <component :is="Component" :key="route.path"/>
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>

<script setup>
import { useTagsViewStore } from '@/store/modules/tagsView'

const tagsViewStore = useTagsViewStore()


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