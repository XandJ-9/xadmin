<template>
  <div class="interface-query-log-container">
    <div class="filter-container">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="接口编码">
          <el-input v-model="filterForm.interface_code" placeholder="请输入接口编码" style="width: 200px" />
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

    <el-table :data="logData" style="width: 100%" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="interface_code" label="接口编码" width="150"></el-table-column>
      <el-table-column prop="creator_name" label="创建用户" width="120"></el-table-column>
      <el-table-column prop="execute_time" label="执行时间(ms)" width="120"></el-table-column>
      <el-table-column prop="interface_sql" label="SQL语句">
        <template #default="scope">
          <el-tooltip 
            class="box-item" 
            effect="dark" 
            :content="scope.row.interface_sql" 
            placement="top-start"
            :hide-after="0"
          >
            <div class="sql-content">{{ scope.row.interface_sql }}</div>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="execute_result" label="执行结果" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.execute_result === 'success' ? 'success' : 'danger'">
            {{ scope.row.execute_result === 'success' ? '成功' : '失败' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="execute_start_time" label="开始时间" width="180"></el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="scope">
          <el-button 
            type="primary" 
            link 
            @click="viewQueryDetail(scope.row)"
          >
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total">
      </el-pagination>
    </div>

    <!-- 查询详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="查询详情"
      width="50%"
    >
      <div class="query-detail">
        <div class="detail-item">
          <span class="label">接口编码：</span>
          <span>{{ currentQuery.interface_code }}</span>
        </div>
        <div class="detail-item">
          <span class="label">创建用户：</span>
          <span>{{ currentQuery.creator_name }}</span>
        </div>
        <div class="detail-item">
          <span class="label">开始时间：</span>
          <span>{{ currentQuery.execute_start_time }}</span>
        </div>
        <div class="detail-item">
          <span class="label">结束时间：</span>
          <span>{{ currentQuery.execute_end_time }}</span>
        </div>
        <div class="detail-item">
          <span class="label">执行时间：</span>
          <span>{{ currentQuery.execute_time }}ms</span>
        </div>
        <div class="detail-item">
          <span class="label">执行结果：</span>
          <el-tag :type="currentQuery.execute_result === 'success' ? 'success' : 'danger'">
            {{ currentQuery.execute_result === 'success' ? '成功' : '失败' }}
          </el-tag>
        </div>
        <div class="detail-item full-width">
          <span class="label">SQL语句：</span>
          <div class="sql-code">
            <div class="sql-header">
              <span>SQL</span>
              <el-button type="primary" link size="small" @click="copySql">
                <el-icon><Document /></el-icon> 复制
              </el-button>
            </div>
            <pre><code ref="sqlCodeBlock" class="language-sql">{{ currentQuery.interface_sql }}</code></pre>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import hljs from 'highlight.js/lib/core'
import sql from 'highlight.js/lib/languages/sql'
import 'highlight.js/styles/atom-one-dark.css'
import { Document } from '@element-plus/icons-vue'

// 注册SQL语言高亮
hljs.registerLanguage('sql', sql)

// 过滤表单
const filterForm = ref({
  interface_code: '',
  dateRange: []
})

// 表格数据
const logData = ref([])
const loading = ref(false)

// 分页
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 详情对话框
const dialogVisible = ref(false)
const currentQuery = ref({})
const sqlCodeBlock = ref(null)

// 获取日志数据
const fetchLogs = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.currentPage,
      page_size: pagination.value.pageSize,
      interface_code: filterForm.value.interface_code || undefined
    }
    
    // 添加日期范围过滤
    if (filterForm.value.dateRange && filterForm.value.dateRange.length === 2) {
      const startDate = filterForm.value.dateRange[0]
      const endDate = filterForm.value.dateRange[1]
      if (startDate) {
        params.start_time = startDate.toISOString().split('T')[0]
      }
      if (endDate) {
        params.end_time = endDate.toISOString().split('T')[0]
      }
    }
    
    const response = await request.get('/api/report/interface-query-logs/', { params })
    logData.value = response.data.results
    pagination.value.total = response.data.count
  } catch (error) {
    console.error('获取接口查询日志失败:', error)
    ElMessage.error('获取接口查询日志失败')
  } finally {
    loading.value = false
  }
}

// 查看详情
const viewQueryDetail = async (row) => {
  try {
    const response = await request.get(`/api/report/interface-query-logs/${row.id}/`)
    currentQuery.value = response.data
    dialogVisible.value = true
    
    // 等待DOM更新后应用代码高亮
    nextTick(() => {
      if (sqlCodeBlock.value) {
        hljs.highlightElement(sqlCodeBlock.value)
      }
    })
  } catch (error) {
    console.error('获取查询详情失败:', error)
    ElMessage.error('获取查询详情失败')
  }
}

// 复制SQL
const copySql = () => {
  if (currentQuery.value.interface_sql) {
    navigator.clipboard.writeText(currentQuery.value.interface_sql)
      .then(() => {
        ElMessage.success('SQL已复制到剪贴板')
      })
      .catch(() => {
        ElMessage.error('复制失败')
      })
  }
}

// 搜索日志
const searchLogs = () => {
  pagination.value.currentPage = 1
  fetchLogs()
}

// 重置过滤器
const resetFilter = () => {
  filterForm.value = {
    interface_code: '',
    dateRange: []
  }
  searchLogs()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  fetchLogs()
}

const handleCurrentChange = (page) => {
  pagination.value.currentPage = page
  fetchLogs()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
.interface-query-log-container {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.sql-content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400px;
}

.query-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.detail-item {
  width: calc(50% - 15px);
  display: flex;
  align-items: flex-start;
}

.detail-item.full-width {
  width: 100%;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 80px;
}

.sql-code {
  width: 100%;
  background-color: #282c34;
  border-radius: 4px;
  overflow: hidden;
}

.sql-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #21252b;
  color: #fff;
}

.sql-code pre {
  margin: 0;
  padding: 12px;
  overflow-x: auto;
  max-height: 300px;
}

.error-box {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 10px;
  border-radius: 4px;
  width: 100%;
  overflow-x: auto;
}

.error-box pre {
  margin: 0;
  white-space: pre-wrap;
}

.result-preview {
  width: 100%;
  margin-top: 10px;
}

.result-info {
  margin-top: 10px;
  color: #909399;
  font-size: 12px;
}
</style>