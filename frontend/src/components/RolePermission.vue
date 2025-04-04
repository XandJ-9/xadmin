<template>
  <el-drawer
    v-model="visible"
    title="编辑角色权限"
    size="30%"
    :destroy-on-close="true"
    direction="rtl"
  >
    <div class="role-permission-container">
      <div class="role-info">
        <h3>{{ role.name }}</h3>
        <p>{{ role.description }}</p>
      </div>
      
      <div class="menu-tree-container" v-loading="loading">
        <h4>菜单权限</h4>
        <el-tree
          ref="menuTreeRef"
          :data="menuTreeData"
          show-checkbox
          node-key="id"
          :props="{ label: 'name', children: 'children' }"
          default-expand-all
          @check="handleCheckChange"
        >
          <template #default="{ node, data }">
            <span class="custom-tree-node">
              <span>{{ node.label }}</span>
              <span class="menu-path" v-if="data.path">{{ data.path }}</span>
            </span>
          </template>
        </el-tree>
      </div>
      
      <div class="drawer-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="savePermissions" :loading="saving">保存</el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { listToTree } from '@/utils/treeUtils'

// 抽屉可见性
const visible = ref(false)

// 角色信息
const role = reactive({
  id: null,
  name: '',
  description: ''
})

// 菜单树数据
const menuTreeData = ref([])
const menuTreeRef = ref(null)
const loading = ref(false)
const saving = ref(false)

// 已选择的菜单ID列表
const selectedMenuIds = ref([])

// 打开抽屉并加载数据
const open = async (roleData) => {
  // 设置角色信息
  Object.assign(role, {
    id: roleData.id,
    name: roleData.name,
    description: roleData.description
  })
  
  visible.value = true
  
  // 加载数据
  await Promise.all([
    fetchMenuList(),
    fetchRolePermissions(roleData.id)
  ])
  
  // 设置选中状态
  nextTick(() => {
    if (menuTreeRef.value && selectedMenuIds.value.length > 0) {
      menuTreeRef.value.setCheckedKeys(selectedMenuIds.value)
    }
  })
}

// 获取菜单列表
const fetchMenuList = async () => {
  loading.value = true
  try {
    const response = await request.get('/api/menus/all/')
    menuTreeData.value = listToTree(response.data)
  } catch (error) {
    console.error('获取菜单列表失败:', error)
    ElMessage.error('获取菜单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取角色权限
const fetchRolePermissions = async (roleId) => {
  try {
    // 这里假设后端有获取角色权限的API
    const response = await request.get(`/api/roles/${roleId}/menus/`)
    selectedMenuIds.value = response.data.menu_ids || []
  } catch (error) {
    console.error('获取角色权限失败:', error)
    ElMessage.error('获取角色权限失败')
    // 如果API不存在，可以先使用空数组
    selectedMenuIds.value = []
  }
}

// 处理选中变化
const handleCheckChange = (data, checked) => {
  // 可以在这里添加一些自定义逻辑
  console.log('选中变化:', data, checked)
}

// 保存权限
const savePermissions = async () => {
  if (!role.id) {
    ElMessage.warning('角色ID无效')
    return
  }
  
  saving.value = true
  try {
    // 获取当前选中的菜单ID
    const checkedKeys = menuTreeRef.value.getCheckedKeys()
    const halfCheckedKeys = menuTreeRef.value.getHalfCheckedKeys()
    const allCheckedKeys = [...checkedKeys, ...halfCheckedKeys]
    
    // 调用保存权限API
    await request.post(`/api/roles/${role.id}/set_menus/`, {
      menu_ids: allCheckedKeys
    })
    
    ElMessage.success('权限保存成功')
    visible.value = false
  } catch (error) {
    console.error('保存权限失败:', error)
    ElMessage.error('保存权限失败')
  } finally {
    saving.value = false
  }
}

// 暴露方法给父组件调用
defineExpose({
  open
})
</script>

<style scoped>
.role-permission-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0 20px;
}

.role-info {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.role-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.role-info p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.menu-tree-container {
  flex: 1;
  overflow-y: auto;
}

.menu-tree-container h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
}

.custom-tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.menu-path {
  font-size: 12px;
  color: #909399;
  margin-left: 8px;
}

.drawer-footer {
  margin-top: 20px;
  text-align: right;
}
</style>