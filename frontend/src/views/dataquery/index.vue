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
      <div class="query-editor" :style="{ height: editorHeight + 'px' }">
          <MonacoEditor
            v-model="sqlQuery"
            :options="editorOptions"
            language="sql"
            theme="vs-light"
            @change="onEditorChange"
            @cursor-change="handleCursorChange"
          />
      </div>
      
      <div class="resizer" @mousedown="startResize"></div>
      
      <el-tabs 
        v-model="activeTab" 
        type="card" 
        closable 
        @tab-remove="removeTab"
        class="query-tabs"
      >
        <el-tab-pane
          v-for="tab in queryTabs"
          :key="tab.id"
          :label="tab.label"
          :name="tab.id"
        >
          <QueryResult
            :query-result="tab.queryResult"
            :table-columns="tab.tableColumns"
            :loading="loading"
            :error="tab.error"
            class="query-result"
          />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import MonacoEditor from '@/components/MonacoEditor.vue'
import QueryResult from '@/components/QueryResult.vue'

// 数据查询相关数据
const dataSources = ref([])
const selectedDataSource = ref('')
const sqlQuery = ref('')
const loading = ref(false)
const currentCursorPosition = ref(0)

// 标签页相关数据
const activeTab = ref('')
const queryTabs = ref([])
const tabIndex = ref(0)

// 编辑器高度相关
const editorHeight = ref(500)
const isResizing = ref(false)
const startY = ref(0)
const startHeight = ref(0)

const startResize = (e) => {
  isResizing.value = true
  startY.value = e.clientY
  startHeight.value = editorHeight.value
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', stopResize)
}

const handleMouseMove = (e) => {
  if (!isResizing.value) return
  const deltaY = e.clientY - startY.value
  const newHeight = Math.max(100, Math.min(window.innerHeight - 300, startHeight.value + deltaY))
  editorHeight.value = newHeight
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
}

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
})

const fetchDataSources = async () => {
  try {
    const response = await request.get('/api/datasources/')
    dataSources.value = response.data
  } catch (error) {
    // ElMessage.error('获取数据源列表失败')
  }
}

const handleDataSourceChange = () => {
  // 清空当前查询结果
//   sqlQuery.value = ''
//   activeTab.value = ''
//   queryTabs.value = []
}

// 获取当前光标所在的SQL语句
const getCurrentSql = () => {
  const content = sqlQuery.value
  if (!content) return ''

  // 分割所有SQL语句，保留分号
  const statements = content.split(/(?<=;)/)
  let currentLine = currentCursorPosition.value?.lineNumber || 1
  let currentColumn = currentCursorPosition.value?.column || 1
  let lineCount = 0

  // 找到光标所在的SQL语句
  for (let statement of statements) {
    const statementLines = statement.split('\n')
    lineCount += statementLines.length

    if (lineCount >= currentLine) {
      // 找到包含光标的语句块
      return statement.trim()
    }
  }

  // 如果没有找到或者是最后一个语句，返回最后一个语句
  const lastStatement = statements[statements.length - 1]
  return lastStatement ? lastStatement.trim() : ''
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

  const sql = getCurrentSql()

  if (!sql) {
    ElMessage.warning('请输入SQL语句')
    return
  }

  loading.value = true
  const newTabId = `tab-${tabIndex.value++}`
  
  try {
    const formData = new FormData()
    formData.append('sql', sql)
    
    const response = await request.post(`/api/datasources/${selectedDataSource.value}/query/`, formData)
    
    // 创建新标签
    const newTab = {
      id: newTabId,
      label: `查询-${tabIndex.value}`,
      sql: sql,
      queryResult: [],
      tableColumns: [],
      error: ''
    }

    if (response.data.total > 0) {
      newTab.tableColumns = Object.keys(response.data.data[0])
      newTab.queryResult = response.data.data
    }

    queryTabs.value.push(newTab)
    activeTab.value = newTabId
    editorHeight.value = 400
  } catch (err) {
    const newTab = {
      id: newTabId,
      label: `查询-${tabIndex.value}`,
      sql: sql,
      queryResult: [],
      tableColumns: [],
      error: err.response?.data.error || '查询执行失败'
    }
    queryTabs.value.push(newTab)
    activeTab.value = newTabId
  } finally {
    loading.value = false
  }
}

const removeTab = (targetName) => {
  const tabs = queryTabs.value
  let activeName = activeTab.value
  
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.id === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.id
        }
      }
    })
  }
  
  activeTab.value = activeName
  queryTabs.value = tabs.filter(tab => tab.id !== targetName)
  if (queryTabs.value.length == 0) {
    tabIndex.value = 0
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

const handleCursorChange = (position) => {
  currentCursorPosition.value = position
}
</script>

<style scoped>
.data-query-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  /* height: calc(100vh - 120px); */
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
  overflow: hidden;
}

.query-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  min-height: 100px;
  resize: vertical;
}

.resizer {
  width: 100%;
  height: 6px;
  background-color: #f0f2f5;
  cursor: row-resize;
  position: relative;
}

.resizer:hover {
  background-color: #e4e7ed;
}

.resizer::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 2px;
  background-color: #909399;
  border-radius: 1px;
}

.query-tabs {
  margin-top: 16px;
  flex: 1;
  overflow: auto;
}

.query-result {
  flex-shrink: 0;
  height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>