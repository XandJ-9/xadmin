<template>
  <div class="system-menu-container">
      <div class="operation-container">
        <el-button type="primary" @click="handleAdd">添加菜单</el-button>
      </div>
      
      <el-table :data="menuData" style="width: 100%" row-key="id" border default-expand-all>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="菜单名称" width="180"></el-table-column>
        <el-table-column prop="path" label="路由路径" width="180"></el-table-column>
        <el-table-column prop="component" label="组件路径"></el-table-column>
        <el-table-column prop="icon" label="图标" width="100">
          <template #default="{row}">
            <el-icon v-if="row.icon">
              <component :is="row.icon"></component>
            </el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="80"></el-table-column>
        <el-table-column prop="hidden" label="是否隐藏" width="100">
          <template #default="{row}">
            <el-tag :type="row.hidden ? 'danger' : 'success'">
              {{ row.hidden ? '隐藏' : '显示' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{row}">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    
    <!-- 添加/编辑菜单对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form :model="menuForm" label-width="100px" :rules="rules" ref="menuFormRef">
        <el-form-item label="上级菜单">
          <el-tree-select
            v-model="menuForm.parentId"
            :data="menuTreeData"
            check-strictly
            default-expand-all
            node-key="id"
            :props="{ label: 'name', children: 'children' }"
            placeholder="请选择上级菜单"
            clearable>
          </el-tree-select>
        </el-form-item>
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="menuForm.name"></el-input>
        </el-form-item>
        <el-form-item label="路由路径" prop="path">
          <el-input v-model="menuForm.path"></el-input>
        </el-form-item>
        <el-form-item label="组件路径">
          <el-input v-model="menuForm.component"></el-input>
        </el-form-item>
        <el-form-item label="菜单图标">
          <el-input v-model="menuForm.icon"></el-input>
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="menuForm.sort" :min="0"></el-input-number>
        </el-form-item>
        <el-form-item label="是否隐藏">
          <el-switch v-model="menuForm.hidden"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 菜单数据
const menuData = ref([
  {
    id: 1,
    name: '系统管理',
    path: '/system',
    component: 'Layout',
    icon: 'Setting',
    sort: 1,
    hidden: false,
    children: [
      {
        id: 2,
        name: '系统配置',
        path: '/system/system-config',
        component: 'SystemConfig',
        icon: 'Setting',
        sort: 1,
        hidden: false,
        parentId: 1
      },
      {
        id: 3,
        name: '菜单管理',
        path: '/system/system-menu',
        component: 'SystemMenu',
        icon: 'Menu',
        sort: 2,
        hidden: false,
        parentId: 1
      }
    ]
  },
  {
    id: 4,
    name: '数据管理',
    path: '/data',
    component: 'Layout',
    icon: 'DataLine',
    sort: 2,
    hidden: false,
    children: [
      {
        id: 5,
        name: '数据源管理',
        path: '/data/datasources',
        component: 'DataSources',
        icon: 'Collection',
        sort: 1,
        hidden: false,
        parentId: 4
      }
    ]
  }
])

// 菜单树数据，用于选择上级菜单
const menuTreeData = computed(() => {
  // 构建树形结构
  return [{ id: 0, name: '根菜单', children: [...menuData.value] }]
})

// 对话框相关
const dialogVisible = ref(false)
const dialogTitle = ref('添加菜单')
const menuFormRef = ref(null)

// 表单数据
const menuForm = reactive({
  id: null,
  parentId: 0,
  name: '',
  path: '',
  component: '',
  icon: '',
  sort: 0,
  hidden: false
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' }
  ],
  path: [
    { required: true, message: '请输入路由路径', trigger: 'blur' }
  ]
}

// 添加菜单
const handleAdd = () => {
  dialogTitle.value = '添加菜单'
  resetForm()
  dialogVisible.value = true
}

// 编辑菜单
const handleEdit = (row) => {
  dialogTitle.value = '编辑菜单'
  Object.assign(menuForm, row)
  dialogVisible.value = true
}

// 删除菜单
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除菜单「${row.name}」吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    // 这里添加删除菜单的逻辑
    ElMessage.success('删除成功')
  }).catch(() => {
    // 取消删除
  })
}

// 重置表单
const resetForm = () => {
  if (menuFormRef.value) {
    menuFormRef.value.resetFields()
  }
  Object.assign(menuForm, {
    id: null,
    parentId: 0,
    name: '',
    path: '',
    component: '',
    icon: '',
    sort: 0,
    hidden: false
  })
}

// 提交表单
const submitForm = () => {
  menuFormRef.value.validate((valid) => {
    if (valid) {
      // 这里添加保存菜单的逻辑
      if (menuForm.id) {
        // 编辑菜单
        ElMessage.success('菜单更新成功')
      } else {
        // 添加菜单
        ElMessage.success('菜单添加成功')
      }
      dialogVisible.value = false
    }
  })
}

onMounted(() => {
  // 组件挂载时加载菜单数据
  // 这里可以添加从后端获取菜单数据的逻辑
})
</script>

<style scoped>
.system-menu-container {
  padding: 20px;
}

.box-card {
  margin-top: 20px;
}

.operation-container {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>