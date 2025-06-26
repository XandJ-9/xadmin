<template>
  <div class="app-container">
      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="平台名称">
            <el-select v-model="searchForm.platformId" placeholder="请选择平台" clearable 
            style="width: 120px;"
            @click="fetchPlatformOptions"
            @change="handlePlatformChange">
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
            style="width: 120px;"
            @click="fetchModuleOptionsByPlatform"
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
            <el-input v-model="searchForm.reportName" placeholder="请输入报表名称" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    
    <!-- 数据列表 -->
    <el-table :data="reportList" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="报表名称" />
      <el-table-column prop="desc" label="描述" />
      <el-table-column prop="module_info.name" label="所属模块" />
      <el-table-column prop="module_info.platform_info.name" label="所属平台" />
      <el-table-column prop="create_time" label="创建时间" width="180" />
      <el-table-column prop="update_time" label="更新时间" width="180" />
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <!-- <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button> -->
        </template>
      </el-table-column>
    </el-table>

    <div class="card-footer">
          <div class="add-btn">
            <el-button type="primary" @click="handleAdd">新增报表</el-button>
          </div>

            <!-- 分页 -->
            <Pagination
                :total="total"
                :current-page="currentPage"
                :page-size="pageSize"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
      </div>
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <!-- 报表信息 -->
        <el-divider content-position="left">报表信息</el-divider>
        <el-form-item label="报表名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入报表名称" />
        </el-form-item>
        <el-form-item label="描述" prop="desc">
          <el-input
            v-model="form.desc"
            type="textarea"
            placeholder="请输入报表描述"
          />
        </el-form-item>
        
        <!-- 模块选择/创建 -->
        <el-divider content-position="left">所属模块</el-divider>
        <el-form-item label="选择方式" prop="moduleSelectType">
          <el-radio-group v-model="form.moduleSelectType" @change="handleModuleSelectTypeChange">
            <el-radio value="existing">选择已有模块</el-radio>
            <el-radio value="new">创建新模块</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 选择已有模块 -->
        <template v-if="form.moduleSelectType === 'existing'">
          <el-form-item label="所属模块" prop="module">
            <el-select v-model="form.module" placeholder="请选择所属模块"
            @click="fetchModuleOptions">
              <el-option
                v-for="item in moduleOptions"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
        </template>
        
        <!-- 创建新模块 -->
        <template v-else>
          <!-- 平台选择/创建 -->
          <el-form-item label="选择方式" prop="platformSelectType">
            <el-radio-group v-model="form.platformSelectType" @change="handlePlatformSelectTypeChange">
              <el-radio value="existing">选择已有平台</el-radio>
              <el-radio value="new">创建新平台</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <!-- 选择已有平台 -->
          <template v-if="form.platformSelectType === 'existing'">
            <el-form-item label="所属平台" prop="platform">
              <el-select v-model="form.platform" placeholder="请选择所属平台"
              @click="fetchPlatformOptions">
                <el-option
                  v-for="item in platformOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </template>
          
          <!-- 创建新平台 -->
          <template v-else>
            <el-form-item label="平台名称" prop="newPlatformName">
              <el-input v-model="form.newPlatformName" placeholder="请输入平台名称" />
            </el-form-item>
            <el-form-item label="平台描述" prop="newPlatformDesc">
              <el-input
                v-model="form.newPlatformDesc"
                type="textarea"
                placeholder="请输入平台描述"
              />
            </el-form-item>
            <el-form-item label="平台状态" prop="newPlatformStatus">
              <el-radio-group v-model="form.newPlatformStatus">
                <el-radio value="1">启用</el-radio>
                <el-radio value="0">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </template>
          
          <!-- 新模块信息 -->
          <el-form-item label="模块名称" prop="newModuleName">
            <el-input v-model="form.newModuleName" placeholder="请输入模块名称" />
          </el-form-item>
          <el-form-item label="模块描述" prop="newModuleDesc">
            <el-input
              v-model="form.newModuleDesc"
              type="textarea"
              placeholder="请输入模块描述"
            />
          </el-form-item>
          <el-form-item label="模块状态" prop="newModuleStatus">
            <el-radio-group v-model="form.newModuleStatus">
              <el-radio value="1">启用</el-radio>
              <el-radio value="0">禁用</el-radio>
            </el-radio-group>
          </el-form-item>
        </template>
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

