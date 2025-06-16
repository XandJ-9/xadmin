<template>
    <div id="interface-view-container">
        <el-form class="demo-form-inline" :model="queryForm" label-position="top">
            <el-form-item label="接口编码" style="font-weight: 15px;">
                <el-input v-model="interface_code" placeholder="" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="接口参数" class="param-item">
                <div class="param-header">
                    <span class="param-label">接口参数</span>
                    <el-button link type="primary" @click="showJsonFormat = !showJsonFormat" icon="el-icon-edit">
                        <el-icon :size="20">
                            <Edit />
                        </el-icon>
                        {{ showJsonFormat ? '表格' : 'JSON' }}
                    </el-button>
                </div>
                <el-input v-if="showJsonFormat" v-model="queryForm.query_field_json" placeholder="接口参数"
                    type="textarea" />
                <el-table v-else :data="queryForm.query_field_list" border fit>
                    <el-table-column align="center" label="参数名称" prop="interface_para_name" />
                    <el-table-column align="center" label="参数编码" prop="interface_para_code" />
                    <el-table-column align="center" label="参数数值" value="">
                        <template #default="{ row }">
                            <el-input :placeholder="row.interface_para_code"
                                v-model="queryForm.query_para_value[row.interface_para_code]"></el-input>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
        </el-form>



        <el-button @click="queryData({ env_type: 0 })" type="primary" link size="small">查询测试环境</el-button>
        <!-- <el-button @click="queryData({ env_type: 1 })" type="primary" link size="small">查询生产环境</el-button> -->
        <!-- <el-button @click="exportData({ env_type: 0 })" type="primary" link size="small">测试导出</el-button> -->
        <!-- <el-button @click="exportData({ env_type: 1 })" type="primary" link size="small">生产导出</el-button> -->
        <!-- :label="item.interface_para_name ? item.interface_para_name : item.interface_para_desc"  -->
        <el-table :data="pageInfo.tableData" border highlight-current-row style="width: 100%">
            <el-table-column align="center" v-for="item, index in columnsFields" :key="index"
                :show-overflow-tooltip="true" :min-width="100">
                <template #header>
                    <span>{{ item.interface_para_name }}</span>
                    <el-tooltip class="item" effect="light" placement="top">
                        <el-icon>
                            <InfoFilled />
                        </el-icon>
                        <template #content>
                            {{ item.interface_para_code }}
                        </template>
                    </el-tooltip>
                </template>
                <template #default="{ row }">
                    <span>{{ row[item.interface_para_code] }}</span>
                </template>
            </el-table-column>
        </el-table>

        <el-alert v-show="errorMsg.error" title="查询失败" type="error" :closable="true">
            <template #default>
                <span style="color: red;">{{ errorMsg.msg }}</span>
            </template>
        </el-alert>
        <div class="card-footer">
            <Pagination
                :total="pageInfo.total"
                :current-page="pageInfo.page_no"
                :page-size="pageInfo.page_size"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>

    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '@/utils/request'
// import { XLSX } from 'xlsx'
import Pagination from '@/components/Pagination'

const props = defineProps({
    interface_id: { type: Number, default: 0 },
    interface_name: { type: String, default: '' },
})

const interface_code = ref(null)
const queryFields = ref([])
const columnsFields = ref([])


const resDataList = ref([])
const totalresDataList = ref([])

const visiable = ref(false)
const showJsonFormat = ref(false)

const queryForm = reactive({
    query_field_json: '',
    query_field_list: [],
    query_para_value: {}
})

onMounted(() => {
    getInterfaceInfo()
})
const getInterfaceInfo = async () => {
    const res = await request.get(`/api/report/interfaces/${props.interface_id}/`)
    interface_code.value = res.data.data.interface_code
    const resp = await request.get(`/api/report/interface-fields/?interface=${props.interface_id}&noPage=1`)
    const fields = resp.data.data
    if (!fields) {
        return
    }
    queryFields.value = fields.filter(e => e.interface_para_type == '输入参数')
    columnsFields.value = fields.filter(e => e.interface_para_type == '输出参数')
    queryForm.query_field_list = queryFields

    queryFields.value.forEach((item) => {
        if (item.interface_para_type == '输入参数') {
            queryForm.query_para_value[item.interface_para_code] = ''
        }
    })
    queryForm.query_field_json = JSON.stringify(queryForm.query_para_value, null, 2)
    
}

