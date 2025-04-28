<template>
  <div class="app-main" >
    
    <el-main>
        <router-view v-slot="{ Component }">
            <keep-alive>
                <component :is="Component" />
            </keep-alive>
        </router-view>
    </el-main>
  </div>
</template>

<script setup>

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