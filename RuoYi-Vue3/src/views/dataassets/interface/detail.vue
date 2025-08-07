<template>
    <div class="app-container">
        <el-card style="margin-bottom: 5px;">
            <!-- 接口信息 -->
             <el-row style="padding: 20px;">
                <el-col :span="12" class="item-box">
                    <span class="item-label">接口代码: </span>
                    <span class="item-content">{{ interfaceInfo?.interface_code }}</span>
                </el-col>
                <el-col :span="12" class="item-box">
                    <span class="item-label">接口名称: </span>
                    <span class="item-content">{{ interfaceInfo?.interface_name }}</span>
                </el-col>
                <el-col :span="12" class="item-box">
                    <span class="item-label">接口描述: </span>
                    <span class="item-content">{{ interfaceInfo?.interface_desc }}</span>
                </el-col>
                <el-col :span="12" class="item-box">
                    <span class="item-label">是否登录: </span>
                    <span class="item-content">
                      {{ interfaceInfo?.is_login_visit }}
                    </span>
                </el-col>
             </el-row>
        </el-card>
        <el-card>
            <!-- 字段搜索 -->
            <query-params-form :properties="queryProperties" @query="getFieldList" @reset="getFieldList" />

            <crud-bar addBtn @addEvent="handleAdd" removeBtn @removeEvent="handleMultiDelete" saveBtn @saveEvent="handleMutltiSave"/>

            <!-- 数据表格 -->
            <el-table :data="paginateData" style="width: 100%" v-loading="loading" border fit @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="50" align="center" />

                <el-table-column prop="interface_para_code" label="参数编码" :width="interfaceParaCodeWidth">
                    <template #default="scope">
                        <item-wrapper type="input" v-model:modelValue="scope.row.interface_para_code" placeholder="请输入参数编码" />
                    </template>
                </el-table-column>
                <el-table-column prop="interface_para_name" label="参数名称">
                    <template #default="scope">
                         <item-wrapper type="input" v-model:modelValue="scope.row.interface_para_name"  placeholder="请输入参数名称" />
                    </template>
                </el-table-column>
                <el-table-column prop="interface_para_position" label="参数位置" width="80" align="center">
                    <template #default="scope">
                        <span>{{ scope.row.interface_para_position }}</span>
                        <!-- <item-wrapper type="input-number"  v-model:modelValue="scope.row.interface_para_position" /> -->
                    </template>
                </el-table-column>
                <el-table-column prop="interface_para_type" label="参数类型">
                    <template #default="scope">
                        <!-- <el-select v-model="scope.row.interface_para_type" placeholder="请选择参数类型" style="width: 100%">
                            <el-option v-for="item in interfaceParaTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                        </el-select> -->
                        <item-wrapper 
                        type="select" 
                        :options="interfaceParaTypeOptions" 
                        v-model:modelValue="scope.row.interface_para_type" 
                        placeholder="请输入参数值" >

                        </item-wrapper>
                    </template>
                </el-table-column>
                <el-table-column prop="interface_data_type" label="数据类型" width="100">
                    <template #default="scope">
                        <!-- <el-select v-model="scope.row.interface_data_type">
                            <el-option v-for="item in dataTypeOptions" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select> -->
                        <item-wrapper 
                        type="select" 
                        :options="dataTypeOptions" 
                        v-model:modelValue="scope.row.interface_data_type" 
                        placeholder="请选择" >

                        </item-wrapper>
                    </template>
                </el-table-column>
                <el-table-column prop="interface_para_default" label="默认值" width="100" show-overflow-tooltip />
                <el-table-column prop="interface_show_flag" label="是否显示" width="100">
                    <template #default="scope">
                        <!-- {{ scope.row.interface_show_flag === '1' ? '是' : '否' }} -->
                        <item-wrapper
                        type="select"
                        :options="[{'label':'是', 'value':'1'},{'label':'否', 'value':'0'}]"
                        v-model="scope.row.interface_show_flag"
                        />
                    </template>
                </el-table-column>
                <el-table-column prop="interface_export_flag" label="是否导出" width="100">
                    <template #default="scope">
                        <!-- {{ scope.row.interface_export_flag === '1' ? '是' : '否' }} -->
                        <item-wrapper
                        type="select"
                        :options="[{'label':'是', 'value':'1'},{'label':'否', 'value':'0'}]"
                        v-model="scope.row.interface_export_flag"
                        />
                    </template>
                </el-table-column>
                <!-- <el-table-column prop="interface_para_desc" label="参数描述" /> -->
                <el-table-column label="操作" align="center">
                    <template #default="scope">
                        <el-button
                        link type="primary" @click="handleSaveField(scope.row)">
                            保存
                        </el-button>

                        <!-- <el-button link type="primary" icon="Edit" @click="handleEdit(scope.row)"
                            v-hasPermi="['report:interface-field:update']"></el-button> -->
                        <el-button link type="primary" icon="Plus" @click="handleAppendField(scope.row)"
                            v-hasPermi="['report:interface-field:add']"></el-button>
                        <el-button link type="danger" icon="Delete" @click="handleDeleteField(scope.row)"
                            v-hasPermi="['report:interface-field:remove']"></el-button>
                    </template>
                </el-table-column>
            </el-table>
                    <!-- 分页 -->
            <pagination v-show="paginatedTotal > 0" :total="paginatedTotal" v-model:page="currentPage" v-model:limit="pageSize" />
            <el-col>
                <el-button type="primary" plain @click="refreshFields">刷新顺序</el-button>
                <el-button type="primary" plain @click="saveInterface">更新接口</el-button>
            </el-col>
        </el-card>

        <el-card style="margin-top: 10px;" >
            <el-row>
                <el-col :span="24" style="margin-top: 10px;">
                    <el-button type="primary" plain @click="showSqlEditor">SQL详情</el-button>
                </el-col>
            </el-row>
            <div ref="sqlContentRef" class="sql-content" v-if="sqlEditorVisible">
                <InterfaceSqlEditor :initial-sql="interfaceInfo?.interface_sql || ''" :interface-info="interfaceInfo"
                    @execute="handleExecuteSql" @save="handleSaveSql" @close="sqlEditorVisible = false" />
            </div>
        </el-card>


    </div>
