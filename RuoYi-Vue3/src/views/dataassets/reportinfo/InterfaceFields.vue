<template>
    <div class="app-container">

        <query-params-form :properties="queryProperties" @query="getFieldList" @reset="getFieldList" />

        <crud-bar addBtn @addEvent="handleAdd" />
        <!-- 数据表格 -->
        <el-table :data="paginateData" style="width: 100%" v-loading="loading" border fit>
            <el-table-column prop="interface_para_code" label="参数编码" :width="interfaceParaCodeWidth" />
            <el-table-column prop="interface_para_name" label="参数名称" width="200" />
            <el-table-column prop="interface_para_position" label="参数位置" width="100" />
            <el-table-column prop="interface_para_type" label="参数类型" width="100">
                <template #default="scope">
                    <!-- {{ scope.row.interface_para_type }} -->
                    {{ interfaceParaTypeOptions.filter(item => item.value === scope.row.interface_para_type)[0].label }}
                </template>
            </el-table-column>
            <el-table-column prop="interface_data_type" label="数据类型" width="100">
                <template #default="scope">
                    {{ getDataTypeName(scope.row.interface_data_type) }}
                </template>
            </el-table-column>
            <el-table-column prop="interface_para_default" label="默认值" width="100" show-overflow-tooltip />
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
                    <el-button link type="primary" icon="Edit" @click="handleEdit(scope.row)"
                        v-hasPermi="['report:interface-field:update']"></el-button>
                    <el-button link type="primary" icon="Plus" @click="handleAppend(scope.row)"
                        v-hasPermi="['report:interface-field:add']"></el-button>
                    <el-button link type="danger" icon="Delete" @click="handleDelete(scope.row)"
                        v-hasPermi="['report:interface-field:remove']"></el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-row>
            <el-col :span="24" style="margin-top: 10px;">
                <el-button type="primary" @click="showSqlEditor">接口开发</el-button>
                <el-button type="primary" @click="showSqlEditor">保存信息</el-button>
            </el-col>
        </el-row>

        <!-- 分页 -->
        <pagination v-show="paginatedTotal > 0" :total="paginatedTotal" v-model:page="currentPage" v-model:limit="pageSize" />

        <!-- 字段编辑对话框 -->
        <el-dialog v-model="dialogVisible" 
        :title="dialogType === 'add' ? '新增字段' : '编辑字段'" 
        width="50%">
            <el-form ref="formRef" :model="formData" :rules="rules" label-width="120px">
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
                        <el-option v-for="item in interfaceParaTypeOptions" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="数据类型" prop="interface_data_type">
                    <el-select v-model="formData.interface_data_type">
                        <el-option v-for="item in dataTypeOptions" :key="item.value" :label="item.label"
                            :value="item.value" />
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
                    <el-input v-model="formData.interface_para_desc" type="textarea" />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleSubmit">确定</el-button>
                </div>
            </template>
        </el-dialog>

        <!-- SQL编辑器对话框 -->
        <el-dialog v-model="sqlEditorVisible" 
        title="接口SQL开发" fullscreen 
        :destroy-on-close="true" 
        :show-close="true"
            class="sql-editor-dialog" :close-on-click-modal="false">
            <InterfaceSqlEditor :initial-sql="interfaceInfo?.interface_sql || ''" :interface-info="interfaceInfo"
                @execute="handleExecuteSql" @save="handleSaveSql" @close="sqlEditorVisible = false" />
        </el-dialog>
    </div>
</template>

<script>

export default {
    // 路由监听
    // 修改路由元信息，这样就可以使得复用同一个组件时，元信息是不同的，可以区分部分动态路由
    beforeRouteEnter(to, from, next) {
        if (to.query.interface_name) {
            const title = to.meta.title
            to.meta.title = title + '-' + to.query.interface_name
            to.meta.activeMenu = '/report/interface/interfaceManage'
        }
        next()
    },
}

</script>

