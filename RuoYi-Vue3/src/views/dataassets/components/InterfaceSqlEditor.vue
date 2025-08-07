<template>
  <div class="sql-editor-container">
    <div class="editor-header">
      <!-- <div class="interface-info" v-if="interfaceInfo">
        <span class="interface-name">{{ interfaceInfo.interface_name }}</span>
        <span class="interface-code">({{ interfaceInfo.interface_code }})</span>
      </div> -->
      <div class="editor-actions">
        <el-tooltip content="纯sql执行，如果有输入参数，请先移除输入参数，待验证sql查询正常，再添加输入参数模板" placement="top">
        <el-button type="primary" plain @click="executeSql" :loading="loading">执行</el-button>
        </el-tooltip>
        <el-button plain @click="saveSql">更新SQL</el-button>
        <el-button plain @click="closeSql">关闭</el-button>
      </div>
    </div>
    
    <div class="editor-main">
      <div class="sql-input">
        <div class="section-title">SQL语句</div>
        <div class="monaco-wrapper">
          <MonacoEditor
            v-model="sqlContent"
            :options="editorOptions"
            language="sql"
            theme="vs-light"
            @change="onEditorChange"
            @cursor-change="handleCursorChange"
          />
        </div>
      </div>
      
      <div class="sql-result" v-if="resultVisible">
        <div class="section-title">
            <span>执行结果</span>
            <span class="close-btn" @click="closeResult">关闭</span>
        </div>

        <div v-if="sqlError" class="sql-error">
          <pre>{{ sqlError }}</pre>
        </div>
        <el-table v-else :data="sqlResult" border style="width: 100%">
          <el-table-column 
            v-for="(col, index) in sqlColumns" 
            :key="index" 
            :prop="col" 
            :label="col" 
            :width="calculateColumnWidth(col)"
          />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import MonacoEditor from '@/components/MonacoEditor'

// 定义组件属性
const props = defineProps({
  // 初始SQL内容
  initialSql: {
    type: String,
    default: ''
  },
  // 接口信息
  interfaceInfo: {
    type: Object,
    default: () => ({})
  }
})

// 定义事件
const emit = defineEmits(['update:sql', 'execute', 'save', 'close'])

// 状态变量
const sqlContent = ref(props.initialSql || '')
const resultVisible = ref(false)
const sqlResult = ref([])
const sqlColumns = ref([])
const sqlError = ref('')
const loading = ref(false)
const currentCursorPosition = ref(null)

// 监听初始SQL变化
watch(() => props.initialSql, (newValue) => {
  if (newValue !== sqlContent.value) {
    sqlContent.value = newValue
  }
}, { immediate: true })

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
  padding: { top: 8, bottom: 8 },
  quickSuggestions: true,
  snippetSuggestions: 'inline',
  formatOnSave: true,
  lineNumbersMinChars: 5,
  lineDecorationsWidth: 5
}

// 编辑器内容变化事件
const onEditorChange = (value) => {
  sqlContent.value = value
  emit('update:sql', value)
}

// 光标位置变化事件
const handleCursorChange = (position) => {
  currentCursorPosition.value = position
}

// 获取当前光标所在的SQL语句
const getCurrentSql = () => {
  const content = sqlContent.value
  if (!content) return ''

  // 分割所有SQL语句，保留分号
  const statements = content.split(/(?<=;)/)
  let currentLine = currentCursorPosition.value?.lineNumber || 1
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

// 执行SQL
const executeSql = async () => {
  if (!sqlContent.value.trim()) {
    ElMessage.warning('请输入SQL查询语句')
    return
  }

  const sql = getCurrentSql()
  if (!sql) {
    ElMessage.warning('请输入SQL语句')
    return
  }

  loading.value = true
  sqlError.value = ''
  
  try {
    // 触发执行事件，由父组件处理实际的SQL执行
    emit('execute', {
        sql,
        interfaceId: props.interfaceInfo?.id
    },
        // 回调函数，获取父组件返回值
        async (result) => { 
        // 如果父组件返回了结果
        if (result && result.data) {
        sqlResult.value = result.data
        if (result.data.length > 0) {
            sqlColumns.value = Object.keys(result.data[0])
        } else {
            sqlColumns.value = []
        }
        sqlError.value = ''
        } else if (result && result.error) {
        sqlError.value = result.error
        sqlResult.value = []
        sqlColumns.value = []
        }
        resultVisible.value = true
    })

  } catch (error) {
    console.error('SQL执行失败：', error)
    sqlError.value = error.message || '执行SQL失败'
    sqlResult.value = []
    sqlColumns.value = []
    resultVisible.value = true
  } finally {
    loading.value = false
  }
}

const closeSql = () => {
    emit('close')
}

const closeResult = () => {
  resultVisible.value = false
}

// 保存SQL
const saveSql = async () => {
  if (!sqlContent.value.trim()) {
    ElMessage.warning('SQL内容不能为空')
    return
  }
  
    // 触发保存事件，由父组件处理实际的保存操作
    emit('save', {
        sql: sqlContent.value,
        interfaceId: props.interfaceInfo?.id
    })
    
}

// 计算列宽
const calculateColumnWidth = (columnName) => {
  // 根据列名长度计算合适的宽度
  const baseWidth = 100
  const charWidth = 10
  return Math.max(baseWidth, columnName.length * charWidth) + 'px'
}

// 组件挂载时初始化
// onMounted(() => {
//   // 如果有初始SQL，设置到编辑器中
//   if (props.initialSql) {
//     sqlContent.value = props.initialSql
//   }
// })
</script>

<style scoped>
.sql-editor-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 使用视口高度单位，确保填满整个视口高度 */
  background-color: #f5f7fa;
  border-radius: 4px;
  overflow: hidden;
  animation: flip-in 0.5s ease-out;
}

@keyframes flip-in {
  0% {
    transform: perspective(400px) rotateX(90deg);
    opacity: 0;
  }
  100% {
    transform: perspective(400px) rotateX(0deg);
    opacity: 1;
  }
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
}

.interface-info {
  display: flex;
  align-items: center;
}

.interface-name {
  font-size: 16px;
  font-weight: bold;
  margin-right: 8px;
}

.interface-code {
  color: #909399;
  font-size: 14px;
}

.editor-actions {
  display: flex;
  gap: 8px;
}

.editor-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
  padding: 16px;
  gap: 16px;
  height: calc(100vh - 60px); /* 减去头部高度 */
}

.section-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #303133;
}

.sql-input {
  flex: 1;
  min-height: 40vh; /* 使用视口高度的40%作为最小高度 */
  display: flex;
  flex-direction: column;
}

.monaco-wrapper {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  background-color: #fff;
  min-height: 40vh; /* 使用视口高度的40%作为最小高度 */
  height: 100%; /* 确保填满父容器 */
}

.sql-result {
  flex: 1;
  min-height: 30vh; /* 使用视口高度的30%作为最小高度 */
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.sql-error {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 12px;
  border-radius: 4px;
  overflow: auto;
  max-height: 300px;
}

.sql-error pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: monospace;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #303133;
}

.close-btn {
  color: #409EFF;
  cursor: pointer;
  font-size: 13px;
  user-select: none;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #f56c6c;
}
</style>