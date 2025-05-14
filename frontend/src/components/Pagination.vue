<template>
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
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
    total: {
        type: Number,
        default: 0
    },
    currentPage: {
        type: Number,
        default: 1
    },
    pageSize: {
        type: Number,
        default: 10
    }
})

const emit = defineEmits(['size-change', 'current-change'])

// 分页大小变更处理
const handleSizeChange = (val) => {
    emit('size-change', val)
}

// 当前页变更处理
const handleCurrentChange = (val) => {
    emit('current-change', val)
}
</script>

<style scoped>
.pagination-container {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}
</style>