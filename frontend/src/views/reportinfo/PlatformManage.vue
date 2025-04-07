<template>
  <div class="platform-manage">
        <div class="card-header">
          <el-button type="primary" @click="handleAdd">新增平台</el-button>
        </div>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <!-- <el-form-item label="平台编码">
            <el-input v-model="searchForm.platformCode" placeholder="请输入平台编码" clearable />
          </el-form-item> -->
          <el-form-item label="平台名称">
            <el-input v-model="searchForm.platformName" placeholder="请输入平台名称" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <!-- <el-table-column prop="platform_code" label="平台编码" width="120" /> -->
        <el-table-column prop="name" label="平台名称" width="120" />
        <el-table-column prop="description" label="平台描述" show-overflow-tooltip />
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

      <!-- 平台表单对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'add' ? '新增平台' : '编辑平台'"
        width="50%"
      >
        <el-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-width="120px"
        >
          <el-form-item label="平台名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入平台名称" />
          </el-form-item>
          <el-form-item label="平台描述" prop="description">
            <el-input
              v-model="formData.description"
              type="textarea"
              :rows="3"
              placeholder="请输入平台描述"
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
  platformCode: '',
  platformName: ''
})

// 表格数据
const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 获取平台列表
const getPlatformList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      platform_code: searchForm.platformCode,
      name: searchForm.platformName
    }
    const response = await request.get('/api/report/platforms/', { params })
    tableData.value = response.data
    total.value = response.data.length
  } catch (error) {
    console.error('获取平台列表失败：', error)
    ElMessage.error('获取平台列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  getPlatformList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.platformCode = ''
  searchForm.platformName = ''
  handleSearch()
}

// 分页大小变更处理
const handleSizeChange = (val) => {
  pageSize.value = val
  getPlatformList()
}

// 当前页变更处理
const handleCurrentChange = (val) => {
  currentPage.value = val
  getPlatformList()
}

// 表单数据
const formData = reactive({
  id: '',
  platform_code: '',
  name: '',
  description: '',
  status: '1'
})

// 表单校验规则
const rules = {
  name: [{ required: true, message: '请输入平台名称', trigger: 'blur', description: '名称必须唯一' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)

// 重置表单
const resetForm = () => {
  formData.id = ''
  formData.platform_code = ''
  formData.name = ''
  formData.description = ''
  formData.status = '1'
}

// 新增平台
const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 编辑平台
const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    platform_code: row.platform_code,
    name: row.name,
    description: row.description,
    status: row.status
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
          await request.post('/api/report/platforms/', formData)
          ElMessage.success('添加成功')
        } else {
          await request.put(`/api/report/platforms/${formData.id}/`, formData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        getPlatformList()
      } catch (error) {
        console.error('保存平台失败：', error)
        ElMessage.error('保存失败')
      }
    }
  })
}

// 删除平台
const handleDelete = async (row) => {
  ElMessageBox.confirm(
    '确认删除该平台吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        await request.delete(`/api/report/platforms/${row.id}/`)
        ElMessage.success('删除成功')
        getPlatformList()
      } catch (error) {
        console.error('删除平台失败：', error)
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
})
</script>

<style scoped>
.platform-manage {
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