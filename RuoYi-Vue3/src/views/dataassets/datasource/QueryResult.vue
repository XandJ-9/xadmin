<template>
  <div class="query-result" v-loading="loading">
    <div v-if="error" class="error-container">
      <el-alert :title="error" type="error" show-icon />
    </div>
    <div v-else-if="queryResult.length > 0" class="result-container">
      <div class="pagination-container">
        <pagination
          :total="total"
          v-model:page="currentPage" 
          v-model:limit="pageSize" 
          @pagination="paginatedData"
        />
      </div>
      <div class="table-container">
        <el-table 
          :data="data" 
          style="width: 100%" 
          border 
          stripe
          @sort-change="handleSortChange"
        >
          <el-table-column
            v-for="column in tableColumns"
            :key="column"
            :prop="column"
            :label="column"
            :width="columnWidth(column)" 
            sortable
            show-overflow-tooltip
          >
            <template #default="scope">
              <span>{{ formatCellValue(scope.row[column]) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>


    </div>
    <div v-else-if="!loading" class="empty-container">
      <el-empty description="暂无查询结果" />
    </div>
  </div>
</template>

<script setup name="QueryResult">
import { ref, computed, onMounted, inject } from 'vue'
import { defineProps } from 'vue'

const calculateColumnWidth = inject('calculateColumnWidth')

const props = defineProps({
  queryResult: {
    type: Array,
    default: () => []
  },
  total: {
    type: Number,
    default: 0
  },
  tableColumns: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)
const data = ref([])

const paginatedData = () => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  data.value = props.queryResult.slice(start, end)
}

const handleSortChange = ({ prop, order }) => {
  if (!prop || !order) return
  
  props.queryResult.sort((a, b) => {
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

// 根据列名计算列宽度
const columnWidth = (columnName) => {
  return calculateColumnWidth(columnName, {})
}

onMounted(() => { 
  paginatedData()
})
</script>

<style scoped>
/* 核心容器 - 占满父容器高度 */
.query-result {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  /* overflow: hidden; */
}

/* 结果容器 - 使用flex布局确保分页在底部 */
.result-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  margin: 0;
}

/* 表格容器 - 自动填充剩余空间 */
.table-container {
  flex: 1; /* 关键：占满剩余空间 */
  overflow: auto; /* 内容超出时可滚动 */
  padding-bottom: 10px;
  box-sizing: border-box;
  min-height: 100px; /* 确保表格区域不会过小 */
  /* height: 70%; */
  height: calc(100% - 50px);
}

/* 移除表格固定高度，由容器自动控制 */
:deep(.el-table) {
  width: 100%;
  height: 100%; /* 表格占满容器高度 */
}

/* 分页容器 - 固定在底部 */
.pagination-container {
  margin: 0px;
  padding: 0px 16px;
  background-color: #fafafa;
  /* border-top: 1px solid #e4e7ed; */
  display: flex;
  justify-content: flex-end;
  align-items: center;
  box-sizing: border-box;
  width: 100%;
  /* 固定高度确保分页区域不会伸缩 */
  height: 30px;
}

/* 错误提示容器 */
.error-container {
  padding: 16px;
  box-sizing: border-box;
}

/* 空状态容器 - 居中显示 */
.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 20px;
}

/* 处理加载状态的覆盖层位置 */
:deep(.el-loading-mask) {
  height: 100%;
  width: 100%;
}
</style>
