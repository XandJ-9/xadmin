<template>
  <div id="interface-test-container">
    <el-form class="demo-form-inline" :model="queryForm">
            <el-form-item label="接口编码">
                <el-input v-model="queryForm.code" placeholder="接口代码" :disabled="!codeEditable"></el-input>
            </el-form-item>
            <el-form-item label="接口参数">
                <el-button type="text" icon="el-icon-edit"
                    @click="showJsonFormat = !showJsonFormat">{{ showJsonFormat ? '表格' : 'JSON' }}</el-button>
                <el-input v-model="queryForm.query_field_json" placeholder="接口参数" type="textarea" v-if="showJsonFormat"
                    :rows="textareaRows"></el-input>
                <el-table v-else :data="queryForm.query_field_list" border fit highlight-current-row>
                    <el-table-column align="center" label="参数名称" value="">
                        <template slot-scope="{row}">
                            <span>{{ row.interface_para_name }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column align="center" label="参数编码" value="">
                        <template slot-scope="{row}">
                            <span>{{ row.interface_para_code }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column align="center" label="参数数值" value="">
                        <template slot-scope="{row}">
                            <!-- todo： 修改为行内编辑的样式  -->
                            <el-input :placeholder="row.interface_para_code"
                                v-model="queryForm.query_para_value[row.interface_para_code]"></el-input>
                        </template>
                    </el-table-column>
                </el-table>
            </el-form-item>
        </el-form>


        <el-button @click="queryData({ env_type: 0 })" type="text" size="small">查询测试环境</el-button>
        <el-button @click="queryData({ env_type: 1 })" type="text" size="small">查询生产环境</el-button>
        <el-button @click="exportData({ env_type: 0 })" type="text" size="small">测试导出</el-button>
        <el-button @click="exportData({ env_type: 1 })" type="text" size="small">生产导出</el-button>

        <div v-loading="queryLoading || downloadLoading">
            <!-- 
            <el-alert v-if="this.page.total > 0" :title="`共有${this.page.total}条数据`" type="success" show-icon center
                close-text="关闭" :closable="true"></el-alert>
            -->
            <el-alert v-if="errorMsg.error" :title="errorMsg.msg" type="error" show-icon center close-text="关闭"
                :closable="true"></el-alert>

            <el-table v-show="visiable" :data="page.tableData" border highlight-current-row style="width: 100%">
                <el-table-column align="center" v-for="item,index in columns" :key="index"
                    :label="item.paraDesc ? item.paraDesc : item.paraName" :show-overflow-tooltip="true" :min-width="100"
                    >
                    <template slot="header">
                        <span>{{ item.paraName }}</span>
                        <el-tooltip class="item" effect="light"  placement="top">
                            <i class="el-icon-question" style="font-size: 14px; vertical-align: middle;"></i>
                            <div slot="content">
                                {{ item.paraCode }}
                            </div>
                        </el-tooltip>
                    </template>
                    <template slot-scope="{row}">
                        <span>{{ row[item.paraCode] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <pagination v-show="page.total > 0" :total="page.total" :page.sync="page.page_no"
                :limit.sync="page.page_size" @pagination="nextPage()" />

        </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
const props = defineProps({
    interface_id: { type: Number, default: 0 },
    interface_code: { type: String, default: '' },
    interface_name: { type: String, default: '' },
})
</script>

<style>

</style>