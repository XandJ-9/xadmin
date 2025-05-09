<template>
  <div class="system-menu-container">
      <div class="operation-container">
        <el-button type="primary" @click="handleAdd">添加菜单</el-button>
          <el-input
            v-model="searchKeyword"
            placeholder="请输入菜单名称或路径搜索"
            clearable
            style="width: 200px; margin-left: 5px;"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="fetchMenuList" style="margin-left: 5px;">搜索</el-button>
      </div>
      
      <el-table :data="filteredMenuData" style="width: 100%" row-key="id" v-loading="loading" border default-expand-all>
        <!-- <el-table-column prop="id" label="ID" width="80"></el-table-column> -->
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
        <el-table-column prop="meta.needTagview" label="是否添加Tagview" width="100">
            <template #default="{row}">
                <el-tag :type="row.meta.needTagview ? 'success' : 'danger'">
                    {{ row.meta.needTagview ? '是' : '否' }}
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
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="50%">
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
        <el-form-item label="添加Tagview">
            <el-switch v-model="menuForm.needTagview"></el-switch>
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
import { Search } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import request from '@/utils/request'
import { listToTree } from '@/utils/treeUtils'

// 菜单数据
const menuData = ref([])

// 搜索关键词
const searchKeyword = ref('')

const loading = ref(false)

// 过滤后的菜单数据
const filteredMenuData = computed(() => {
  if (!searchKeyword.value) {
    return menuData.value
  }
  const keyword = searchKeyword.value.toLowerCase()
  // 递归搜索菜单树
  const filterMenuTree = (menus) => {
    return menus.filter(menu => {
      // 检查当前菜单是否匹配
      const nameMatch = menu.name && menu.name.toLowerCase().includes(keyword)
      const pathMatch = menu.path && menu.path.toLowerCase().includes(keyword)
      const componentMatch = menu.component && menu.component.toLowerCase().includes(keyword)
      
      // 如果当前菜单匹配，直接返回true
      if (nameMatch || pathMatch || componentMatch) {
        return true
      }
      
      // 如果有子菜单，递归搜索子菜单
      if (menu.children && menu.children.length) {
        const filteredChildren = filterMenuTree(menu.children)
        if (filteredChildren.length) {
          menu.children = filteredChildren
          return true
        }
      }
      
      return false
    })
  }
  
  return filterMenuTree(JSON.parse(JSON.stringify(menuData.value)))
})

// 菜单树数据，用于选择上级菜单
const menuTreeData = computed(() => {
  // 使用工具方法将扁平菜单数据转换为树形结构
  // 添加根菜单选项
  return [{ id: 0, name: '根菜单', children: menuData.value }]
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
  hidden: false,
  needTagview: false
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
  // 设置表单数据
  Object.assign(menuForm, {
    id: row.id,
    name: row.name,
    path: row.path,
    component: row.component,
    icon: row.icon,
    sort: row.sort,
    hidden: row.hidden,
    parentId: row.parent || 0 , // 如果parent为null，则设置为0（根菜单）
    needTagview: row.meta.needTagview
  })
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
    // 调用删除菜单API
    deleteMenu(row.id)
  }).catch(() => {
    // 取消删除
  })
}


const user= useUserStore()
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
    hidden: false,
    meta_need_tagview: true
  })
}

// 提交表单
const submitForm = () => {
  menuFormRef.value.validate(async (valid) => {
    if (valid) {
      // 准备提交的数据
      const submitData = {
        name: menuForm.name,
        path: menuForm.path,
        component: menuForm.component,
        icon: menuForm.icon,
        sort: menuForm.sort,
        hidden: menuForm.hidden,
        parent: menuForm.parentId === 0 ? null : menuForm.parentId,
          meta_need_tagview: menuForm.needTagview
      }
      
      // 如果是编辑，添加ID
      if (menuForm.id) {
        submitData.id = menuForm.id
      }
      console.log('submitData ',submitData)
        // 调用保存菜单API
      const success = await saveMenu(submitData)
      if (success) {
        dialogVisible.value = false
      }
    }
  })
}


// 获取菜单列表
const fetchMenuList = async () => {
    loading.value = true
  try {
    const response = await request.get('/api/menus/all/')
    // menuData.value = response.data
    menuData.value = listToTree(response.data)
    // ElMessage.success('菜单数据加载成功')
  } catch (error) {
    ElMessage.error('获取菜单列表失败')
  } finally {
    loading.value = false
  }
}

// 删除菜单
const deleteMenu = async (id) => {
  try {
    await request.delete(`/api/menus/${id}/`)
    ElMessage.success('删除成功')
    fetchMenuList() // 重新加载菜单数据
  } catch (error) {
    ElMessage.error('删除菜单失败')
  }
}

// 保存菜单
const saveMenu = async (menuData) => {
  try {
    if (menuData.id) {
      // 编辑菜单
      await request.put(`/api/menus/${menuData.id}/`, menuData)
      ElMessage.success('菜单更新成功')
    } else {
      // 添加菜单
      await request.post('/api/menus/', menuData)
      ElMessage.success('菜单添加成功')
    }
    fetchMenuList() // 重新加载菜单数据
    return true
  } catch (error) {
    ElMessage.error('保存菜单失败')
    return false
  }
}

onMounted(() => {
  // 组件挂载时加载菜单数据
  fetchMenuList()
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
  display: flex;
  /* justify-content: space-between; */
  align-items: center;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>