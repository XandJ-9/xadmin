<template>
  <div class="users-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加用户
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户名"
        style="width: 200px"
      />
      <el-button @click="fetchUsers">
        <el-icon><Search /></el-icon>搜索
      </el-button>
    </div>

    <el-table :data="userList" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="180" />
      <el-table-column prop="role_info.name" label="角色" width="180" />
      <el-table-column prop="create_time" label="创建时间" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
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
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const userList = ref([])
const loading = ref(false)
const searchQuery = ref('')

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await request.get('/api/users/', {
      params: {
        search: searchQuery.value
      }
    })
    userList.value = response.data
  } catch (error) {
      if (error.response.status === 403) {
        ElMessage.error('当前用户无访问权限')
      } else {
        ElMessage.error('获取用户列表失败')
        }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})

const dialogVisible = ref(false)
const dialogTitle = ref('')
const userFormRef = ref(null)

const userForm = reactive({
  id: null,
  username: '',
  password: '',
  role: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const handleAdd = () => {
  dialogTitle.value = '添加用户'
  Object.assign(userForm, {
    id: null,
    username: '',
    password: '',
    role: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑用户'
  Object.assign(userForm, {
    id: row.id,
    username: row.username,
    role: row.role === '管理员' ? 'admin' : 'user'
  })
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request.delete(`/api/users/${row.id}`)
    ElMessage.success('删除成功')
    await fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Error deleting user:', error)
    }
  }
}

const handleSubmit = async () => {
  userFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (userForm.id) {
          // 编辑用户
          await request.put(`/api/users/${userForm.id}/`, {
            username: userForm.username,
            role: userForm.role
          })
          ElMessage.success('编辑成功')
        } else {
          // 添加用户
          await request.post('/api/users/', {
            username: userForm.username,
            password: userForm.password,
            role: userForm.role
          })
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        await fetchUsers()
      } catch (error) {
        ElMessage.error(userForm.id ? '编辑失败' : '添加失败')
        console.error('Error submitting user:', error)
      }
    }
  })
}
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-table) {
  background-color: #ffffff;
  color: #303133;
}

:deep(.el-table__header) {
  background-color: #ffffff;
}

:deep(.el-table__header-wrapper th) {
  background-color: #ffffff;
  color: #303133;
  border-bottom: 1px solid #e6e6e6;
}

:deep(.el-table td) {
  border-bottom: 1px solid #e6e6e6;
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: #f5f7fa;
}

:deep(.el-table__body tr) {
  background-color: #ffffff;
}
</style>