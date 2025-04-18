<template>
  <div class="interface-manage">
    <div v-if="route.path === '/reportinfo/interface'">
      <!-- 搜索区域 -->
    <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="平台名称">
            <el-select v-model="searchForm.platformId" placeholder="请选择平台" clearable 
            style="display: inline-block; width: 120px;"
            @change="handlePlatformChange"
            @click="getPlatformList">
              <el-option
                v-for="item in platformOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="模块名称">
            <el-select v-model="searchForm.moduleId" placeholder="请选择模块" clearable
            style="display: inline-block; width: 120px;"
            @change="handleModuleChange">
              <el-option
                v-for="item in moduleOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="报表名称">
            <el-select v-model="searchForm.reportId" placeholder="请选择报表" clearable
            style="display: inline-block; width: 120px;">
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
      <el-table ref="tableRef" :data="tableData" style="width: 100%" v-loading="loading" border>
        <el-table-column fixed prop="interface_code" label="接口编码" width="100" />
        <el-table-column prop="interface_name" label="接口名称" />
        <el-table-column prop="interface_desc" label="接口描述" show-overflow-tooltip >
            <template #default="scope">
                {{ scope.row.interface_desc ? scope.row.interface_desc : scope.row.interface_name }}
            </template>
        </el-table-column>
        <el-table-column prop="report_info.name" label="报表名称"/>
        <el-table-column prop="report_info.module_info.name" label="模块名称"/>
        <el-table-column prop="report_info.module_info.platform_info.name" label="平台名称"/>
        <el-table-column prop="interface_url" label="接口地址" show-overflow-tooltip />
        <el-table-column prop="interface_db_type" label="数据库类型"/>
        <el-table-column prop="interface_db_name" label="数据库名称"/>
        <el-table-column prop="is_total" label="是否合计">
          <template #default="scope">
            {{ scope.row.is_total }}
          </template>
        </el-table-column>
        <el-table-column prop="is_paging" label="是否分页" width="80">
          <template #default="scope">
            {{ scope.row.is_paging }}
          </template>
        </el-table-column>
        <el-table-column prop="is_date_option" label="是否日期查询">
          <template #default="scope">
            {{ scope.row.is_date_option }}
          </template>
        </el-table-column>
        <el-table-column prop="is_login_visit" label="是否需要登录">
            <template #default="scope">
                {{ scope.row.is_login_visit }}
            </template>
        </el-table-column>
        <el-table-column prop="updator_username" label="更新用户">
        </el-table-column>
        <el-table-column prop="update_time" label="更新时间" width="150">
          <template #default="scope">
            {{ scope.row.update_time }}
          </template>
        </el-table-column>
        <el-table-column prop="creator_username" label="创建用户">
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="150">
          <template #default="scope">
            {{ scope.row.create_time }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" min-width="300">
          <template #default="scope">
            <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="small" type="success" @click="handleFields(scope.row)">字段配置</el-button>
            <el-button size="small" type="info" @click="handleExport(scope.row)">导出</el-button>
          </template>
        </el-table-column>
        <!-- <el-table-column type="expand" width="50">
            <template>
                <interface-fields-editor :table-data="interfaceFields" />
            </template>
        </el-table-column> -->
      </el-table>

      <div class="card-footer">
          <div class="add-btn">
            <el-button type="primary" @click="handleAdd">新增接口</el-button>
            <el-button type="primary" @click="handleImport">模板导入</el-button>
          </div>
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
      </div>

      <el-dialog
        v-model="importVisible"
        title="选择上传文件"
        width="50%"
      >
          <el-upload
              ref="uploadRef"
              :action="importExcelUrl"
              class="upload-demo"
              :auto-upload="false"
              :http-request="handleUpload"
          >
              <el-button type="primary">选择文件</el-button>
              <template #tip>
                <div class="el-upload__tip">只能上传xlsx/xls文件，且不超过10MB</div>
              </template>
          </el-upload>
            <template #footer>
          <span class="dialog-footer">
            <el-button @click="importVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSubmitImport">确定</el-button>
          </span>
        </template>
      </el-dialog>

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
        <!-- 
         报表的平台模块信息放在报表设计中修改
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
          <el-form-item label="模块名称" prop="module">
            <el-select v-model="formData.module" placeholder="请选择模块">
              <el-option
                v-for="item in moduleOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
        -->
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
            <el-select v-model="formData.interface_db_type" placeholder="请选择数据库类型" @click="getDatasourceList">
              <!-- <el-option label="MySQL" value="mysql" /> -->
              <!-- <el-option label="Oracle" value="oracle" /> -->
              <!-- <el-option label="PostgreSQL" value="postgresql" /> -->
               <el-option v-for="item in datasourceOptions" :key="item.id" :label="item.type" :value="item.type" />
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
      <!-- 接口字段编辑窗口 -->
    <div class="field-editor-view">
        <router-view />
    </div>
  
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import request from '@/utils/request'
// import InterfaceFields from './InterfaceFields.vue'
const router = useRouter()
const route = useRoute()

// 搜索表单数据
const searchForm = reactive({
  platformId: '',
  moduleId: '',
  reportId: '',
  interfaceCode: ''
})

const tableRef = ref(null)
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
const datasourceOptions = ref([])

// 获取支持的数据库类型
const getDatasourceList = async () => {
  try {
    const response = await request.get('/api/datasources/types/')
    datasourceOptions.value = response.data
  } catch (error) {
    console.error('获取数据库类型列表失败：', error)
  }
}

// 获取平台列表
const getPlatformList = async () => {
  try {
    const response = await request.get('/api/report/platforms/list_all/')
    platformOptions.value = response.data.data
  } catch (error) {
    console.error('获取平台列表失败：', error)
  }
}

// 获取模块列表
const getModuleList = async (platformId) => {
  try {
    const response = await request.get(`/api/report/modules/?platform_id=${platformId}&noPage=1`)
    moduleOptions.value = response.data.data
  } catch (error) {
    console.error('获取模块列表失败：', error)
  }
}

// 获取报表列表
const getReportList = async (moduleId) => {
  try {
    const response = await request.get(`/api/report/reports/?module_id=${moduleId}&noPage=1`)
      reportOptions.value = response.data.data
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
    platform: row.report_info.module_info.platform,
    module: row.report_info.module,
    report: row.report
  })
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
        if (dialogType.value === 'add') {
          await request.post('/api/report/interfaces/', formData)
          ElMessage.success('添加成功')
        } else {
          await request.put(`/api/report/interfaces/${formData.id}/`, formData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        getInterfaceList()
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
        await request.delete(`/api/report/interfaces/${row.id}/`)
        ElMessage.success('删除成功')
        getInterfaceList()
    })
}