<script>
export default {
    name: 'ReportManage',
}
</script>

<script setup>
import { ref, onMounted, reactive, watch, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination'
import { getPlatformList, createPlatform,
         getModuleList, getModulesByPlatform, createModule,
         getReportList, createReport, updateReport, deleteReport } from '@/api/dataassets/reportinfo'

const reportList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const moduleOptions = ref([])
const platformOptions = ref([])

// 搜索表单数据
const searchForm = reactive({
  platformId: '',
  moduleId: '',
  reportName: ''
})
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 表单数据
const form = ref({
  // 报表信息
  name: '',
  desc: '',
  module: '',
  
  // 模块选择方式
  moduleSelectType: 'existing', // existing 或 new
  
  // 新模块信息
  newModuleName: '',
  newModuleDesc: '',
  newModuleStatus: '1',
  
  // 平台选择方式
  platformSelectType: 'existing', // existing 或 new
  platform: '',
  
  // 新平台信息
  newPlatformName: '',
  newPlatformDesc: '',
  newPlatformStatus: '1'
})

// 表单校验规则
const rules = {
  // 报表信息验证
  name: [{ required: true, message: '请输入报表名称', trigger: 'blur' }],
  
  // 模块选择验证
  moduleSelectType: [{ required: true, message: '请选择模块选择方式', trigger: 'change' }],
  module: [{ required: true, message: '请选择所属模块', trigger: 'change' }],
  
  // 新模块信息验证
  newModuleName: [{ required: true, message: '请输入模块名称', trigger: 'blur' }],
  
  // 平台选择验证
  platformSelectType: [{ required: true, message: '请选择平台选择方式', trigger: 'change' }],
  platform: [{ required: true, message: '请选择所属平台', trigger: 'change' }],
  
  // 新平台信息验证
  newPlatformName: [{ required: true, message: '请输入平台名称', trigger: 'blur' }]
}

const formRef = ref(null)
const currentId = ref(null)

// 获取报表列表
const fetchReportList = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      platform_id: searchForm.platformId,
      module_id: searchForm.moduleId,
      name: searchForm.reportName
    }
    const response = await getReportList(params)
    reportList.value = response.data
    total.value = response.total
  } catch (error) {
    console.error('获取报表列表失败：', error)
    ElMessage.error('获取报表列表失败')
  }
}

// 获取平台列表
const fetchPlatformOptions = async () => {
  try {
    const response = await getPlatformList({ list_all: true })
    platformOptions.value = response.data
  } catch (error) {
    console.error('获取平台列表失败：', error)
    ElMessage.error('获取平台列表失败')
  }
}

// 获取模块列表
const fetchModuleOptions = async () => {
  try {
    const response = await getModuleList({ list_all: true })
    moduleOptions.value = response.data
  } catch (error) {
    console.error('获取模块列表失败：', error)
    ElMessage.error('获取模块列表失败')
  }
}

// 根据平台ID获取模块列表
const fetchModuleOptionsByPlatform = async () => {
  if (!searchForm.platformId) {
    await fetchModuleOptions()
    return
  }
  
  try {
    const response = await getModulesByPlatform(searchForm.platformId)
    moduleOptions.value = response.data
  } catch (error) {
    console.error('获取模块列表失败：', error)
    ElMessage.error('获取模块列表失败')
  }
}

// 平台变更处理
const handlePlatformChange = () => {
  searchForm.moduleId = ''
  fetchModuleOptionsByPlatform()
  handleSearch()
}

// 模块变更处理
const handleModuleChange = () => {
  handleSearch()
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchReportList()
}

// 重置搜索
const resetSearch = () => {
  searchForm.platformId = ''
  searchForm.moduleId = ''
  searchForm.reportName = ''
  handleSearch()
}

// 模块选择方式变更处理
const handleModuleSelectTypeChange = () => {
  if (form.value.moduleSelectType === 'existing') {
    // 重置新模块和平台相关字段
    form.value.newModuleName = ''
    form.value.newModuleDesc = ''
    form.value.newModuleStatus = '1'
    form.value.platformSelectType = 'existing'
    form.value.platform = ''
    form.value.newPlatformName = ''
    form.value.newPlatformDesc = ''
    form.value.newPlatformStatus = '1'
  }
}

