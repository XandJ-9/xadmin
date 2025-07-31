<template>
  <div class="app-container">
    <!-- <div class="filter-container"> -->
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
    <!-- </div> -->

    <el-table :data="pageInfo.data" style="width: 100%" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="interface_code" label="接口编码" :width="getInterfaceCodeWidth">
        <template #default="scope">
          <span>{{ scope.row.interface_code }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="creator_username" label="创建用户" width="120"></el-table-column>
      <el-table-column prop="execute_time" label="执行时间(ms)" width="120"></el-table-column>
      <el-table-column prop="interface_sql" label="SQL语句">
        <template #default="scope">
          <!-- <el-tooltip 
            class="box-item" 
            effect="dark" 
            :content="scope.row.interface_sql" 
            placement="top-start"
            :hide-after="0"
          > -->
            <div class="sql-content">{{ scope.row.interface_sql }}</div>
          <!-- </el-tooltip> -->
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
    
    <!-- <div class="card-footer">
      <Pagination
        :total="pageInfo.total"
        v-model:current-page="pageInfo.currentPage"
        v-model:page-size="pageInfo.pageSize"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div> -->
    <pagination v-show="pageInfo.total > 0" 
      :total="pageInfo.total" 
      v-model:page="pageInfo.currentPage" 
      v-model:limit="pageInfo.pageSize" 
      @pagination="fetchData" />

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
          <span>{{ currentQuery.creator_username }}</span>
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
        <div class="detail-item full-width" v-if="currentQuery.execute_result === 'error'">
          <span class="label">错误信息：</span>
          <div class="error-box">
            <pre>{{ currentQuery.error_message}}</pre>
          </div>
        </div>
        <div class="detail-item full-width">
          <span class="label">查询参数：</span>
          <div class="json-code">
            <div class="sql-header">
              <span>JSON</span>
              <el-button type="primary" link size="small" @click="copyText(currentQuery.query_params)">
                <el-icon><Document /></el-icon> 复制
              </el-button>
            </div>
            <pre><code ref="jsonParamsBlock" class="language-json">{{ formatJsonParams }}</code></pre>
          </div>
        </div>
        <div class="detail-item full-width">
          <span class="label">SQL语句：</span>
          <div class="sql-code">
            <div class="sql-header">
              <span>SQL</span>
              <el-button type="primary" link size="small" @click="copyText(currentQuery.interface_sql)">
                <el-icon><Document /></el-icon> 复制
              </el-button>
            </div>
            <pre><code ref="sqlCodeBlock" class="language-sql">{{ currentQuery.interface_sql }}</code></pre>
          </div>
        </div>
        <div class="detail-item full-width">
          <span class="label">合计SQL语句：</span>
          <div class="sql-code">
            <div class="sql-header">
              <span>SQL</span>
              <el-button type="primary" link size="small" @click="copyText(currentQuery.interface_total_sql)">
                <el-icon><Document /></el-icon> 复制
              </el-button>
            </div>
            <pre><code ref="sqlCodeBlock" class="language-sql">{{ currentQuery.interface_total_sql }}</code></pre>
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


<script setup name="InterfaceQueryLog">
import { reactive, ref, onMounted, nextTick, computed, inject } from 'vue'
import { ElMessage } from 'element-plus'
import hljs from 'highlight.js/lib/core'
import sql from 'highlight.js/lib/languages/sql'
import json from 'highlight.js/lib/languages/json'
import 'highlight.js/styles/atom-one-dark.css'
import { Document } from '@element-plus/icons-vue'
// import Pagination from '@/components/Pagination'
import { getInterfaceQueryLogs, getInterfaceQueryLogDetail } from '@/api/dataassets/reportinfo'

// 注入计算列宽方法
const calculateColumnWidth = inject('calculateColumnWidth')
// 注册SQL和JSON语言高亮支持
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('json', json)

// 过滤表单
// 表单相关的多个字段用 reactive
const filterForm = reactive({
  interface_code: '',
  dateRange: []
})

// 表格数据
const logData = ref([])
const loading = ref(false)

// 分页
const pageInfo = reactive({
  data: [],
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 详情对话框
const dialogVisible = ref(false)
const currentQuery = ref({})
const sqlCodeBlock = ref(null)
const jsonParamsBlock = ref(null)

// 获取日志数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      pageNum: pageInfo.currentPage,
      pageSize: pageInfo.pageSize,
      interfaceCode: filterForm.interface_code || undefined
    }
    
    // 添加日期范围过滤
    if (filterForm.dateRange && filterForm.dateRange.length === 2) {
      const startDate = filterForm.dateRange[0]
      const endDate = filterForm.dateRange[1]
      if (startDate) {
        params.start_time = startDate.toISOString().split('T')[0]
      }
      if (endDate) {
        params.end_time = endDate.toISOString().split('T')[0]
      }
    }
    
      await getInterfaceQueryLogs(params).then(response => {
        pageInfo.data = response.data
        pageInfo.total = response.total
      }
    )

  } catch (error) {
    ElMessage.error('获取接口查询日志失败')
  } finally {
    loading.value = false
  }
}