// 跳转到字段配置页面
const handleFields = async (row) => {
    router.push({ path: '/reportinfo/interface/fields', query: { interface_id: row.id } })
    // fieldEditorVisible.value = true
    //   router.push(`/api/report/interface-fields/${row.id}`)
    // tableRef.value.toggleRowExpansion(row, true)
    // const response = await request.get(`/api/report/interface-fields/?noPage=1&interface=${row.id}`)
    
}

const download = inject('download')

// 导出接口到excel
const handleExport = (row) => {
    // request.post(`/api/report/interfaces/exportInterfaceinfo/`,{interface_id: row.id}).then((response) => {})
    download(`/api/report/export/Interfaceinfo/`, 'POST', {interface_id: row.id}, '接口信息.xlsx')
}

const uploadRef = ref(null)
const importVisible = ref(false)
const importExcelUrl = ref('/api/report/interfaces/importInterfaceinfo/')

const handleImport = () => {
    importExcelUrl.value = '/api/report/import/Interfaceinfo/'
    importVisible.value = true
}

const handleSubmitImport = async () => {
  uploadRef.value.submit()
}

const handleUpload = (options) => {
  const formData = new FormData()
  formData.append('file', options.file)
  request.post(importExcelUrl.value, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then((response) => {
    ElMessage.success('导入成功')
    options.onSuccess = () => {
      console.log('上传成功')
    }
    importVisible.value = false
    uploadRef.value.clearFiles()
    getInterfaceList()
  }).catch((error) => {
    console.error('导入失败：', error)
    ElMessage.error('导入失败')
  })
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

/* .search-area {
  margin-bottom: 20px;
} */

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}
.add-btn {
  margin-bottom: 20px;
}
.pagination-container {
  display: flex;
  justify-content: flex-end;
}

.el-table__expand-icon{
    display: none;
}
</style>