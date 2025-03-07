<template>
  <div class="users-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加用户
      </el-button>
    </div>

    <el-table :data="userList" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="180" />
      <el-table-column prop="role" label="角色" width="180" />
      <el-table-column prop="createTime" label="创建时间" />
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
import { ref, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const userList = ref([
  {
    id: 1,
    username: 'admin',
    role: '管理员',
    createTime: '2024-03-15'
  },
  {
    id: 2,
    username: 'user1',
    role: '普通用户',
    createTime: '2024-03-15'
  }
])

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

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该用户吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // TODO: 实现实际的删除逻辑
    const index = userList.value.findIndex(item => item.id === row.id)
    userList.value.splice(index, 1)
    ElMessage.success('删除成功')
  })
}

const handleSubmit = () => {
  userFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现实际的提交逻辑
      if (userForm.id) {
        // 编辑用户
        const index = userList.value.findIndex(item => item.id === userForm.id)
        userList.value[index] = {
          ...userList.value[index],
          username: userForm.username,
          role: userForm.role === 'admin' ? '管理员' : '普通用户'
        }
        ElMessage.success('编辑成功')
      } else {
        // 添加用户
        userList.value.push({
          id: userList.value.length + 1,
          username: userForm.username,
          role: userForm.role === 'admin' ? '管理员' : '普通用户',
          createTime: new Date().toLocaleDateString()
        })
        ElMessage.success('添加成功')
      }
      dialogVisible.value = false
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