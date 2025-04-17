<template>
  <div class="datasource-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">新增数据源</el-button>
    </div>

    <el-table :data="dataSources" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" width="120" />
      <el-table-column prop="type" label="类型" width="120" />
      <el-table-column prop="host" label="主机地址" width="150" />
      <el-table-column prop="port" label="端口" width="100" />
      <el-table-column prop="database" label="数据库" width="120" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="creator_username" label="创建者" width="120" />
      <el-table-column prop="create_time" label="创建时间" width="180" />
      <el-table-column fixed="right" label="操作" width="250">
        <template #default="scope">
          <div class="operation-buttons">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="success" :loading="btnTestList.includes(scope.row)" @click="handleTest(scope.row)">测试连接</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="50%"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入数据源名称" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择数据源类型" style="width: 100%">
            <el-option label="MySQL" value="mysql" />
            <el-option label="PostgreSQL" value="postgresql" />
            <el-option label="StarRocks" value="starrocks" />
            <el-option label="Presto" value="presto" />
          </el-select>
        </el-form-item>
        <el-form-item label="主机地址" prop="host">
          <el-input v-model="form.host" placeholder="请输入主机地址" />
        </el-form-item>
        <el-form-item label="端口" prop="port">
          <el-input v-model="form.port" placeholder="请输入端口号" />
        </el-form-item>
        <el-form-item label="数据库" prop="database">
          <el-input v-model="form.database" placeholder="请输入数据库名称" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            placeholder="请输入描述信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const loading = ref(false)
const btnLoading = ref(false)
const dataSources = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)

const form = ref({
  name: '',
  type: '',
  host: '',
  port: '',
  database: '',
  username: '',
  password: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入数据源名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择数据源类型', trigger: 'change' }],
  host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  port: [{ required: true, message: '请输入端口号', trigger: 'blur' }],
  database: [{ required: true, message: '请输入数据库名称', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const fetchDataSources = async () => {
  try {
    loading.value = true
    const response = await request.get('/api/datasources/')
    dataSources.value = response.data
  } catch (error) {
    // ElMessage.error('获取数据源列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增数据源'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑数据源'
  form.value = { ...row }
  dialogVisible.value = true
}

const btnTestList = ref([])

const handleTest = async (row) => {
    btnTestList.value.push(row)
    const response = await request.post(`/api/datasources/${row.id}/test/`)
    if (response.data.status === 'success') {
      ElMessage.success(`${row.name}连接测试成功`)
    } else {
      ElMessage.error(`${row.name}连接测试失败: ${response.data.msg}`)
    }
      // row.loading = false
    btnTestList.value = btnTestList.value.filter(item => item.id !== row.id)
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该数据源吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request.delete(`/api/datasources/${row.id}/`)
      ElMessage.success('删除成功')
      fetchDataSources()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.value.id) {
          await request.put(`/api/datasources/${form.value.id}/`, form.value)
          ElMessage.success('更新成功')
        } else {
          await request.post('/api/datasources/', form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchDataSources()
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '操作失败')
      }
    }
  })
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.value = {
    name: '',
    type: '',
    host: '',
    port: '',
    database: '',
    username: '',
    password: '',
    description: ''
  }
}

onMounted(() => {
  fetchDataSources()
})
</script>

<style scoped>
.datasource-container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.operation-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  width: auto;
  min-width: 80px;
}

.operation-buttons .el-button {
  margin-left: 0;
  padding-left: 12px;
  padding-right: 12px;
}

@media screen and (max-width: 768px) {
  .operation-buttons {
    flex-direction: column;
    width: 80px;
    gap: 4px;
  }
  
  .operation-buttons .el-button {
    width: 100%;
    margin-left: 0;
    padding-left: 12px;
    padding-right: 12px;
  }
}
</style>