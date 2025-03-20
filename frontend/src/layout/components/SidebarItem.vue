<template>
  <el-sub-menu v-if="hasChildren" :index="resolvePath(route.path)">
    <template #title>
      <el-icon v-if="route.meta?.icon">
        <component :is="route.meta.icon" />
      </el-icon>
      <span>{{ route.meta?.title || route.name }}</span>
    </template>
    <template v-for="child in visibleChildren" :key="child.path">
      <sidebar-item :route="child" :base-path="resolvePath(route.path)" />
    </template>
  </el-sub-menu>
  <el-menu-item v-else :index="resolvePath(route.path)">
    <el-icon v-if="route.meta?.icon">
      <component :is="route.meta.icon" />
    </el-icon>
    <span>{{ route.meta?.title || route.name }}</span>
  </el-menu-item>
</template>

<script setup>
import { computed } from 'vue'
import path from 'path'

const props = defineProps({
  route: {
    type: Object,
    required: true,
    validator: (value) => {
      return value && typeof value.path === 'string'
    }
  },
  basePath: {
    type: String,
    default: ''
  }
})

const hasChildren = computed(() => {
  return props.route.children && props.route.children.length > 0
})

const visibleChildren = computed(() => {
  return props.route.children?.filter(child => child.hidden !== true) || []
})

const resolvePath = (routePath) => {
  if (routePath.startsWith('/')) {
    return routePath
  }
  return path.resolve(props.basePath, routePath)
}
</script>

<style scoped>
.el-menu-item, :deep(.el-sub-menu__title) {
  display: flex;
  align-items: center;
  gap: 8px;
}

.el-icon {
  flex-shrink: 0;
  margin-right: 4px;
}

span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>