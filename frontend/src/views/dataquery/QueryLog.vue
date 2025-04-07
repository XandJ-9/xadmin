<template>
  <div class="query-log-container">
    <el-card class="box-card">
      <div class="filter-container">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="查询状态">
            <el-select v-model="filterForm.status" placeholder="请选择查询状态" style="width: 200px">
              <el-option label="全部" value=""></el-option>
              <el-option label="成功" value="success"></el-option>
              <el-option label="失败" value="error"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="数据源">
            <el-select v-model="filterForm.dataSourceId" placeholder="请选择数据源" style="width: 200px">
              <el-option label="全部" value=""></el-option>
              <el-option 
                v-for="source in dataSources" 
                :key="source.id" 
                :label="source.name" 
                :value="source.id"
              ></el-option>
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
      
      <el-table :data="logData" style="width: 100%" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="datasource_name" label="数据源" width="120"></el-table-column>
        <el-table-column prop="username" label="查询用户" width="120"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="execution_time" label="执行时间(ms)" width="120"></el-table-column>
        <el-table-column prop="sql" label="SQL语句">
          <template #default="scope">
            <el-tooltip 
              class="box-item" 
              effect="dark" 
              :content="scope.row.sql" 
              placement="top-start"
              :hide-after="0"
            >
              <div class="sql-content">{{ scope.row.sql }}</div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="error_message" label="错误信息">
          <template #default="scope">
            <span v-if="scope.row.status === 'error'" class="error-message">
              {{ scope.row.errorMessage }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="查询时间" width="180"></el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button 
              type="primary" 
              link 
              @click="viewQueryDetail(scope.row)"
            >
              查看详情
            </el-button>
            <el-button 
              type="primary" 
              link 
              @click="reExecuteQuery(scope.row)"
              :disabled="scope.row.status === 'error'"
            >
              重新执行
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
    </el-card>

    <!-- 查询详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="查询详情"
      width="80%"
    >
      <div class="query-detail">
        <div class="detail-item">
          <span class="label">数据源：</span>
          <span>{{ currentQuery.dataSourceName }}</span>
        </div>
        <div class="detail-item">
          <span class="label">查询用户：</span>
          <span>{{ currentQuery.username }}</span>
        </div>
        <div class="detail-item">
          <span class="label">查询时间：</span>
          <span>{{ currentQuery.createTime }}</span>
        </div>
        <div class="detail-item">
          <span class="label">执行时间：</span>
          <span>{{ currentQuery.executionTime }}ms</span>
        </div>
        <div class="detail-item">
          <span class="label">状态：</span>
          <el-tag :type="currentQuery.status === 'success' ? 'success' : 'danger'">
            {{ currentQuery.status === 'success' ? '成功' : '失败' }}
          </el-tag>
        </div>
        <div class="detail-item full-width">
          <span class="label">SQL语句：</span>
          <div class="sql-code">
            <pre>{{ currentQuery.sql }}</pre>
          </div>
        </div>
        <div v-if="currentQuery.status === 'error'" class="detail-item full-width">
          <span class="label">错误信息：</span>
          <div class="error-box">
            <pre>{{ currentQuery.errorMessage }}</pre>
          </div>
        </div>
        <div v-if="currentQuery.status === 'success'" class="detail-item full-width">
          <span class="label">查询结果：</span>
          <div class="result-preview">
            <el-table :data="currentQuery.resultPreview" border>
              <el-table-column 
                v-for="column in currentQuery.resultColumns" 
                :key="column" 
                :prop="column" 
                :label="column">
              </el-table-column>
            </el-table>
            <div class="result-info" v-if="currentQuery.resultTotal > 0">
              共 {{ currentQuery.resultTotal }} 条记录，显示前 {{ Math.min(currentQuery.resultPreview.length, 10) }} 条
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button 
            type="primary" 
            @click="reExecuteQuery(currentQuery)"
            :disabled="currentQuery.status === 'error'"
          >
            重新执行
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { useRouter } from 'vue-router'

const router = useRouter()

// 过滤表单
const filterForm = ref({
  status: '',
  dataSourceId: '',
  dateRange: []
})

// 分页信息
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 数据源列表
const dataSources = ref([])

// 日志数据
const logData = ref([])
const loading = ref(false)

// 查询详情对话框
const dialogVisible = ref(false)
const currentQuery = ref({
  id: 0,
  dataSourceName: '',
  username: '',
  status: '',
  executionTime: 0,
  sql: '',
  errorMessage: '',
  createTime: '',
  resultPreview: [],
  resultColumns: [],
  resultTotal: 0
})

// 获取数据源列表
const fetchDataSources = async () => {
  try {
    const response = await request.get('/api/datasources/')
    dataSources.value = response.data
  } catch (error) {
    ElMessage.error('获取数据源列表失败')
  }
}

// 查询日志
const searchLogs = async () => {
  loading.value = true
  try {
    // 构建查询参数
    const params = {
      page: pagination.value.currentPage,
      page_size: pagination.value.pageSize,
      status: filterForm.value.status,
      datasource_id: filterForm.value.dataSourceId
    }
    
    // 添加日期范围参数
    if (filterForm.value.dateRange && filterForm.value.dateRange.length === 2) {
      params.start_date = filterForm.value.dateRange[0].toISOString().split('T')[0]
      params.end_date = filterForm.value.dateRange[1].toISOString().split('T')[0]
    }
    
    const response = await request.get('/api/querylogs/', { params })
    logData.value = response.data.data.data
    pagination.value.total = response.data.data.total
  } catch (error) {
    ElMessage.error('获取查询日志失败')
  } finally {
    loading.value = false
  }
}

// 重置过滤条件
const resetFilter = () => {
  filterForm.value = {
    status: '',
    dataSourceId: '',
    dateRange: []
  }
  pagination.value.currentPage = 1
  searchLogs()
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

// 查看查询详情
const viewQueryDetail = async (row) => {
  try {
    const response = await request.get(`/api/datasources/query-logs/${row.id}/`)
    currentQuery.value = {
      ...response.data,
      dataSourceName: row.dataSourceName,
      resultPreview: response.data.result_preview || [],
      resultColumns: response.data.result_columns || [],
      resultTotal: response.data.result_total || 0
    }
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取查询详情失败')
  }
}

// 重新执行查询
const reExecuteQuery = (row) => {
  // 跳转到数据查询页面并填充SQL
  router.push({
    path: '/dataquery/index',
    query: {
      datasource_id: row.datasource_id,
      sql: row.sql
    }
  })
}

onMounted(() => {
  // 组件挂载时加载数据
  fetchDataSources()
  searchLogs()
})
</script>

<style scoped>
.query-log-container {
  padding: 20px;
}

.box-card {
  margin-top: 20px;
}

.filter-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.sql-content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

.error-message {
  color: #f56c6c;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.query-detail {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  width: calc(33% - 16px);
}

.full-width {
  width: 100%;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-weight: bold;
  margin-right: 8px;
  min-width: 80px;
}

.sql-code, .error-box {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 12px;
  width: 100%;
  overflow-x: auto;
}

.sql-code pre, .error-box pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.error-box {
  background-color: #fef0f0;
  color: #f56c6c;
}

.result-preview {
  width: 100%;
  margin-top: 8px;
}

.result-info {
  margin-top: 8px;
  color: #909399;
  font-size: 12px;
}
</style>