<template>
  <div class="interface-manage">
      <template #header>
        <div class="card-header">
          <span>接口管理</span>
          <el-button type="primary" @click="handleAdd">新增接口</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="平台名称">
            <el-select v-model="searchForm.platformId" placeholder="请选择平台" clearable @change="handlePlatformChange">
              <el-option
                v-for="item in platformOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="模块名称">
            <el-select v-model="searchForm.moduleId" placeholder="请选择模块" clearable @change="handleModuleChange">
              <el-option
                v-for="item in moduleOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="报表名称">
            <el-select v-model="searchForm.reportId" placeholder="请选择报表" clearable>
              <el-option
                v-for="item in reportOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="接口编码">
            <el-input v-model="searchForm.interfaceCode" placeholder="请输入接口编码" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="interface_code" label="接口编码" width="150" />
        <el-table-column prop="interface_name" label="接口名称" />
        <el-table-column prop="interface_desc" label="接口描述" show-overflow-tooltip />
        <el-table-column prop="interface_db_type" label="数据库类型"/>
        <el-table-column prop="interface_db_name" label="数据库名称"/>
        <el-table-column prop="is_total" label="是否合计">
          <template #default="scope">
            {{ scope.row.is_total === '1' ? '是' : '否' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_paging" label="是否分页" width="80">
          <template #default="scope">
            {{ scope.row.is_paging === '1' ? '是' : '否' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_date_option" label="是否日期查询">
          <template #default="scope">
            {{ scope.row.is_date_option === '1' ? '是' : '否' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" min-width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="small" type="success" @click="handleFields(scope.row)">字段配置</el-button>
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

      <!-- 接口表单对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'add' ? '新增接口' : '编辑接口'"
        width="50%"
      >
        <el-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-width="120px"
        >
          <el-form-item label="平台名称" prop="platform">
            <el-select v-model="formData.platform" placeholder="请选择平台" @change="handleFormPlatformChange">
              <el-option
                v-for="item in platformOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="模块名称" prop="module">
            <el-select v-model="formData.module" placeholder="请选择模块" @change="handleFormModuleChange">
              <el-option
                v-for="item in moduleOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="报表名称" prop="report">
            <el-select v-model="formData.report" placeholder="请选择报表">
              <el-option
                v-for="item in reportOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="接口编码" prop="interface_code">
            <el-input v-model="formData.interface_code" placeholder="请输入接口编码" />
          </el-form-item>
          <el-form-item label="接口名称" prop="interface_name">
            <el-input v-model="formData.interface_name" placeholder="请输入接口名称" />
          </el-form-item>
          <el-form-item label="接口描述" prop="interface_desc">
            <el-input
              v-model="formData.interface_desc"
              type="textarea"
              :rows="3"
              placeholder="请输入接口描述"
            />
          </el-form-item>
          <el-form-item label="数据库类型" prop="interface_db_type">
            <el-select v-model="formData.interface_db_type" placeholder="请选择数据库类型">
              <el-option label="MySQL" value="mysql" />
              <el-option label="Oracle" value="oracle" />
              <el-option label="PostgreSQL" value="postgresql" />
            </el-select>
          </el-form-item>
          <el-form-item label="数据库名称" prop="interface_db_name">
            <el-input v-model="formData.interface_db_name" placeholder="请输入数据库名称" />
          </el-form-item>
          <el-form-item label="是否合计" prop="is_total">
            <el-radio-group v-model="formData.is_total">
              <el-radio label="1">是</el-radio>
              <el-radio label="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="是否分页" prop="is_paging">
            <el-radio-group v-model="formData.is_paging">
              <el-radio label="1">是</el-radio>
              <el-radio label="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="是否日期查询" prop="is_date_option">
            <el-radio-group v-model="formData.is_date_option">
              <el-radio label="1">是</el-radio>
              <el-radio label="0">否</el-radio>
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
import { useRouter } from 'vue-router'


const router = useRouter()
// 搜索表单数据
const searchForm = reactive({
  platformId: '',
  moduleId: '',
  reportId: '',
  interfaceCode: ''
})

// 表格数据
const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 选项数据
const platformOptions = ref([])
const moduleOptions = ref([])
const reportOptions = ref([])

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
const getModuleList = async (platformId) => {
  try {
    const response = await request.get(`/api/report/modules/?platform_id=${platformId}`)
    moduleOptions.value = response.data
  } catch (error) {
    console.error('获取模块列表失败：', error)
  }
}

// 获取报表列表
const getReportList = async (moduleId) => {
  try {
    const response = await request.get(`/api/report/reports/?module_id=${moduleId}`)
    reportOptions.value = response.data
  } catch (error) {
    console.error('获取报表列表失败：', error)
  }
}

// 获取接口列表
const getInterfaceList = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      platform_id: searchForm.platformId,
      module_id: searchForm.moduleId,
      report_id: searchForm.reportId,
      interface_code: searchForm.interfaceCode
    }
    const response = await request.get('/api/report/interfaces/', { params })
    tableData.value = response.data.data.data
    total.value = response.data.data.total
  } catch (error) {
    console.error('获取接口列表失败：', error)
    ElMessage.error('获取接口列表失败')
  } finally {
    loading.value = false
  }
}

// 平台变更处理
const handlePlatformChange = (value) => {
  searchForm.moduleId = ''
  searchForm.reportId = ''
  moduleOptions.value = []
  reportOptions.value = []
  if (value) {
    getModuleList(value)
  }
}

// 模块变更处理
const handleModuleChange = (value) => {
  searchForm.reportId = ''
  reportOptions.value = []
  if (value) {
    getReportList(value)
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  getInterfaceList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.platformId = ''
  searchForm.moduleId = ''
  searchForm.reportId = ''
  searchForm.interfaceCode = ''
  moduleOptions.value = []
  reportOptions.value = []
  handleSearch()
}

// 分页大小变更处理
const handleSizeChange = (val) => {
  pageSize.value = val
  getInterfaceList()
}

// 当前页变更处理
const handleCurrentChange = (val) => {
  currentPage.value = val
  getInterfaceList()
}

// 表单数据
const formData = reactive({
  id: '',
  interface_code: '',
  interface_name: '',
  interface_desc: '',
  interface_db_type: '',
  interface_db_name: '',
  is_total: '0',
  is_paging: '0',
  is_date_option: '0',
  platform: '',
  module: '',
  report: ''
})

// 表单校验规则
const rules = {
  interface_code: [{ required: true, message: '请输入接口编码', trigger: 'blur' }],
  interface_name: [{ required: true, message: '请输入接口名称', trigger: 'blur' }],
  interface_db_type: [{ required: true, message: '请选择数据库类型', trigger: 'change' }],
  interface_db_name: [{ required: true, message: '请输入数据库名称', trigger: 'blur' }],
  platform: [{ required: true, message: '请选择平台', trigger: 'change' }],
  module: [{ required: true, message: '请选择模块', trigger: 'change' }],
  report: [{ required: true, message: '请选择报表', trigger: 'change' }]
}

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)

// 重置表单
const resetForm = () => {
  formData.id = ''
  formData.interface_code = ''
  formData.interface_name = ''
  formData.interface_desc = ''
  formData.interface_db_type = ''
  formData.interface_db_name = ''
  formData.is_total = '0'
  formData.is_paging = '0'
  formData.is_date_option = '0'
  formData.platform = ''
  formData.module = ''
  formData.report = ''
}

// 新增接口
const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 编辑接口
const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(formData, {
    id: row.id,
    interface_code: row.interface_code,
    interface_name: row.interface_name,
    interface_desc: row.interface_desc,
    interface_db_type: row.interface_db_type,
    interface_db_name: row.interface_db_name,
    is_total: row.is_total,
    is_paging: row.is_paging,
    is_date_option: row.is_date_option,
    platform: row.platform,
    module: row.module,
    report: row.report
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
          await request.post('/api/report/interfaces/', formData)
          ElMessage.success('添加成功')
        } else {
          await request.put(`/api/report/interfaces/${formData.id}/`, formData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        getInterfaceList()
      } catch (error) {
        console.error('保存接口失败：', error)
        ElMessage.error('保存失败')
      }
    }
  })
}

// 删除接口
const handleDelete = async (row) => {
  ElMessageBox.confirm(
    '确认删除该接口吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        await request.delete(`/api/report/interfaces/${row.id}/`)
        ElMessage.success('删除成功')
        getInterfaceList()
      } catch (error) {
        console.error('删除接口失败：', error)
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}


// 跳转到字段配置页面
const handleFields = (row) => {
  router.push(`/interface-fields/${row.id}`)
}

// 页面加载时获取数据
onMounted(() => {
  getPlatformList()
  getModuleList()
  getReportList()
  getInterfaceList()
})
</script>

<style scoped>
.interface-manage {
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