// 平台选择方式变更处理
const handlePlatformSelectTypeChange = () => {
  if (form.value.platformSelectType === 'existing') {
    // 重置新平台相关字段
    form.value.newPlatformName = ''
    form.value.newPlatformDesc = ''
    form.value.newPlatformStatus = '1'
  } else {
    // 重置已有平台选择
    form.value.platform = ''
  }
}

// 新增报表
const handleAdd = () => {
  dialogTitle.value = '新增报表'
  form.value = {
    name: '',
    desc: '',
    module: '',
    moduleSelectType: 'existing',
    newModuleName: '',
    newModuleDesc: '',
    newModuleStatus: '1',
    platformSelectType: 'existing',
    platform: '',
    newPlatformName: '',
    newPlatformDesc: '',
    newPlatformStatus: '1'
  }
  currentId.value = null
  dialogVisible.value = true
}

// 编辑报表
const handleEdit = (row) => {
  dialogTitle.value = '编辑报表'
  form.value = {
    name: row.name,
    desc: row.desc,
    module: row.module,
    moduleSelectType: 'existing',
    newModuleName: '',
    newModuleDesc: '',
    newModuleStatus: '1',
    platformSelectType: 'existing',
    platform: '',
    newPlatformName: '',
    newPlatformDesc: '',
    newPlatformStatus: '1'
  }
  currentId.value = row.id
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('删除报表会连带下属所有接口被清理，请仔细确认是否删除该报表?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteReport(row.id)
        ElMessage.success('删除成功')
        fetchReportList()
      } catch (error) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 编辑报表
        if (currentId.value) {
          const reportData = {
            name: form.value.name,
            desc: form.value.desc,
            module: form.value.module
          }
          await updateReport(currentId.value, reportData)
          ElMessage.success('更新成功')
          dialogVisible.value = false
          fetchReportList()
          return
        }
        
        // 新增报表 - 使用已有模块
        if (form.value.moduleSelectType === 'existing') {
          const reportData = {
            name: form.value.name,
            desc: form.value.desc,
            module: form.value.module
          }
          await createReport(reportData)
          ElMessage.success('创建成功')
          dialogVisible.value = false
          fetchReportList()
          return
        }
        
        // 新增报表 - 创建新模块
        let moduleId = null
        
        // 使用已有平台创建新模块
        if (form.value.platformSelectType === 'existing') {
          // 创建新模块
          const moduleData = {
            name: form.value.newModuleName,
            desc: form.value.newModuleDesc,
            status: form.value.newModuleStatus,
            platform: form.value.platform
          }
          const moduleResponse = await createModule(moduleData)
          moduleId = moduleResponse.data.id
        } 
        // 创建新平台和新模块
        else {
          // 创建新平台
          const platformData = {
            name: form.value.newPlatformName,
            description: form.value.newPlatformDesc,
            status: form.value.newPlatformStatus
          }
          const platformResponse = await createPlatform(platformData)
          const platformId = platformResponse.data.id
          
          // 创建新模块
          const moduleData = {
            name: form.value.newModuleName,
            desc: form.value.newModuleDesc,
            status: form.value.newModuleStatus,
            platform: platformId
          }
          const moduleResponse = await createModule(moduleData)
          moduleId = moduleResponse.data.id
        }
        
        // 创建新报表
        const reportData = {
          name: form.value.name,
          desc: form.value.desc,
          module: moduleId
        }
        await createReport(reportData)
        
        ElMessage.success('创建成功')
        dialogVisible.value = false
        fetchReportList()
        // 刷新平台和模块选项
        fetchPlatformOptions()
        fetchModuleOptions()
      } catch (error) {
        console.error('保存失败：', error)
        ElMessage.error(currentId.value ? '更新失败' : '创建失败')
      }
    }
  })
}

// 分页大小变更处理
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchReportList()
}

// 当前页变更处理
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchReportList()
}

// 页面加载时初始化数据
onMounted(() => {
  fetchReportList()
  fetchPlatformOptions()
  fetchModuleOptions()
})
</script>

<style scoped>
.report-info-container {
  padding: 20px;
}

.header-actions {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.add-btn {
  margin-bottom: 20px;
}

</style>