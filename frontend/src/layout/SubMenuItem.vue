<template>
  <el-sub-menu v-if="route.children && route.children.length > 0" :index="route.path">
    <template #title>
      <el-icon v-if="route.meta?.icon">
        <component :is="route.meta.icon" />
      </el-icon>
      <span>{{ route.meta?.title || route.name }}</span>
    </template>
    <template v-for="child in route.children.filter(child => child.meta?.hidden !== true)" :key="child.path">
      <sub-menu :route="child" />
    </template>
  </el-sub-menu>
  <el-menu-item v-else :index="route.path">
    <el-icon v-if="route.meta?.icon">
      <component :is="route.meta.icon" />
    </el-icon>
    <span>{{ route.meta?.title || route.name }}</span>
  </el-menu-item>
</template>

<script setup>
import { onMounted } from 'vue'
import subMenu from './SubMenuItem.vue'
defineProps({
  route: {
    type: Object,
    required: true
  }
})



</script>