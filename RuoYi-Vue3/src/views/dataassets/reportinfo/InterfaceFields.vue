<template>
  <div class="app-container">
    
      <span style="margin-bottom: 10px;">接口字段配置 - {{ interfaceInfo?.interface_name }}</span>

      <!-- 数据表格 -->
      <el-table :data="tableData" style="width: 100%" v-loading="loading" border fit>
        <el-table-column prop="interface_para_code" label="参数编码"/>
        <el-table-column prop="interface_para_name" label="参数名称" width="120" />
        <el-table-column prop="interface_para_position" label="参数位置" width="100" />
        <el-table-column prop="interface_para_type" label="参数类型" width="100">
          <template #default="scope">
            {{ scope.row.interface_para_type }}
          </template>
        </el-table-column>
        <el-table-column prop="interface_data_type" label="数据类型" width="100">
          <template #default="scope">
            {{ getDataTypeName(scope.row.interface_data_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="interface_para_default" label="默认值" show-overflow-tooltip/>
        <el-table-column prop="interface_show_flag" label="是否显示" width="100">
          <template #default="scope">
            {{ scope.row.interface_show_flag === '1' ? '是' : '否' }}
          </template>
        </el-table-column>
        <el-table-column prop="interface_export_flag" label="是否导出" width="100">
          <template #default="scope">
            {{ scope.row.interface_export_flag === '1' ? '是' : '否' }}
          </template>
        </el-table-column>
        <el-table-column prop="interface_para_desc" label="参数描述" show-overflow-tooltip />
        <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="small" icon="Plus" @click="handleAppend(scope.row)" v-hasPermi="['system:user:add']">添加</el-button>
          </template>
        </el-table-column>
      </el-table>


      <div class="card-footer">
        <div>
            <el-button type="primary" @click="goInterfaceList">返回接口列表</el-button>
            <el-button type="primary" @click="handleAdd">新增字段</el-button>
        </div>

        <!-- 分页 -->
        <pagination
            :total="total"
            :current-page="currentPage"
            :page-size="pageSize"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </div>
      <!-- 字段编辑对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'add' ? '新增字段' : '编辑字段'"
        width="50%"
      >
        <el-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          label-width="120px"
        >
          <el-form-item label="参数编码" prop="interface_para_code">
            <el-input v-model="formData.interface_para_code" />
          </el-form-item>
          <el-form-item label="参数名称" prop="interface_para_name">
            <el-input v-model="formData.interface_para_name" />
          </el-form-item>
          <el-form-item label="参数位置" prop="interface_para_position">
            <el-input-number v-model="formData.interface_para_position" :min="1" />
          </el-form-item>
          <el-form-item label="参数类型" prop="interface_para_type">
            <el-select v-model="formData.interface_para_type">
              <el-option label="输入参数" value="1" />
              <el-option label="输出参数" value="2" />
            </el-select>
          </el-form-item>
          <el-form-item label="数据类型" prop="interface_data_type">
            <el-select v-model="formData.interface_data_type">
              <el-option
                v-for="item in dataTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="默认值" prop="interface_para_default">
            <el-input v-model="formData.interface_para_default" />
          </el-form-item>
          <el-form-item label="是否显示" prop="interface_show_flag">
            <el-radio-group v-model="formData.interface_show_flag">
              <el-radio value="1">是</el-radio>
              <el-radio value="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="是否导出" prop="interface_export_flag">
            <el-radio-group v-model="formData.interface_export_flag">
              <el-radio value="1">是</el-radio>
              <el-radio value="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="参数描述" prop="interface_para_desc">
            <el-input
              v-model="formData.interface_para_desc"
              type="textarea"
              :rows="3"
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
  </div>
</template>


<script setup name="InterfaceFields">
import { ref, onMounted, reactive } from 'vue'
import { useRoute , useRouter} from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { getInterfaceDetail, getInterfaceFields } from '@/api/dataassets/reportinfo'

const router = useRouter()
const route = useRoute()
const interfaceId = route.query.interface_id

// 接口信息
const interfaceInfo = ref(null)

// 表格数据
const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)
const formData = reactive({
  interface_para_code: '',
  interface_para_name: '',
  interface_para_position: 1,
  interface_para_type: '2',
  interface_data_type: '1',
  interface_para_default: '',
  interface_show_flag: '1',
  interface_export_flag: '1',
  interface_para_desc: ''
})

// 表单验证规则
const rules = {
  interface_para_code: [{ required: true, message: '请输入参数编码', trigger: 'blur' }],
  interface_para_name: [{ required: true, message: '请输入参数名称', trigger: 'blur' }],
  interface_para_position: [{ required: true, message: '请输入参数位置', trigger: 'blur' }],
  interface_para_type: [{ required: true, message: '请选择参数类型', trigger: 'change' }],
  interface_data_type: [{ required: true, message: '请选择数据类型', trigger: 'change' }]
}

// 数据类型选项
const dataTypeOptions = [
  { value: '1', label: '字符' },
  { value: '2', label: '整数' },
  { value: '3', label: '小数' },
  { value: '4', label: '百分比' },
  { value: '5', label: '无格式整数' },
  { value: '6', label: '无格式小数' },
  { value: '7', label: '无格式百分比' },
  { value: '8', label: '1位百分比' },
  { value: '9', label: '1位小数' },
  { value: '10', label: '年份' },
  { value: '11', label: '日期' },
  { value: '12', label: '月份' },
  { value: '13', label: '单选' },
  { value: '14', label: '多选' },
  { value: '15', label: '文本' }
]

// 获取数据类型名称
const getDataTypeName = (type) => {
  const option = dataTypeOptions.find(item => item.value === type)
  return option ? option.label : type
}

// 获取接口信息
const getInterfaceInfo = async () => {
    let interfaceId = router.currentRoute.value.params.id
    getInterfaceDetail(interfaceId).then(res => {
        interfaceInfo.value = res.data
  }).catch(error => {
    ElMessage.error('获取接口详情失败')
  })
}

const sortTableData = (dataList) => {
        const inputType = dataList.filter(item => item.interface_para_type === '输入参数').sort((a, b) => a.interface_para_position - b.interface_para_position)
        const outputType = dataList.filter(item => item.interface_para_type === '输出参数').sort((a, b) => a.interface_para_position - b.interface_para_position)
        tableData.value = [...inputType, ...outputType]
}

// 获取字段列表
const getFieldList = async () => {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      interface: router.currentRoute.value.params.id
    }

    await getInterfaceFields(params).then(res => {
        const tempData = res.data
        if (tempData) {
            sortTableData(tempData)
        }
        total.value = res.total

    }).catch(error => {
        ElMessage.error('获取接口字段失败')
    }).finally(() => {
        loading.value = false
    })
}

const goInterfaceList = () => {
    router.push({
        path: '/reportinfo/interface'
    })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.assign(formData, {
    interface_para_code: '',
    interface_para_name: '',
    interface_para_position: 1,
    interface_para_type: '2',
    interface_data_type: '1',
    interface_para_default: '',
    interface_show_flag: '1',
    interface_export_flag: '1',
    interface_para_desc: ''
  })
}

// 新增字段
const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 编辑字段
const handleEdit = (row) => {
  dialogType.value = 'edit'
  Object.assign(formData, row)
  dialogVisible.value = true
}

// 删除字段
const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确认删除该字段吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        await request.delete(`/api/report/interface-fields/${row.id}/`)
        ElMessage.success('删除成功')
        getFieldList()
      } catch (error) {
        console.error('删除字段失败：', error)
        ElMessage.error('删除字段失败')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

// 追加字段
const handleAppend = (row) => {

    const fileInfo = {
        interface_para_code: '',
        interface_para_name: '',
        interface_para_position: row.interface_para_position + 1,
        interface_para_type: '2',
        interface_data_type: '1',
        interface_para_default: '',
        interface_show_flag: '1',
        interface_export_flag: '1',
        interface_para_desc: ''
    }
    tableData.value.splice(row.interface_para_position + 1, 0, fileInfo)
    // 将新增的字段插入到tableData.value中
    // sortTableData(newTableData)
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const data = { ...formData, interface: interfaceId }
        if (dialogType.value === 'add') {
          await request.post('/api/report/interface-fields/', data)
          ElMessage.success('添加成功')
        } else {
          await request.put(`/api/report/interface-fields/${data.id}/`, data)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        getFieldList()
      } catch (error) {
        console.error('保存字段失败：', error)
        ElMessage.error('保存字段失败')
      }
    }
  })
}

// 分页大小变更处理
const handleSizeChange = (val) => {
  pageSize.value = val
  getFieldList()
}

// 当前页变更处理
const handleCurrentChange = (val) => {
  currentPage.value = val
  getFieldList()
}

// 页面加载时获取数据
onMounted(() => {
  getInterfaceInfo()
  getFieldList()
})
</script>

<style scoped>
.interface-fields {
  padding: 20px;
}

.card-header {
  display: flex;
  /* justify-content: space-between; */
  align-items: center;
  margin-bottom: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>