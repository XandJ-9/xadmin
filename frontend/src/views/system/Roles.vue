<template>
  <div class="roles-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加角色
      </el-button>
    </div>

    <el-table :data="roleList" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="角色名称" width="180" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="create_time" label="创建时间" width="180" />
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          <el-button size="small" type="primary" @click="handlePermission(scope.row)">菜单权限</el-button>
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
    
    <!-- 角色权限编辑抽屉 -->
    <RolePermission ref="rolePermissionRef" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import RolePermission from '@/components/RolePermission.vue'

const roleList = ref([])
const loading = ref(false)

const fetchRoles = async () => {
  loading.value = true
  try {
    const response = await request.get('/api/roles/')
    roleList.value = response.data
  } catch (error) {
    if (error.response?.status === 403) {
      ElMessage.error('当前用户无访问权限')
    } else {
      ElMessage.error('获取角色列表失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRoles()
})

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

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确认删除该角色吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    
    await request.delete(`/api/roles/${row.id}/`)
    ElMessage.success('删除成功')
    await fetchRoles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error('Error deleting role:', error)
    }
  }
}

const handleSubmit = async () => {
  roleFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (roleForm.id) {
          // 编辑角色
          await request.put(`/api/roles/${roleForm.id}/`, {
            name: roleForm.name,
            description: roleForm.description
          })
          ElMessage.success('编辑成功')
        } else {
          // 添加角色
          await request.post('/api/roles/', {
            name: roleForm.name,
            description: roleForm.description
          })
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        await fetchRoles()
      } catch (error) {
        ElMessage.error(roleForm.id ? '编辑失败' : '添加失败')
        console.error('Error submitting role:', error)
      }
    }
  })
}

// 角色权限编辑相关
const rolePermissionRef = ref(null)

// 处理编辑权限
const handlePermission = (row) => {
  rolePermissionRef.value.open(row)
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