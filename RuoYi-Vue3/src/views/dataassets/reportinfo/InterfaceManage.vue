<template>
  <div class="app-container">
    <query-params-form :properties="queryProperties" 
     @query="handleQuery"
     @select-change="handleSelectChange" 
     @select-click="handleSelectClick" />

      <!-- 数据表格 -->
      <el-table ref="tableRef" :data="tableData" style="width: 100%" v-loading="loading" fit highlight-current-row>
        <el-table-column prop="interface_code" label="接口编码" show-overflow-tooltip />
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
        <el-table-column label="操作" min-width="350">
          <template #default="scope">
            <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="small" type="success" @click="handleFields(scope.row)">字段配置</el-button>
            <el-button size="small" type="info" @click="handleExport(scope.row)">导出</el-button>
            <el-button size="small" type="warning" @click="handleDataview(scope.row)">查询</el-button>
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
            <Pagination
                :total="total"
                :current-page="currentPage"
                :page-size="pageSize"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
      </div>
       
      <!-- 文件上传对话框 -->
      <el-dialog
        v-model="importVisible"
        title="选择上传文件"
        width="50%"
      >
          <el-upload
              ref="uploadRef"
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
          <el-form-item label="报表名称" prop="report">
            <el-select v-model="formData.report" placeholder="请选择报表"
            @focus="fetchReportOptions">
              <el-option
                v-for="item in reportOptions"
                :key="item.id"
                :label="item.label"
                :value="item.value"
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
            <el-select v-model="formData.interface_db_type" placeholder="请选择数据库类型" @click="fetchDataSourceOptions">
               <el-option v-for="item in dataSourceOptions" :key="item.id" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="数据库名称" prop="interface_db_name">
            <el-input v-model="formData.interface_db_name" placeholder="请输入数据库名称" />
          </el-form-item>
          <el-form-item label="是否合计" prop="is_total">
            <el-radio-group v-model="formData.is_total">
              <el-radio value="1">是</el-radio>
              <el-radio value="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="是否分页" prop="is_paging">
            <el-radio-group v-model="formData.is_paging">
              <el-radio value="1">是</el-radio>
              <el-radio value="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="是否日期查询" prop="is_date_option">
            <el-radio-group v-model="formData.is_date_option">
              <el-radio value="1">是</el-radio>
              <el-radio value="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="接口sql" prop="interface_sql">
            <el-input
              v-model="formData.interface_sql"
              type="textarea"
              placeholder="请输入接口sql"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSubmit">确定</el-button>
          </span>
        </template>
      </el-dialog>
      
    <!-- </div> -->
      <!-- 接口字段编辑窗口 -->
    <div class="field-editor-view">
        <router-view />
    </div>
  
  </div>
</template>

