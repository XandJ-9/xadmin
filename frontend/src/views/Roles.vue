<template>
  <div class="roles-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加角色
      </el-button>
    </div>

    <el-table :data="roleList" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="角色名称" width="180" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="createTime" label="创建时间" width="180" />
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
      <el-form :model="roleForm" :rules="rules" ref="roleFormRef" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="roleForm.description" type="textarea" :rows="3" />
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

const roleList = ref([
  {
    id: 1,
    name: '管理员',
    description: '系统管理员，拥有所有权限',
    createTime: '2024-03-15'
  },
  {
    id: 2,
    name: '普通用户',
    description: '普通用户，拥有基本权限',
    createTime: '2024-03-15'
  }
])

const dialogVisible = ref(false)
const dialogTitle = ref('')
const roleFormRef = ref(null)

const roleForm = reactive({
  id: null,
  name: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入角色描述', trigger: 'blur' }]
}

const handleAdd = () => {
  dialogTitle.value = '添加角色'
  Object.assign(roleForm, {
    id: null,
    name: '',
    description: ''
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑角色'
  Object.assign(roleForm, {
    id: row.id,
    name: row.name,
    description: row.description
  })
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确认删除该角色吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    // TODO: 实现实际的删除逻辑
    const index = roleList.value.findIndex(item => item.id === row.id)
    if (index > -1) {
      roleList.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  }).catch(() => {})
}

const handleSubmit = () => {
  roleFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现实际的提交逻辑
      if (roleForm.id === null) {
        // 添加角色
        const newRole = {
          id: roleList.value.length + 1,
          name: roleForm.name,
          description: roleForm.description,
          createTime: new Date().toLocaleDateString()
        }
        roleList.value.push(newRole)
        ElMessage.success('添加成功')
      } else {
        // 编辑角色
        const index = roleList.value.findIndex(item => item.id === roleForm.id)
        if (index > -1) {
          roleList.value[index] = {
            ...roleList.value[index],
            name: roleForm.name,
            description: roleForm.description
          }
          ElMessage.success('编辑成功')
        }
      }
      dialogVisible.value = false
    }
  })
}
</script>

<style scoped>
.roles-container {
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