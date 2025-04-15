<script setup>
// App.vue作为根组件，只需要提供一个路由出口
</script>

<template>
  <router-view />
</template>

<style>
/* 全局样式 */
html,body{
  width: 100% !important;
  height: 100%;
  overflow: hidden;
  margin: 0;
}
#app{
  width: 100%;
  height: 100%;
  overflow-y: auto;
  max-width: none !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>