<script setup name="InterfaceManage">
import { ref, onMounted, reactive, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import QueryParamsForm from '@/components/QueryParamsForm'
import Pagination from '@/components/Pagination'
import { getDataSourceTypeList } from '@/api/dataassets/datasource'
import { getPlatformList, getModuleList, getReportList, getInterfaceList, updateInterface, createInterface, deleteInterface, importInterface} from '@/api/dataassets/reportinfo'

const router = useRouter()

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
const dataSourceOptions = ref([])

// 指定搜索条件字段信息
const queryProperties = reactive([
    { label: '平台名称', prop: 'platformId', type: 'select', options: platformOptions },
    { label: '模块名称', prop: 'moduleId', type: 'select', options: moduleOptions },
    { label: '报表名称', prop: 'reportId', type: 'select', options: reportOptions },
    { label: '数据源类型', prop: 'dataSourceType', type: 'select', options: dataSourceOptions },
    { label: '接口编码', prop: 'interfaceCode', type: 'input' }
])

const fetchPlatformOptions = async () => {
    await getPlatformList({noPage: 1}).then((response) => {
        platformOptions.value = []
        let arr = response.data
        arr.forEach(item => {
            platformOptions.value.push({
                id: item.id,
                label: item.name,
                value: item.id
            })
        })
    }).catch(error => {
        ElMessage.error('获取平台列表失败')
      })
}

const fetchModuleOptions = async (platformId) => {
  await getModuleList({ platformId, noPage: 1 }).then((res) => {
        moduleOptions.value = []
        let arr = res.data
        arr.forEach(item => {
            moduleOptions.value.push({
                id: item.id,
                label: item.name,
                value: item.id
            })
        })
    }).catch(error => {
          ElMessage.error('获取模块列表失败')
        })
}

const fetchReportOptions = async (moduleId) => {
    await getReportList({ moduleId, noPage:1 }).then((res) => {
      reportOptions.value = []
      let arr = res.data
        arr.forEach(item => {
            reportOptions.value.push({
                id: item.id,
                label: item.name,
                value: item.id
            })
        })
    }).catch(error => {
        ElMessage.error('获取报表列表失败')
    })
}

const fetchDataSourceOptions = async () => {
  await getDataSourceTypeList().then((res) => {
    dataSourceOptions.value = []
    let arr = res
    arr.forEach(item => {
      dataSourceOptions.value.push({
        label: item[0],
        value: item[0]
      })
    })
  }).catch(error => {
    ElMessage.error('获取数据源类型列表失败')
  })
}

// 获取接口列表
const fetchInterfaceList = async (queryParams) => {
    loading.value = true
    const params = {
        page: currentPage.value,
        page_size: pageSize.value,
        platform_id: queryParams?.platformId,
        module_id: queryParams?.moduleId,
        report_id: queryParams?.reportId,
        interface_code: queryParams?.interfaceCode
    }

    await getInterfaceList(params).then(res => {
        tableData.value = res.data
        total.value = res.total
    }).catch(err => {
        ElMessage.error('获取接口列表失败')
    }).finally(() => {
        loading.value = false
    })
}

// 处理搜索条件变更
const handleSelectChange = (queryParams) => {
    // console.log("select-change", queryParams)
    // 每次条件变更时，变更选项信息
    let { moduleId, platformId } = queryParams
    fetchPlatformOptions()
    fetchModuleOptions(platformId)
    fetchReportOptions(moduleId)
    fetchDataSourceOptions()
}

// 点击选项框时，调用该方法
const handleSelectClick = (event) => {
    // console.log("select-click",event)
}

// 搜索处理
const handleQuery = (queryParams) => {
  currentPage.value = 1
  fetchInterfaceList(queryParams)
}

// 重置搜索
const resetQuery = () => {
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
  interface_sql: '',
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
  formData.interface_sql = ''
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
    interface_sql: row.interface_sql,
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
            // await request.post('/report/interfaces/', formData)
          await createInterface(formData)
          ElMessage.success('添加成功')
        } else {
            //   await request.put(`/report/interfaces/${formData.id}/`, formData)
          await updateInterface(formData.id, formData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchInterfaceList()
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
        await deleteInterface(row.id)
        ElMessage.success('删除成功')
        fetchInterfaceList()
    })
}

// 跳转到字段配置页面
const handleFields = async (row) => {
    router.push({ path: '/reportinfo/interface/fields', query: { interface_id: row.id } })
    // fieldEditorVisible.value = true
    //   router.push(`/report/interface-fields/${row.id}`)
    // tableRef.value.toggleRowExpansion(row, true)
    // const response = await request.get(`/report/interface-fields/?noPage=1&interface=${row.id}`)
}

const download = inject('download')

// 导出接口到excel
const handleExport = (row) => {
    download(`/report/export/Interfaceinfo/`, 'POST', {interface_id: row.id}, '接口信息.xlsx')
}

const uploadRef = ref(null)
const importVisible = ref(false)

const handleImport = () => {
    importVisible.value = true
}

const handleSubmitImport = async () => {
  uploadRef.value.submit()
}

const handleUpload = (options) => {

    // request.post('/report/interfaces/importInterfaceinfo/', formData, { headers })
    importInterface(options.file).then((response) => {
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


const handleDataview = (row) => {
    // const matched_routes = router.resolve({ path: `/reportinfo/interface/view/${row.id}` }).matched
    // if (matched_routes.length > 0) {
    //     console.log('跳转路由', matched_routes)
    //     router.push({
    //         path: `/reportinfo/interface/view/${row.id}`,
    //         query: { interface_name: row.interface_name },
    //     })
    // } else {
    // }
    // router.push({ path: `/reportinfo/view/${row.id}`, query: { interface_name: row.interface_name } })
    router.push({ path: `/report/interface/interfaceDataView/${row.id}`, query: { interface_name: row.interface_name } })
    .then(() => {
        console.log('跳转成功')
    })
    .catch((error) => {
        console.error('跳转失败', error)
        ElMessage.warning('路由信息不存在')
    })
}

// 页面加载时获取数据
onMounted(() => {
  // initOptions()
  fetchPlatformOptions()
  fetchModuleOptions()
  fetchReportOptions()
  fetchDataSourceOptions()
  fetchInterfaceList()
})
</script>

<style scoped>
.interface-manage {
  padding: 20px;
  /* height: 100%; */
  /* display: flex; */
  /* flex-direction: column; */
}

.search-area {
  margin-bottom: 20px;
}

.add-btn {
  margin-bottom: 20px;
}

.el-table__expand-icon{
    display: none;
}
</style>