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

    <div class="query-content">
      <div class="query-editor">
          <MonacoEditor
            v-model="sqlQuery"
            :options="editorOptions"
            language="sql"
            theme="vs-light"
            @change="onEditorChange"
          />
      </div>
      <QueryResult
        :query-result="queryResult"
        :table-columns="tableColumns"
        :loading="loading"
        :error="error"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import MonacoEditor from '@/components/MonacoEditor.vue'
import QueryResult from '@/components/QueryResult.vue'

const dataSources = ref([])
const selectedDataSource = ref('')
const sqlQuery = ref('')
const queryResult = ref([])
const tableColumns = ref([])
const loading = ref(false)
const error = ref('')


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
  // currentPage.value = 1
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

// Monaco Editor配置
const editorOptions = {
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  automaticLayout: true,
  tabSize: 2,
  fontSize: 14,
  suggestOnTriggerCharacters: true,
  formatOnPaste: true,
  formatOnType: true,
  wordWrap: 'on',
  lineNumbers: 'on',
  roundedSelection: false,
  scrollbar: {
    vertical: 'visible',
    horizontal: 'visible',
    useShadows: false,
    verticalScrollbarSize: 8,
    horizontalScrollbarSize: 8
  },
  padding: { top: 0, left: 8, right: 8, bottom: 0},
  quickSuggestions: true,
  snippetSuggestions: 'inline',
  formatOnSave: true,
  lineNumbersMinChars: 5,
  lineDecorationsWidth: 5,
  theme: {
    colors: {
      'editor.background': '#f5f7fa',
      'editorLineNumber.background': '#f5f7fa',
      'editorLineNumber.foreground': '#606266',
      'editorGutter.background': '#fffffe'
    }
  },
  // 添加快捷键支持
  keybindings: [
    { command: 'editor.action.formatDocument', key: 'ctrl+shift+f' },
    { command: 'editor.action.formatDocument', key: 'cmd+shift+f' },
  ]
}

const onEditorChange = (value) => {
  sqlQuery.value = value
}
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

.query-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #fff;
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.query-editor {
  flex: 0 0 auto;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  height: 300px;
  position: relative;
}
</style>