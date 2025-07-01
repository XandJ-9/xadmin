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
               :disabled="single"
               @click="handleUpdate"
               v-hasPermi="editPermi"
            >修改</el-button>
         </el-col>
         <el-col :span="1.5" v-if="removeBtn">
            <el-button
               type="danger"
               plain
               icon="Delete"
               :disabled="multiple"
               @click="handleDelete"
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
    multiple: {
        type: Boolean,
        default: true
    },
    single: {
        type: Boolean,
        default: true
    },
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
  }
})

const emit = defineEmits(["addEvent", "updateEvent", "deleteEvent", "exportEvent"])



const handleAdd = () => {
    emit("addEvent")
 }

const handleUpdate = () => { 
    emit('updateEvent')
}

const handleDelete = () => {
    emit('deleteEvent')
 }

const handleExport = () => { 
    emit('exportEvent')
}

</script>