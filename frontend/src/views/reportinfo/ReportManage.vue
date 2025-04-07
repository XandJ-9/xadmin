<template>
  <div class="report-info-container">
    <div class="header-actions">
      <el-button type="primary" @click="handleAdd">新增报表</el-button>
    </div>

    <el-table :data="reportList" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="报表名称" />
      <el-table-column prop="desc" label="描述" />
      <el-table-column prop="module_name" label="所属模块" />
      <el-table-column prop="platform_name" label="所属平台" />
      <el-table-column prop="create_time" label="创建时间" width="180" />
      <el-table-column prop="update_time" label="更新时间" width="180" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
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
        <el-form-item label="所属模块" prop="module">
          <el-select v-model="form.module" placeholder="请选择所属模块">
            <el-option
              v-for="item in moduleOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
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

const reportList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const moduleOptions = ref([])


// 搜索表单数据
const searchForm = reactive({
  platformId: '',
  moduleCode: '',
  moduleName: ''
})
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)


const form = ref({
  name: '',
  desc: '',
  module: ''
})

const rules = {
  name: [{ required: true, message: '请输入报表名称', trigger: 'blur' }],
  module: [{ required: true, message: '请选择所属模块', trigger: 'change' }]
}

const formRef = ref(null)
const currentId = ref(null)

const fetchReportList = async () => {
    try {
      const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      platform_id: searchForm.platformId,
      module_code: searchForm.moduleCode,
      name: searchForm.moduleName
    }
    const response = await request.get('/api/report/reports/',{ params })
    reportList.value = response.data.data.data
  } catch (error) {
    ElMessage.error('获取报表列表失败')
  }
}

const fetchModuleOptions = async () => {
  try {
    const response = await request.get('/api/report/modules/list_all/')
    moduleOptions.value = response.data.data
  } catch (error) {
    ElMessage.error('获取模块列表失败')
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增报表'
  form.value = {
    name: '',
    desc: '',
    module: ''
  }
  currentId.value = null
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑报表'
  form.value = {
    name: row.name,
    desc: row.desc,
    module: row.module
  }
  currentId.value = row.id
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该报表?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await request.delete(`/api/report/reports/${row.id}/`)
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
        if (currentId.value) {
          await request.put(`/api/report/reports/${currentId.value}/`, form.value)
          ElMessage.success('更新成功')
        } else {
          await request.post('/api/report/reports/', form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchReportList()
      } catch (error) {
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

onMounted(() => {
  fetchReportList()
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
</style>