<template>
    <div class="query-params-container">
      <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
        <el-form-item v-for="(item,index) in properties" :key="index"
          :label="item.label"
          :prop="item.prop">
            <el-input v-if="item.type=='input'" 
            v-model="queryParams[item.prop]" 
            :placeholder="`请输入` + item.label" 
            clearable 
            style="width: 200px" 
            @keyup.enter="handleQuery"/>

            <el-select v-if="item.type=='select'"
             v-model="queryParams[item.prop]" 
             :placeholder="`请选择` + item.label" 
             clearable 
             style="width: 200px">
                <el-option
                v-for="dict in item.options"
                :key="dict.id"
                :label="dict.label"
                :value="dict.value"
                />
            </el-select>

            <el-date-picker v-if="item.type=='dateRange'"
               v-model="queryParams[item.prop]"
               value-format="YYYY-MM-DD"
               type="daterange"
               range-separator="-"
               start-placeholder="开始日期"
               end-placeholder="结束日期"
            ></el-date-picker>

            <el-date-picker v-if="item.type=='date'"
               v-model="queryParams[item.prop]"
               value-format="YYYY-MM-DD"
               type="date"
            ></el-date-picker>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
            <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>

      </el-form>
    </div>

</template>


<script setup>


const emit = defineEmits()
// 传参样例
// const queryProperties = ref([
//     { label: '数据源名称', type: 'input', prop: 'name' },
//     { label: '数据源类型', type: 'select', prop: 'type' , options: [
//         {id:1, label: 'MySQL', value: 'mysql' },
//         {id:2, label: 'PostgreSql', value: 'PostgreSql' },
//     ]}
// ])
const props = defineProps({
    properties: {
        type: Array,
        default: () => []
    }
})


const showSearch = ref(true)

const queryParams = reactive({})

const handleQuery = () => { 
    emit("query", queryParams)
}

const { proxy } = getCurrentInstance()

const resetQuery = () => { 
    // emit("reset")
    proxy.resetForm("queryRef")
    handleQuery()
}

</script>