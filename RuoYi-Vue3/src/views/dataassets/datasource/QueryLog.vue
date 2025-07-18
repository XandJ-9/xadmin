<template>
  <div class="app-container">
  
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
                v-for="source in dataSourcesOptions" 
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
        <el-table-column prop="sql" label="SQL语句" show-overflow-tooltip>
          <template #default="scope">
            <!-- <el-tooltip  -->
              <!-- class="box-item"  -->
              <!-- effect="dark"  -->
              <!-- :content="scope.row.sql"  -->
              <!-- placement="top-start" -->
              <!-- :hide-after="0" -->
            <!-- > -->
              <div class="sql-content">{{ scope.row.sql }}</div>
            <!-- </el-tooltip> -->
          </template>
        </el-table-column>
        <el-table-column prop="error_message" label="错误信息" show-overflow-tooltip>
          <template #default="scope">
            <!-- <el-tooltip -->
              <!-- class="box-item" -->
              <!-- effect="dark" -->
              <!-- :content="scope.row.error_message" -->
              <!-- placement="top-start" -->
              <!-- :hide-after="0" -->
              <!-- > -->
              <span v-if="scope.row.status === 'error'" class="error-message">
              {{ scope.row.error_message }}
              </span>
              <span v-else>-</span>
            <!-- </el-tooltip> -->

          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="查询时间" width="180"></el-table-column>
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

    <pagination v-show="pageInfo.total > 0" 
      :total="pageInfo.total"
      v-model:page="pageInfo.currentPage" 
      v-model:limit="pageInfo.pageSize" 
      @pagination="searchLogs"
    />

    <!-- 查询详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="查询详情"
      width="50%"
    >
      <div class="query-detail">
        <!-- <div class="detail-item">
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
        </div> -->
        <div class="detail-item">
          <span class="label">状态：</span>
          <el-tag :type="currentQuery.status === 'success' ? 'success' : 'danger'">
            {{ currentQuery.status === 'success' ? '成功' : '失败' }}
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
            <pre><code ref="sqlCodeBlock" class="language-sql">{{ currentQuery.sql }}</code></pre>
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
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="QueryLog">
import { ref, onMounted, nextTick, watch, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import hljs from 'highlight.js/lib/core'
import sql from 'highlight.js/lib/languages/sql'
import 'highlight.js/styles/atom-one-dark.css'
import { Document } from '@element-plus/icons-vue'

import { getQueryLogs, getQueryLogDetail } from '@/api/dataassets/datasource'
import { getDataSourceList } from '@/api/dataassets/datasource'

// 注册SQL语言高亮
hljs.registerLanguage('sql', sql)

const router = useRouter()

// 过滤表单
const filterForm = ref({
  status: '',
  dataSourceId: '',
  dateRange: []
})

// 分页信息
const pageInfo = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 数据源列表
const dataSourcesOptions = ref([])

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

// SQL代码块引用
const sqlCodeBlock = ref(null)

// 复制SQL功能
const copySql = () => {
  if (currentQuery.value.sql) {
    navigator.clipboard.writeText(currentQuery.value.sql)
      .then(() => {
        ElMessage.success('SQL已复制到剪贴板')
      })
      .catch(() => {
        ElMessage.error('复制失败，请手动复制')
      })
  }
}

// 监听对话框显示状态，当对话框显示时应用代码高亮
watch(dialogVisible, (newVal) => {
    if (newVal && sqlCodeBlock.value) {
    sqlCodeBlock.value.dataset.highlighted = "no"
    nextTick(() => {
      hljs.highlightElement(sqlCodeBlock.value)
    })
  }
})

// 获取数据源列表
const fetchDataSources = async () => {
    getDataSourceList().then((response) => { 
    dataSourcesOptions.value = response
    })
}

// 查询日志
const searchLogs = async () => {
  loading.value = true
  try {
    // 构建查询参数
    const params = {
      pageNum: pageInfo.currentPage,
      pageSize: pageInfo.pageSize,
      status: filterForm.value.status,
      datasource_id: filterForm.value.dataSourceId
    }
    
    // 添加日期范围参数
    if (filterForm.value.dateRange && filterForm.value.dateRange.length === 2) {
      params.start_date = filterForm.value.dateRange[0].toISOString().split('T')[0]
      params.end_date = filterForm.value.dateRange[1].toISOString().split('T')[0]
    }
    
    await getQueryLogs(params).then(res => {
          logData.value = res.data
          pageInfo.total = res.total
    })
  } catch (error) {
    // ElMessage.error('获取查询日志失败')
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
  pageInfo.currentPage = 1
  searchLogs()
}

// 处理每页显示数量变化
const handleSizeChange = (size) => {
  pageInfo.pageSize = size
  searchLogs()
}

// 处理页码变化
const handleCurrentChange = (page) => {
  pageInfo.currentPage = page
  searchLogs()
}

// 查看查询详情
const viewQueryDetail = async (row) => {
  try {
    const response = await getQueryLogDetail(row.id)
    const result = response.data
    currentQuery.value = {
      id: result.id,
      dataSourceName: result.datasource_name,
      username: result.username,
      status: result.status,
      executionTime: result.execution_time,
      sql: result.sql,
      errorMessage: result.error_message,
      createTime: result.create_time,
      // resultPreview: response.data.result_preview || [],
      // resultColumns: result.result_columns || [],
      // resultTotal: result.result_total || 0
    }
    dialogVisible.value = true
    
    // 在对话框显示后应用代码高亮
    nextTick(() => {
        if (sqlCodeBlock.value) {
        hljs.highlightElement(sqlCodeBlock.value)
      }
    })
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


/* .box-card {
  margin-top: 20px;
}

.filter-container {
  margin-bottom: 20px;
} */

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
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  /* width: calc(33% - 16px); */
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
  background-color: #282c34;
  border-radius: 6px;
  width: 100%;
  overflow-x: auto;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 8px;
}

.sql-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background-color: #21252b;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
  border-bottom: 1px solid #3e4451;
}

.sql-header span {
  font-size: 12px;
  font-weight: bold;
  color: #abb2bf;
}

.sql-code pre {
  margin: 0;
  padding: 16px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Fira Code', 'Consolas', 'Monaco', 'Andale Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
}

.sql-code code {
  background: transparent;
  padding: 0;
  border-radius: 0;
  color: #abb2bf;
}


.error-box pre {
  margin: 0;
  padding: 5px;
  white-space: pre-wrap;
  word-break: break-word;
  color: #e06c75;
  font-family: 'Fira Code', 'Consolas', 'Monaco', 'Andale Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  overflow-x: auto;
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