<script setup name="InterfaceFields">
import { ref, onMounted, reactive, computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import QueryParamsForm from '@/components/QueryParamsForm'
import CrudBar from '@/components/CrudBar'
import InterfaceSqlEditor from './components/InterfaceSqlEditor.vue'
import {
    getInterfaceDetail,
    getInterfaceFields,
    createInterfaceField,
    updateInterfaceField,
    deleteInterfaceField,
    updateInterface
} from '@/api/dataassets/reportinfo'

import { executeQuery } from '@/api/dataassets/datasource'

const queryProperties = reactive([
    { label: '字段名称', type: 'input', prop: 'interface_para_name' },
    { label: '字段编码', type: 'input', prop: 'interface_para_code' }
])

const router = useRouter()

const interfaceId = ref(null)
// 接口信息
const interfaceInfo = ref(null)

// 表格数据
const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

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

// 字段类型选项
const interfaceParaTypeOptions = [
    { value: '1', label: '输入参数' },
    { value: '2', label: '输出参数' }
]

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

const calculateColumnWidth = inject('calculateColumnWidth')

const interfaceParaCodeWidth = computed(() => {
    let maxWidth = 200
    if (paginateData.length === 0) return maxWidth

    paginateData.value.forEach(item => {
        const width = calculateColumnWidth(item.interface_para_code)
        maxWidth = Math.max(maxWidth, width)
    })

    return maxWidth
})

// 获取数据类型名称
const getDataTypeName = (type) => {
    const option = dataTypeOptions.find(item => item.value === type)
    return option ? option.label : type
}

// 获取接口信息
const getInterfaceInfo = async () => {
    interfaceId.value = router.currentRoute.value.params.id
    getInterfaceDetail(interfaceId.value).then(res => {
        interfaceInfo.value = res.data
    }).catch(error => {
        ElMessage.error('获取接口详情失败')
    })
}

// 接口字段对象
const interfaceFields = reactive({
    inputFields: [],
    outputFields: []
})
// 获取字段列表
const getFieldList = async (queryParams) => {
    loading.value = true
    const params = {
        noPage: 1,
        interface: interfaceId.value,
        ...queryParams
    }

    await getInterfaceFields(params).then(res => {
        const tempData = res.data || []
        if (tempData) {
            // sortTableData(tempData)
            interfaceFields.inputFields = tempData.filter(item => item.interface_para_type === '1').sort((a, b) => a.interface_para_position - b.interface_para_position)
            interfaceFields.outputFields = tempData.filter(item => item.interface_para_type === '2').sort((a, b) => a.interface_para_position - b.interface_para_position)
        }
        tableData.value = [...interfaceFields.inputFields, ...interfaceFields.outputFields]

    }).catch(error => {
        ElMessage.error('获取接口字段失败')
    }).finally(() => {
        loading.value = false
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
            deleteInterfaceField(row.id).then(res => {
                ElMessage.success('删除成功')
                getFieldList()
            }).catch(error => {
                ElMessage.error('删除字段失败')
            })
        })
        .catch(() => {
            ElMessage.info('已取消删除')
        })
}

// 追加字段
const handleAppend = (row) => {
    dialogType.value = 'add'
    resetForm()

    // 预设新字段的位置为当前选中字段的后一位
    formData.interface_para_position = row.interface_para_position + 1
    // 继承当前字段的参数类型
    formData.interface_para_type = row.interface_para_type

    // 打开对话框让用户填写其他信息
    dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
    if (!formRef.value) return

    await formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const data = { ...formData, interface: interfaceId.value }
                if (dialogType.value === 'add') {
                    await createInterfaceField(data).then(res => {
                        ElMessage.success('添加成功')
                    }).catch(error => {
                        ElMessage.error('添加字段失败' + error)
                    })
                } else {
                    await updateInterfaceField(data.id, data).then(res => {
                        ElMessage.success('更新成功')
                    }).catch(error => {
                        ElMessage.error('更新字段失败' + error)
                    })
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

// 分页数据
const paginateData = computed(() => {
    const startIndex = (currentPage.value - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value
    return tableData.value.slice(startIndex, endIndex)
})

// 分页数据总数
const paginatedTotal = computed(() => tableData.value.length)

// SQL编辑器相关
const sqlEditorVisible = ref(false)

// 显示SQL编辑器
const showSqlEditor = () => {
    sqlEditorVisible.value = true
}

// 处理SQL执行
const handleExecuteSql = async ({ sql, interfaceId }, callback) => {
    const datasourceId = interfaceInfo.value.interface_datasource

    // 3. 执行查询
    const result = await executeQuery(datasourceId, sql).then(res => {
        return res
    }).catch(error => {
        console.error('执行SQL失败：', error)
        ElMessage.error('执行SQL失败：' + (error.message || ''))
        return { error: error.message || '执行SQL失败' }
    })
    // console.log('execute result', result)
    // 回调函数，将结果返回给子组件中
    callback(result)

    // 获取返回的字段名称
    if (result && result.data && result.data.length > 0) {
        const fieldNames = Object.keys(result.data[0])
        let position = interfaceFields.outputFields.length + 1
        let start = tableData.length
        const newFields = []
        fieldNames.forEach(fieldName => {
            const newField = {
                    interface_para_code: fieldName,
                    interface_para_name: '',
                    interface_para_position: position,
                    interface_para_type: '2',
                    interface_data_type: '1',
                    interface_para_default: '',
                    interface_show_flag: '1',
                    interface_export_flag: '1',
                    interface_para_desc: ''
            }
            position += 1
            newFields.push(newField)
            if(tableData.value.some(item => item.interface_para_code === newField.interface_para_code)) return
            tableData.value.splice(start, 0, newField)
        })
        // tableData.value.splice(start, 0, newFields)
        console.log('add new fileds', tableData.value)
    }
}

// 处理SQL保存
const handleSaveSql = async ({ sql, interfaceId }) => {
    try {
        const payload = Object.assign({}, interfaceInfo.value, { interface_sql: sql })
        console.log('保存SQL：', payload)
        await updateInterface(interfaceId, payload)
        // 更新本地接口信息
        if (interfaceInfo.value) {
            interfaceInfo.value.interface_sql = sql
        }
        return true
    } catch (error) {
        console.error('保存SQL失败：', error)
        ElMessage.error('保存SQL失败：' + (error.message || ''))
        return false
    }
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

/* SQL编辑器对话框样式 */
:deep(.sql-editor-dialog) {
    display: flex;
    flex-direction: column;
}

:deep(.sql-editor-dialog .el-dialog__body) {
    flex: 1;
    padding: 0;
    overflow: hidden;
    height: calc(100vh - 54px);
    /* 减去对话框头部高度 */
}
</style>