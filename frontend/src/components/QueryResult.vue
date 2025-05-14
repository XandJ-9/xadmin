<template>
  <div class="query-result" v-loading="loading">
    <div v-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon />
    </div>
    <div v-else-if="queryResult.length > 0" class="result-container">
      <el-table 
        :data="paginatedData" 
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
          sortable
          show-overflow-tooltip
        >
          <template #default="scope">
            <span>{{ formatCellValue(scope.row[column]) }}</span>
          </template>
        </el-table-column>
      </el-table>
      <div class="card-footer">
        <Pagination
          :total="queryResult.length"
          :current-page="currentPage"
          :page-size="pageSize"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
    <div v-else-if="!loading" class="empty-result">
      <el-empty description="暂无查询结果" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Pagination from '@/components/Pagination.vue'

const props = defineProps({
  queryResult: {
    type: Array,
    default: () => []
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
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return props.queryResult.slice(start, end)
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
</script>

<style scoped>
.query-result {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.result-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 16px;
}

.error-message {
  margin-bottom: 16px;
}

.empty-result {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>