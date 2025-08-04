<template>
  <div class="app-container">
    <div class="query-header">
      <div class="header-left">
        <el-select
          v-model="selectedDataSource"
          placeholder="选择数据源"
          style="width: 200px"
        >
          <el-option
            v-for="source in dataSources"
            :key="source.id"
            :label="source.name"
            :value="source.id"
          />
        </el-select>
      </div>
      <div class="header-right">
        <el-button  icon="Search" @click="handleQuery" :loading="loading">
           执行查询
        </el-button>
        <el-button  icon="Save" @click="handleSave" :disabled="!sqlQuery.trim()">
          保存
        </el-button>
      </div>
    </div>

    <div class="query-content">
      <!-- SQL编辑器区域 -->
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

      <!-- 可调整大小的分隔条 -->
      <div class="resizer" v-if="queryTabs.length > 0" @mousedown="startResize"></div>

      <!-- 查询结果区域 -->
      <div class="query-result" v-if="queryTabs.length > 0" :style="{ height: resultHeight + 'px' }">
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
            <template #label>
              <el-tooltip
                class="box-item"
                effect="dark"
                :content="tab.sql"
                placement="top"
              >
                <span>{{ tab.label }}</span>
              </el-tooltip>
            </template>
            <template #default> 
              <QueryResult
                :query-result="tab.queryResult"
                :total="tab.queryResult.length"
                :table-columns="tab.tableColumns"
                :loading="loading"
                :error="tab.error"
              />
            </template>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup name="DataQuery">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
// import { Search, Save } from '@element-plus/icons-vue'
import MonacoEditor from '@/components/MonacoEditor'
import QueryResult from './QueryResult'
import { getDataSourceList, executeQuery, saveSqlQuery } from '@/api/dataassets/datasource'

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

// 编辑器和结果区域高度相关
const editorHeight = ref(400) // 初始编辑器高度
const resultHeight = ref(300) // 初始结果区域高度
const isResizing = ref(false)
const startY = ref(0)
const startEditorHeight = ref(0)
const startResultHeight = ref(0)
const minEditorHeight = 200 // 编辑器最小高度
const minResultHeight = 200 // 结果区域最小高度

// 计算可用的总高度（减去头部和分隔条高度）
const calculateAvailableHeight = () => {
  return window.innerHeight - 60 - 6 // 头部高度60px，分隔条高度6px
}

const startResize = (e) => {
  isResizing.value = true
  startY.value = e.clientY
  startEditorHeight.value = editorHeight.value
  startResultHeight.value = resultHeight.value
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'row-resize'
}

const handleMouseMove = (e) => {
  if (!isResizing.value) return
  
  const deltaY = e.clientY - startY.value
  const availableHeight = calculateAvailableHeight()
  
  // 计算新的编辑器高度和结果区域高度
  let newEditorHeight = startEditorHeight.value + deltaY
  let newResultHeight = startResultHeight.value - deltaY
  
  // 确保两个区域都不小于最小高度
  if (newEditorHeight < minEditorHeight) {
    newEditorHeight = minEditorHeight
    newResultHeight = availableHeight - minEditorHeight
  } else if (newResultHeight < minResultHeight) {
    newResultHeight = minResultHeight
    newEditorHeight = availableHeight - minResultHeight
  }
  
  editorHeight.value = newEditorHeight
  resultHeight.value = newResultHeight
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
}

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
})

const fetchDataSources = async () => {
    await getDataSourceList().then(res => {
        dataSources.value = res.data
    }).catch(error => {
        ElMessage.error(error.message)
     })
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

const handleQuery = async () => {
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
    const response = await executeQuery(selectedDataSource.value, sql)
    
    // 创建新标签
    const newTab = {
      id: newTabId,
      label: `查询-${tabIndex.value}`,
      sql: sql,
      queryResult: [],
      tableColumns: [],
      error: response?.error
    }

    if (response.total > 0) {
      newTab.tableColumns = Object.keys(response.data[0])
      newTab.queryResult = response.data
    }

    queryTabs.value.push(newTab)
    activeTab.value = newTabId
    
    // 调整编辑器和结果区域的高度
    const availableHeight = calculateAvailableHeight()
    editorHeight.value = Math.floor(availableHeight * 0.6) // 编辑器占60%
    resultHeight.value = Math.floor(availableHeight * 0.4) // 结果区域占40%
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
    
    // 调整编辑器和结果区域的高度
    const availableHeight = calculateAvailableHeight()
    editorHeight.value = Math.floor(availableHeight * 0.6) // 编辑器占60%
    resultHeight.value = Math.floor(availableHeight * 0.4) // 结果区域占40%
  } finally {
    loading.value = false
  }
  
//   try {
//     // const formData = new FormData()
//     // formData.append('sql', sql)
    
//     const response = await executeQuery(selectedDataSource.value, sql)
    

//   } catch (err) {
//     const newTab = {
//       id: newTabId,
//       label: `查询-${tabIndex.value}`,
//       sql: sql,
//       queryResult: [],
//       tableColumns: [],
//       error: err.response?.data.error || '查询执行失败'
//     }
//     queryTabs.value.push(newTab)
//     activeTab.value = newTabId
//   } finally {
//     loading.value = false
//   }
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

// 保存查询脚本
const handleSave = async () => {
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

  // 弹出对话框让用户输入查询名称
  ElMessageBox.prompt('请输入查询名称', '保存SQL查询', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    inputPattern: /\S+/,
    inputErrorMessage: '名称不能为空'
  }).then(({ value }) => {
    // 调用保存API
    saveSqlQuery(selectedDataSource.value, value, sql)
      .then(() => {
        ElMessage.success('保存成功')
      })
      .catch(error => {
        ElMessage.error(`保存失败: ${error.message || '未知错误'}`)
      })
  }).catch(() => {
    // 用户取消操作
  })
}
</script>

<style scoped>
.app-container {
  padding: 0;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 84px); /* 减去顶部导航和标签页的高度 */
  background-color: #f5f7fa;
  overflow: hidden;
}

.query-header {
  display: flex;
  gap: 20px;
  align-items: center;
  padding: 12px 16px;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  height: 60px;
  box-sizing: border-box;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.query-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #fff;
  height: calc(100vh - 60px); /* 减去头部高度 */
  position: relative;
}

.query-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  min-height: 200px;
  flex: 1;
  transition: height 0.3s ease;
}

.resizer {
  width: 100%;
  height: 6px;
  background-color: #f0f2f5;
  cursor: row-resize;
  position: relative;
  z-index: 10;
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
  width: 40px;
  height: 4px;
  background-color: #909399;
  border-radius: 2px;
}

.query-tabs {
  margin-top: 8px;
}

.query-result {
  flex-shrink: 0;
  min-height: 200px;
  max-height: 60vh;
  overflow: auto;
  width: 100%;
}

/* 确保Monaco编辑器填充其容器 */
:deep(.monaco-editor) {
  height: 100% !important;
}

/* 确保查询结果表格正确显示 */
:deep(.el-tabs__content) {
  height: calc(100% - 40px); /* 减去标签页头部的高度 */
  overflow: auto;
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