</template>

<script>

export default {
    name: 'InterfaceDetail',
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

<script setup name="InterfaceDetail">
import { ref, reactive, computed, inject, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import QueryParamsForm from '@/components/QueryParamsForm'
import CrudBar from '@/components/CrudBar'
import InterfaceSqlEditor from '../components/InterfaceSqlEditor.vue'
import {
    getInterfaceDetail,
    getInterfaceFields,
    createInterfaceField,
    updateInterfaceField,
    deleteInterfaceField,
    updateInterface
} from '@/api/dataassets/reportinfo'

import { executeQuery } from '@/api/dataassets/datasource'
import ItemWrapper from '../components/ItemWrapper.vue'

const { proxy } = getCurrentInstance()

const { interface_is_paging, interface_is_total, interface_is_date_option, interface_is_login_visit } = proxy.useDict("interface_is_paging", "interface_is_total", "interface_is_date_option", "interface_is_login_visit")

const queryProperties = reactive([
    { label: '字段名称', type: 'input', prop: 'interface_para_name' },
    { label: '字段编码', type: 'input', prop: 'interface_para_code' }
])


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


const router = useRouter()

// 接口信息
const interfaceInfo = ref({})

// 表格数据
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


const selectionItems = ref([])

const handleSelectionChange = (selections) => { 
    selectionItems.value = selections
}

const calculateColumnWidth = inject('calculateColumnWidth')

const interfaceParaCodeWidth = computed(() => {
    let maxWidth = 150
    if (paginateData.length === 0) return maxWidth

    paginateData.value.forEach(item => {
        const width = calculateColumnWidth(item.interface_para_code)
        maxWidth = Math.max(maxWidth, width)
    })

    return maxWidth
})

// 获取接口信息
const getInterfaceInfo = async () => {
    let id = router.currentRoute.value.params.id
    await getInterfaceDetail(id).then(res => {
        interfaceInfo.value = res.data
    }).catch(error => {
        ElMessage.error('获取接口详情失败')
    })

    await getFieldList()
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
        interface: interfaceInfo.value.id,
        ...queryParams
    }

    await getInterfaceFields(params).then(res => {
        const tempData = res.data || []
        if (tempData) {
            // sortTableData(tempData)
            interfaceFields.inputFields = tempData.filter(item => item.interface_para_type === '1').sort((a, b) => a.interface_para_position - b.interface_para_position)
            interfaceFields.outputFields = tempData.filter(item => item.interface_para_type === '2').sort((a, b) => a.interface_para_position - b.interface_para_position)
        }

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



const handleMultiDelete = () => {
    if(selectionItems.value.length > 0){
            const ids = selectionItems.value.map(item => item.id)
            // 将数组转换为逗号分隔的字符串
            const idString = ids.join(',')
            deleteInterfaceField(idString).then(res => { 
                ElMessage.success(res.msg)
                getFieldList()
            })
        } else {
            ElMessage.info('请选择要删除的字段')
        }
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

const handleAppendField = (row) => { 
  const pre_postion = row.interface_para_position
    console.log('add field after ', pre_postion)
    const newField = {
            interface_para_code: '',
            interface_para_name: '',
            interface_para_position: pre_postion + 1,
            interface_para_type: row.interface_para_type,
            interface_data_type: '',
            interface_para_default: '',
            interface_show_flag: '1',
            interface_export_flag: '1',
            new_flag: true
    }
    if (row.interface_para_type === '1') { 
        // 查找插入位置
        let insertIdx = interfaceFields.inputFields.findIndex(item => item === row)
        interfaceFields.inputFields.splice(insertIdx, 0, newField)
    } else if (row.interface_para_type === '2') {
        // 查找插入位置
        let insertIdx = interfaceFields.outputFields.findIndex(item => item === row)
        interfaceFields.outputFields.splice(insertIdx, 0, newField)
    }
}


// 添加查询返回的新字段
const handleSaveField = async (row) => {
    if (row.id===undefined) {
      await createInterfaceField({ interface: interfaceInfo.value.id, ...row }).then(res => { 
            ElMessage.success('新增字段成功')
            row.new_field = false
        }).catch(error => { 
            ElMessage.error(`新增字段失败: ${error?.response.data.msg || '未知错误'}`)
        })
    } else {
        await updateInterfaceField(row.id, row).then(res => { 
            ElMessage.success('更新字段成功')
        }).catch(error => {
            ElMessage.error(`更新字段失败: ${error?.response.data.msg || '未知错误'}`)
        })
    }

}


// 删除字段
const handleDeleteField = (row) => {
    if (row.id === undefined) {
        if (row.interface_para_type === '1') {
            interfaceFields.inputFields=interfaceFields.inputFields.filter(item => item.id !== row.id)
        } else {
            interfaceFields.outputFields=interfaceFields.outputFields.filter(item => item.id !== row.id)
        }
    } else {
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
}

// 提交表单
const handleSubmit = async () => {
    if (!formRef.value) return

    await formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const data = { ...formData, interface: interfaceInfo.value.id }
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
    return [...interfaceFields.inputFields, ...interfaceFields.outputFields].slice(startIndex, endIndex)
})

// 分页数据总数
const paginatedTotal = computed(() => [...interfaceFields.inputFields, ...interfaceFields.outputFields].length)

// SQL编辑器相关
const sqlEditorVisible = ref(false)


const sqlContentRef = ref(null)
// 显示SQL编辑器
const showSqlEditor = () => {
    sqlEditorVisible.value = true
    // 关键：使用nextTick确保DOM已更新后再执行滚动
    nextTick(() => {
        if (sqlContentRef.value) {
        // 滚动到新内容区域
        sqlContentRef.value.scrollIntoView({
            behavior: 'smooth', // 平滑滚动效果
            block: 'start'      // 对齐方式：顶部对齐
        });
        }
    });
}

// 新增字段
const newFields = ref([])

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
        let start = interfaceFields.outputFields.length
        fieldNames.forEach(fieldCode => {
            let fieldName = fieldCode  // 这里可以尝试关联到字段的中文名
            const newField = {
                    interface: interfaceId,
                    interface_para_code: fieldCode,
                    interface_para_name: fieldName,
                    interface_para_position: position,
                    interface_para_type: '2',
                    interface_data_type: '1',
                    interface_para_default: '',
                    interface_show_flag: '1',
                    interface_export_flag: '1',
                    interface_para_desc: '',
                    new_flag: true
            }
            position += 1
            newFields.value.push(newField)
            if (interfaceFields.outputFields.some(item => item.interface_para_code === newField.interface_para_code)) return
            interfaceFields.outputFields.splice(start, 0, newField)
            start += 1
        })
    }
}



const handleMutltiSave = async () => {
  selectionItems.value.forEach(row => {
    handleSaveField(row)
  })
}

// 刷新字段顺序
const refreshFields = () => { 
    // 更新输入字段位置编号
    for (let i = 0; i<interfaceFields.inputFields.length; i++) { 
        interfaceFields.inputFields[i].interface_para_position = i + 1
    }
    // 更新输出字段位置编号
    for (let i = 0; i<interfaceFields.outputFields.length; i++) { 
        interfaceFields.outputFields[i].interface_para_position = i + 1
    }
}

// 处理SQL保存
const handleSaveSql = async ({ sql, interfaceId }) => {
    try {
        const payload = Object.assign({}, interfaceInfo.value, { interface_sql: sql })
        await updateInterface(interfaceId, payload).then(res => { 
            ElMessage.success('保存成功')
            // 更新本地接口信息
            if (interfaceInfo.value) {
                interfaceInfo.value.interface_sql = sql
            }
        })
    } catch (error) {
        ElMessage.error('保存SQL失败：' + (error.message || ''))
    }
}

// 更新接口信息
const saveInterface = async () => { 
    await updateInterface(interfaceInfo.value.id, interfaceInfo.value)

    // 接口字段不与接口信息一起更新
}

// 页面加载时获取数据
// onMounted(() => {
    // getInterfaceInfo()
// })

getInterfaceInfo()
</script>

<style scoped>

.card-header {
    display: flex;
    /* justify-content: space-between; */
    align-items: center;
    margin-bottom: 10px;
}

.item-box {
    margin-bottom: 10px;
}

.item-label {
    margin-right: 5px;
    font-weight: bold;
}

.item-content {
    margin-bottom: 5px;
    padding-left: 5px;
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