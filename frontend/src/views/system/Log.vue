<template>
  <div class="system-log-container">
      <div class="filter-container">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="日志类型" style="width: 20%;">
            <el-select v-model="filterForm.logType" placeholder="请选择日志类型">
              <el-option label="全部" value=""></el-option>
              <el-option label="登录日志" value="login"></el-option>
              <el-option label="操作日志" value="operation"></el-option>
              <el-option label="系统日志" value="system"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="filterForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchLogs">查询</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="logData" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="type" label="日志类型" width="120"></el-table-column>
        <el-table-column prop="username" label="操作用户" width="120"></el-table-column>
        <el-table-column prop="ip" label="IP地址" width="120"></el-table-column>
        <el-table-column prop="content" label="日志内容"></el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180"></el-table-column>
      </el-table>
      
      <div class="card-footer">
        <Pagination
          :total="pagination.total"
          :current-page="pagination.currentPage"
          :page-size="pagination.pageSize"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
  </div>
</template>

<script>
export default {
    name: 'SysLog',
}
</script>

<script setup>
import { ref, onMounted } from 'vue'
import Pagination from '@/components/Pagination.vue'

// 过滤表单
const filterForm = ref({
  logType: '',
  dateRange: []
})

// 分页信息
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 日志数据
const logData = ref([
  {
    id: 1,
    type: '登录日志',
    username: 'admin',
    ip: '192.168.1.1',
    content: '用户登录成功',
    createTime: '2023-01-01 12:00:00'
  },
  {
    id: 2,
    type: '操作日志',
    username: 'admin',
    ip: '192.168.1.1',
    content: '修改系统配置',
    createTime: '2023-01-01 13:30:00'
  },
  {
    id: 3,
    type: '系统日志',
    username: 'system',
    ip: '127.0.0.1',
    content: '系统定时任务执行',
    createTime: '2023-01-01 14:00:00'
  }
])

// 查询日志
const searchLogs = () => {
  // 这里添加查询日志的逻辑
  // console.log('查询条件:', filterForm.value)
  // 模拟查询后更新分页信息
  pagination.value.total = 100
}

// 重置过滤条件
const resetFilter = () => {
  filterForm.value = {
    logType: '',
    dateRange: []
  }
}

// 处理每页显示数量变化
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  searchLogs()
}

// 处理页码变化
const handleCurrentChange = (page) => {
  pagination.value.currentPage = page
  searchLogs()
}

onMounted(() => {
  // 组件挂载时加载日志数据
  searchLogs()
})
</script>

<style scoped>
.system-log-container {
  padding: 20px;
}

/* .filter-container {
  margin-bottom: 20px;
} */


</style>