// 查看详情
// 查看详情
const viewQueryDetail = async (row) => {
  try {
    const response = await getInterfaceQueryLogDetail(row.id)
    currentQuery.value = response.data
    dialogVisible.value = true
    
    // 等待DOM更新后应用代码高亮
    nextTick(() => {
      if (sqlCodeBlock.value) {
        hljs.highlightElement(sqlCodeBlock.value)
      }
      if (jsonParamsBlock.value) {
        hljs.highlightElement(jsonParamsBlock.value)
      }
    })
  } catch (error) {
    console.error('获取查询详情失败:', error)
    ElMessage.error('获取查询详情失败')
  }
}

// 复制SQL
// const copySql = () => {
//   if (currentQuery.value.interface_sql) {
//     navigator.clipboard.writeText(currentQuery.value.interface_sql)
//       .then(() => {
//         ElMessage.success('SQL已复制到剪贴板')
//       })
//       .catch(() => {
//         ElMessage.error('复制失败')
//       })
//   }
// }

const copyText = (text) => {
        if (window.isSecureContext && navigator.clipboard) {
            navigator.clipboard.writeText(text)
                .then(() => {
                    ElMessage.success('复制成功')
                })
                .catch(() => {
                    ElMessage.error('复制失败，请手动复制')
                })
        } else {
            try {
                const textarea = document.createElement("textarea");
                textarea.value = text;
                textarea.style.position = "absolute";
                textarea.style.opacity = "0";
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand("copy");
                document.body.removeChild(textarea);
                ElMessage.success('复制成功')
            } catch (error) {
                ElMessage.error('复制失败，请手动复制')
            }

        }
}

const copySql = () => {
    if (currentQuery.value.interface_sql) {
        if (window.isSecureContext && navigator.clipboard) {
            navigator.clipboard.writeText(currentQuery.value.interface_sql)
                .then(() => {
                    ElMessage.success('复制成功')
                })
                .catch(() => {
                    ElMessage.error('复制失败，请手动复制')
                })
        } else {
            try {
                const textarea = document.createElement("textarea");
                textarea.value = currentQuery.value.interface_sql;
                textarea.style.position = "absolute";
                textarea.style.opacity = "0";
                document.body.appendChild(textarea);
                textarea.select();
                const success = document.execCommand("copy");
                document.body.removeChild(textarea);
                ElMessage.success('复制成功')
            } catch (error) {
                ElMessage.error('复制失败，请手动复制')
            }

        }
    }
}

// 复制JSON参数
const copyJsonParams = () => {
  if (currentQuery.value.query_params) {
    let jsonContent = formatJsonParams.value;
    
    if (window.isSecureContext && navigator.clipboard) {
      navigator.clipboard.writeText(jsonContent)
        .then(() => {
          ElMessage.success('参数已复制到剪贴板')
        })
        .catch(() => {
          ElMessage.error('复制失败，请手动复制')
        })
    } else {
      try {
        const textarea = document.createElement("textarea");
        textarea.value = jsonContent;
        textarea.style.position = "absolute";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        ElMessage.success('参数已复制到剪贴板');
      } catch (err) {
        ElMessage.error('复制失败，请手动复制');
      }
    }
  }
};

// 搜索日志
const searchLogs = () => {
  pageInfo.currentPage = 1
  fetchData()
}

// 重置过滤器
const resetFilter = () => {
  filterForm.valie ={
    interface_code: '',
    dateRange: []
  }
  searchLogs()
}

// 分页处理
const handleSizeChange = (size) => {
  pageInfo.pageSize = size
  fetchData()
}

const handleCurrentChange = (page) => {
  pageInfo.currentPage = page
  fetchData()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchData()
})

// 计算属性：动态计算interface_code列宽度
const getInterfaceCodeWidth = computed(() => {
  // 如果没有数据，返回默认宽度
  if (!pageInfo.data || pageInfo.data.length === 0) return 200;
  
  // 找出最长的interface_code
  let maxWidth = 200; // 默认最小宽度
  
  pageInfo.data.forEach(item => {
    if (item.interface_code) {
      const width = calculateColumnWidth(item.interface_code, {
        minWidth: 150,  // 最小宽度
        maxWidth: 300   // 最大宽度
      });
      maxWidth = Math.max(maxWidth, width);
    }
  });
  
  return maxWidth;
});
// 计算属性：格式化JSON参数
const formatJsonParams = computed(() => {
  if (!currentQuery.value || !currentQuery.value.query_params) {
    return '{}';
  }
  
  try {
    // 如果已经是对象，转为字符串再格式化
    let jsonData = currentQuery.value.query_params;
    
    // 如果是字符串，尝试解析为JSON对象
    if (typeof jsonData === 'string') {
      jsonData = JSON.parse(jsonData);
    }
    
    // 格式化为美观的JSON字符串
    return JSON.stringify(jsonData, null, 2);
  } catch (error) {
    console.error('JSON格式化失败:', error);
    // 如果解析失败，返回原始内容
    return currentQuery.value.query_params;
  }
});
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

.json-code {
  width: 100%;
  background-color: #282c34;
  border-radius: 4px;
  overflow: hidden;
}

.json-code pre {
  margin: 0;
  padding: 12px;
  overflow-x: auto;
  max-height: 300px;
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