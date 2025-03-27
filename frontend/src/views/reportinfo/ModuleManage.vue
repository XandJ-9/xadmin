<template>
  <div class="module-manage">
      <template #header>
        <div class="card-header">
          <span>模块管理</span>
          <el-button type="primary" @click="handleAdd">新增模块</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="平台名称">
            <el-select v-model="searchForm.platformId" placeholder="请选择平台" clearable 
            style="width: 120px;"
            @change="handlePlatformChange">
              <el-option
                v-for="item in platformOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="模块编码">
            <el-input v-model="searchForm.moduleCode" placeholder="请输入模块编码" clearable />
          </el-form-item>
          <el-form-item label="模块名称">
            <el-input v-model="searchForm.moduleName" placeholder="请输入模块名称" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <!-- <el-table-column prop="module_code" label="模块编码" width="120" /> -->
        <el-table-column prop="name" label="模块名称" width="120" />
        <el-table-column prop="desc" label="模块描述" show-overflow-tooltip />
        <el-table-column prop="platform" label="所属平台" width="120" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="scope">
            {{ scope.row.status === '1' ? '启用' : '禁用' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>

      <!-- 模块表单对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'add' ? '新增模块' : '编辑模块'"
        width="50%"
      >
        <el-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-width="120px"
        >
          <el-form-item label="平台名称" prop="platform">
            <el-select v-model="formData.platform" placeholder="请选择平台">
              <el-option
                v-for="item in platformOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="模块编码" prop="module_code">
            <el-input v-model="formData.module_code" placeholder="请输入模块编码" />
          </el-form-item>
          <el-form-item label="模块名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入模块名称" />
          </el-form-item>
          <el-form-item label="模块描述" prop="description">
            <el-input
              v-model="formData.desc"
              type="textarea"
              :rows="3"
              placeholder="请输入模块描述"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="formData.status">
              <el-radio label="1">启用</el-radio>
              <el-radio label="0">禁用</el-radio>
            </el-radio-group>
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

// 搜索表单数据
const searchForm = reactive({
  platformId: '',
  moduleCode: '',
  moduleName: ''
})

// 表格数据
const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 平台选项
const platformOptions = ref([])

// 获取平台列表
const getPlatformList = async () => {
  try {
    const response = await request.get('/api/report/platforms/')
    platformOptions.value = response.data
  } catch (error) {
    console.error('获取平台列表失败：', error)
  }
}

// 获取模块列表
const getModuleList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      platform_id: searchForm.platformId,
      module_code: searchForm.moduleCode,
      name: searchForm.moduleName
    }
    const response = await request.get('/api/report/modules/', { params })
    tableData.value = response.data
    total.value = response.data.length
  } catch (error) {
    console.error('获取模块列表失败：', error)
    ElMessage.error('获取模块列表失败')
  } finally {
    loading.value = false
  }
}

// 平台变更处理
const handlePlatformChange = () => {
  handleSearch()
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  getModuleList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.platformId = ''
  searchForm.moduleCode = ''
  searchForm.moduleName = ''
  handleSearch()
}

// 分页大小变更处理
const handleSizeChange = (val) => {
  pageSize.value = val
  getModuleList()
}

// 当前页变更处理
const handleCurrentChange = (val) => {
  currentPage.value = val
  getModuleList()
}

// 表单数据
const formData = reactive({
  id: '',
  module_code: '',
  name: '',
  description: '',
  status: '1',
  platform: ''
})

// 表单校验规则
const rules = {
  platform: [{ required: true, message: '请选择平台', trigger: 'change' }],
  module_code: [{ required: true, message: '请输入模块编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入模块名称', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)

// 重置表单
const resetForm = () => {
  formData.id = ''
  formData.module_code = ''
  formData.name = ''
  formData.description = ''
  formData.status = '1'
  formData.platform = ''
}

// 新增模块
const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 编辑模块
const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    module_code: row.module_code,
    name: row.name,
    description: row.description,
    status: row.status,
    platform: row.platform
  })
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await request.post('/api/report/modules/', formData)
          ElMessage.success('添加成功')
        } else {
          await request.put(`/api/report/modules/${formData.id}/`, formData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        getModuleList()
      } catch (error) {
        console.error('保存模块失败：', error)
        ElMessage.error('保存失败')
      }
    }
  })
}

// 删除模块
const handleDelete = async (row) => {
  ElMessageBox.confirm(
    '确认删除该模块吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        await request.delete(`/api/report/modules/${row.id}/`)
        ElMessage.success('删除成功')
        getModuleList()
      } catch (error) {
        console.error('删除模块失败：', error)
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 页面加载时获取数据
onMounted(() => {
  getPlatformList()
  getModuleList()
})
</script>

<style scoped>
.module-manage {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-area {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>