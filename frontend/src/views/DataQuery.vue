<template>
  <div class="data-query-container">
    <div class="query-header">
      <el-select
        v-model="selectedDataSource"
        placeholder="请选择数据源"
        style="width: 200px"
        @change="handleDataSourceChange"
      >
        <el-option
          v-for="source in dataSources"
          :key="source.id"
          :label="source.name"
          :value="source.id"
        />
      </el-select>
      <el-button type="primary" @click="executeQuery" :loading="loading">执行查询</el-button>
    </div>

    <div class="query-editor">
      <el-input
        v-model="sqlQuery"
        type="textarea"
        :rows="8"
        placeholder="请输入SQL查询语句"
        :spellcheck="false"
      />
    </div>

    <div class="query-result" v-loading="loading">
      <div v-if="error" class="error-message">
        <el-alert :title="error" type="error" show-icon />
      </div>
      <div v-else-if="queryResult.length > 0">
        <el-table 
          :data="paginatedData" 
          style="width: 100%" 
          border 
          stripe
          height="calc(100vh - 400px)"
          @sort-change="handleSortChange"
        >
          <el-table-column
            v-for="column in tableColumns"
            :key="column"
            :prop="column"
            :label="column"
            sortable
            show-overflow-tooltip
          >
            <template #default="scope">
              <span>{{ formatCellValue(scope.row[column]) }}</span>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-container">
          <el-pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="queryResult.length"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
      <div v-else-if="!loading" class="empty-result">
        <el-empty description="暂无查询结果" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const dataSources = ref([])
const selectedDataSource = ref('')
const sqlQuery = ref('')
const queryResult = ref([])
const tableColumns = ref([])
const loading = ref(false)
const error = ref('')

// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return queryResult.value.slice(start, end)
})

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}

const handleSortChange = ({ prop, order }) => {
  if (!prop || !order) return
  
  queryResult.value.sort((a, b) => {
    const valueA = a[prop]
    const valueB = b[prop]
    
    if (order === 'ascending') {
      return valueA < valueB ? -1 : valueA > valueB ? 1 : 0
    } else {
      return valueA > valueB ? -1 : valueA < valueB ? 1 : 0
    }
  })
}

const formatCellValue = (value) => {
  if (value === null || value === undefined) return '-'
  if (value instanceof Date) return value.toLocaleString()
  if (typeof value === 'object') return JSON.stringify(value)
  return value.toString()
}

const fetchDataSources = async () => {
  try {
    const response = await request.get('/api/datasources/')
    dataSources.value = response.data
  } catch (error) {
    ElMessage.error('获取数据源列表失败')
  }
}

const handleDataSourceChange = () => {
  // 清空当前查询结果
  queryResult.value = []
  tableColumns.value = []
  error.value = ''
  currentPage.value = 1
}

const executeQuery = async () => {
  if (!selectedDataSource.value) {
    ElMessage.warning('请选择数据源')
    return
  }

  if (!sqlQuery.value.trim()) {
    ElMessage.warning('请输入SQL查询语句')
    return
  }

  loading.value = true
  error.value = ''
  currentPage.value = 1
  
  try {
    const response = await request.post(`/api/datasources/${selectedDataSource.value}/query/`, {
      sql: sqlQuery.value
    })
    
    if (response.data.total > 0) {
      // 从第一条记录中获取列名
      tableColumns.value = Object.keys(response.data.data[0])
      // dataList = response.data.data
      queryResult.value = response.data.data
    } else {
      queryResult.value = []
      tableColumns.value = []
    }
  } catch (err) {
    error.value = err.response?.data?.message || '查询执行失败'
    queryResult.value = []
    tableColumns.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDataSources()
})
</script>

<style scoped>
.data-query-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: calc(100vh - 120px);
}

.query-header {
  display: flex;
  gap: 16px;
  align-items: center;
}

.query-editor {
  flex: 0 0 auto;
}

.query-result {
  flex: 1;
  overflow: auto;
  background-color: #fff;
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.error-message {
  margin-bottom: 16px;
}

.empty-result {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>