// const getReportData = async ({ interface_code, payload, env_type }) => {
//     request.post(`/api/report/execute-query/?interface_code=${interface_code}`, data).then(response => {})
// }

const queryLoading = ref(false)
const downloadLoading = ref(false)
const exportOptions = ref({
    filename: 'test.xlsx',
    autoWidth: true,
    bookType: 'xlsx'
})

const pageInfo = reactive({
    env_type: 0,
    page_no: 1,
    page_size: 10,
    total: 0,
    tableData: []
})

const errorMsg = ref({
    error: false,
    msg: ''
})
const queryData = (data) => {
    reset()
    // 只拷贝数值，不修改被引用的对象值
    let payload = showJsonFormat ? JSON.parse(queryForm.query_field_json) : { ...queryForm.query_para_value }
    // console.log(this.showJsonFormat, payload)
    payload = Object.assign(payload, {
        "export_type": "1",
        "operate_type": "1",
        "page_no": pageInfo.page_no,
        "page_size": pageInfo.page_size
    })
    queryLoading.value = true

    //   getReportData({ interface_code, payload, env_type: data.env_type }).then(response => {
    request.post(`/api/report/execute-query/?interface_code=${interface_code.value}`, payload).then(response => {
        const res = response.data
        try {
            if (res.code == '-1') {
                errorMsg.value.error = true
                errorMsg.value.msg = res.message
            } else {
                //   const property = res.property
                //   let columns = this.sortColumns(property);
                //   this.columns = Object.assign({}, columns);
                if (res.isPaging == '1') {
                    resDataList.value = res.data.list
                    pageInfo.total = res.data.total
                    if (res.isTotal == '1') {
                        totalresDataList.value = res.data.totalList
                    }
                } else {
                    resDataList.value = res.data
                    pageInfo.total = resDataList.value.length
                    if (res.isTotal == '1') {
                        totalresDataList.value = res.totaldata
                    }
                }
                prepareTableData(resDataList.value);
                visiable.value = true
            }
            queryLoading.value = false
            pageInfo.env_type = data.env_type
        } catch (e) {
            errorMsg.error = true
            errorMsg.msg = "接口返回数据失败" + e
        } finally {
            queryLoading.value = false
        }
    }
    ).finally(() => {
        queryLoading.value = false
    })
}

const prepareTableData = (data) => {
    if (data.length > pageInfo.page_size) {
        pageInfo.tableData = data.slice((pageInfo.page_no - 1) * pageInfo.page_size, pageInfo.page_no * pageInfo.page_size);
    } else {
        pageInfo.tableData = resDataList;
    }

    // 将合计行追加到最后一行
    if (totalresDataList.length > 0) {
        pageInfo.tableData = pageInfo.tableData.concat(totalresDataList);
    }
}
const sortColumns = (columns, flag = 1) => {
    return Object.entries(columns).filter(column => {
        if (flag == '1') {
            // 可查询
            return column[1].showFlag == '1'
        } else {
            // 导出
            return column[1].exportFlag == '1'
        }
    }).sort(([k1, v1], [k2, v2]) => {
        return v1.position - v2.position
    }).map(o => o[1])
}

const reset = () => {
    errorMsg.value.error = false;
    visiable.value = false;
}
const nextPage = () => {
    if (resDataList.length > pageInfo.page_size) {
        pageInfo.tableData = resDataList.slice((pageInfo.page_no - 1) * pageInfo.page_size, pageInfo.page_no * pageInfo.page_size)
        pageInfo.tableData = pageInfo.tableData.concat(totalresDataList)
    } else {
        queryData({ env_type: pageInfo.env_type })
    }
}

const handleSizeChange = (val) => {
    pageInfo.page_size = val
    nextPage()
}

const handleCurrentChange = (val) => {
    pageInfo.page_no = val
    nextPage()
}

</script>

<style>
.table-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
}

.param-item .el-form-item__label {
    display: none;
}

.param-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

</style>