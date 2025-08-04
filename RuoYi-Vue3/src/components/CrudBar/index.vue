<template>
    <div class="crud-bar">
        <el-row :gutter="10" class="mb8">
         <el-col :span="1.5" v-if="addBtn">
            <el-button
               type="primary"
               plain
               icon="Plus"
               @click="handleAdd"
               v-hasPermi="addPermi"
            >新增</el-button>
         </el-col>
         <el-col :span="1.5" v-if="editBtn">
            <el-button
               type="success"
               plain
               icon="Edit"
               @click="handleUpdate"
               v-hasPermi="editPermi"
            >修改</el-button>
         </el-col>
         <el-col :span="1.5" v-if="removeBtn">
            <el-button
               type="danger"
               plain
               icon="Delete"
               @click="handleRemove"
               v-hasPermi="removePermi"
            >删除</el-button>
         </el-col>
         <el-col :span="1.5" v-if="exportBtn">
            <el-button
               type="warning"
               plain
               icon="Download"
               @click="handleExport"
               v-hasPermi="exportPermi"
            >导出</el-button>
         </el-col>
         <el-col :span="1.5" v-if="importBtn"> 
            <el-button
               type="info"
               plain
               icon="Upload"
               @click="handleImport"
               v-hasPermi="importPermi"
            >导入</el-button>
         </el-col>
         <el-col :span="1.5" v-if="saveBtn"> 
            <el-button
               type="info"
               plain
               icon="Save"
               @click="handleSave"
               v-hasPermi="savePermi"
            >保存</el-button>
         </el-col>
         <!-- <el-col :span="1.5">
            <el-button
               type="danger"
               plain
               icon="Refresh"
               @click="handleRefreshCache"
               v-hasPermi="['system:dict:remove']"
            >刷新缓存</el-button>
         </el-col> -->
      </el-row>
    </div>
</template>

<script setup>

const props = defineProps({
    addPermi: {
        type: Array,
        default: ['undefined:undefined:undefined']
    },
    editPermi: {
        type: Array,
        default: ['undefined:undefined:undefined']
    },
    removePermi: {
        type: Array,
        default:['undefined:undefined:undefined']
    },
    exportPermi: {
        type: Array,
        default: ['undefined:undefined:undefined']
    },
    importPermi: {
        type: Array,
        default: ['undefined:undefined:undefined']
   },
    savePermi: {
        type: Array,
        default: ['undefined:undefined:undefined']
   },
  addBtn: {
      type: Boolean,
      default: undefined
  },
  editBtn: {
      type: Boolean,
      default: undefined
  },
  removeBtn: {
      type: Boolean,
      default: undefined
  },
  exportBtn: {
      type: Boolean,
      default: undefined
    },
    importBtn: {
        type: Boolean,
        default: undefined
    },
    saveBtn: {
        type: Boolean,
        default: undefined
    },
  
})

const emit = defineEmits(["addEvent", "updateEvent", "removeEvent","importEvent", "exportEvent", "saveEvent"])



const handleAdd = () => {
    emit("addEvent")
 }

const handleUpdate = () => { 
    emit('updateEvent')
}

const handleRemove = () => {
    emit('removeEvent')
 }

const handleExport = () => { 
    emit('exportEvent')
}

const handleImport = () => {
    emit('importEvent')
}

const handleSave = () => { 
    emit('saveEvent')
}

</script>