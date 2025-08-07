<template>
  <div class="query-result" v-loading="loading">
    <div v-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon />
    </div>
    <div v-else-if="queryResult.length > 0" class="result-container">
      <div class="table-container">
      <el-table 
        :data="data" 
        style="width: 100%" 
        height="calc(100% - 100px)"
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

      <div class="pagination-container">
        <pagination
        :total="total"
        v-model:page="currentPage" 
        v-model:limit="pageSize" 
        @pagination="paginatedData"
        />
      </div>

    </div>
    <div v-else-if="!loading" class="empty-result">
      <el-empty description="暂无查询结果" />
    </div>
  </div>
</template>

<script setup name="QueryResult">
import { ref, computed, onMounted } from 'vue'


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

// 根据列名计算列宽度
const columnWidth = (columnName) => {
    return calculateColumnWidth(columnName, {})
}

onMounted(() => { 
    paginatedData()
})

</script>

<style scoped>
/* .query-result {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: auto;
} */

/* .result-container {
  display: flex;
  flex-direction: column;
 gap: 16px;
} */

.error-message {
  margin-bottom: 16px;
}

.empty-result {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}


/* 结果表格容器 */
.table-container {
  flex: 1;
  overflow: auto; /* 表格内容滚动 */
  padding: 12px;
  box-sizing: border-box;
  height: calc(100% - 100px);
}

/* 分页控件容器 */
.pagination-container {
  padding: 12px;
  border-top: 1px solid #e4e7ed;
  background-color: #fafafa;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  box-sizing: border-box;
}
</style>