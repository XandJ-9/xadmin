<template>
  <div class="app-container">
    <!-- 报表展示列表 -->
      <splitpanes :horizontal="appStore.device === 'mobile'" class="default-theme">
        <pane min-size="300" size="50">
            <!-- 报表分类信息 -->
             <el-col>

             </el-col>
        </pane>
        <pane>
            <!-- 报表信息 -->
             <el-col>
                
             </el-col>
        </pane>
      </splitpanes>
  </div>
</template>

<script setup name="ReportList">
import { ref } from 'vue'
import useAppStore from '@/store/modules/app'
import { Splitpanes, Pane } from "splitpanes"
import "splitpanes/dist/splitpanes.css"

const appStore = useAppStore()

</script>

<style>

</style>