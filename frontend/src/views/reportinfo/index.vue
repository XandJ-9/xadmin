<template>
  <div class="report-info-container">
    <router-view />
  </div>
</template>

<script setup>
// 该组件作为报表信息的容器组件，通过router-view渲染子路由内容
</script>

<style scoped>
.report-info-container {
  padding: 20px;
}
</style>