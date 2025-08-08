<template>
  <div class="table-field-selector">
    <div class="table-selector">
      <h3>选择要同步的表</h3>
      <el-tree
        :data="tableList"
        show-checkbox
        node-key="id"
        ref="tableTree"
        :check-strictly="false"
        :default-checked-keys="selectedTableIds"
        @check="handleTableCheck"
        class="table-tree"
      />
    </div>

    <div class="field-selector" v-if="selectedTableIds.length > 0">
      <h3>选择字段</h3>
      <el-tabs v-model="activeTableTab" type="border-card">
        <el-tab-pane 
          v-for="tableId in selectedTableIds" 
          :key="tableId"
          :label="getTableName(tableId)"
        >
          <el-checkbox-group
            v-model="selectedFields[tableId]"
            class="field-checkbox-group"
          >
            <el-checkbox
              v-for="field in getTableFields(tableId)"
              :key="field.id"
              :label="field.id"
              class="field-checkbox"
            >
              <span class="field-name">{{ field.name }}</span>
              <span class="field-type">{{ field.type }}</span>
            </el-checkbox>
          </el-checkbox-group>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  databaseId: {
    type: Number,
    required: true
  },
  selectedTables: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits();

// 模拟表数据 - 实际项目中应从API获取
const tableList = ref([
  {
    id: 't1',
    label: 'users',
    children: []
  },
  {
    id: 't2',
    label: 'orders',
    children: []
  },
  {
    id: 't3',
    label: 'products',
    children: []
  },
  {
    id: 't4',
    label: 'categories',
    children: []
  }
]);

// 模拟字段数据 - 实际项目中应从API获取
const tableFields = ref({
  't1': [
    { id: 't1-f1', name: 'id', type: 'int' },
    { id: 't1-f2', name: 'username', type: 'varchar' },
    { id: 't1-f3', name: 'email', type: 'varchar' },
    { id: 't1-f4', name: 'create_time', type: 'datetime' },
    { id: 't1-f5', name: 'status', type: 'tinyint' }
  ],
  't2': [
    { id: 't2-f1', name: 'id', type: 'int' },
    { id: 't2-f2', name: 'user_id', type: 'int' },
    { id: 't2-f3', name: 'amount', type: 'decimal' },
    { id: 't2-f4', name: 'order_time', type: 'datetime' },
    { id: 't2-f5', name: 'status', type: 'tinyint' }
  ],
  't3': [
    { id: 't3-f1', name: 'id', type: 'int' },
    { id: 't3-f2', name: 'name', type: 'varchar' },
    { id: 't3-f3', name: 'price', type: 'decimal' },
    { id: 't3-f4', name: 'stock', type: 'int' },
    { id: 't3-f5', name: 'category_id', type: 'int' }
  ],
  't4': [
    { id: 't4-f1', name: 'id', type: 'int' },
    { id: 't4-f2', name: 'name', type: 'varchar' },
    { id: 't4-f3', name: 'parent_id', type: 'int' },
    { id: 't4-f4', name: 'sort_order', type: 'int' }
  ]
});

// 状态管理
const tableTree = ref(null);
const selectedTableIds = ref([]);
const activeTableTab = ref('');
const selectedFields = ref({});

// 初始化选中的表和字段
const initSelectedData = () => {
  // 从props初始化选中的表
  selectedTableIds.value = props.selectedTables.map(item => item.tableId);
  
  // 初始化选中的字段
  props.selectedTables.forEach(item => {
    selectedFields.value[item.tableId] = item.fieldIds || [];
  });
  
  // 设置默认激活的标签页
  if (selectedTableIds.value.length > 0) {
    activeTableTab.value = selectedTableIds.value[0];
  }
};

// 获取表名
const getTableName = (tableId) => {
  const table = tableList.value.find(t => t.id === tableId);
  return table ? table.label : tableId;
};

// 获取表的字段列表
const getTableFields = (tableId) => {
  return tableFields.value[tableId] || [];
};

// 处理表选择变化
const handleTableCheck = (checkedNodes, checkedKeys) => {
  selectedTableIds.value = checkedKeys;
  
  // 为新选中的表初始化字段选择
  checkedKeys.forEach(tableId => {
    if (!selectedFields.value[tableId]) {
      // 默认选中所有字段
      selectedFields.value[tableId] = getTableFields(tableId).map(field => field.id);
    }
  });
  
  // 设置默认激活的标签页
  if (checkedKeys.length > 0 && !activeTableTab.value) {
    activeTableTab.value = checkedKeys[0];
  }
  
  // 更新选中的表和字段
  updateSelectedTables();
};

// 监听字段选择变化
watch(
  selectedFields,
  () => {
    updateSelectedTables();
  },
  { deep: true }
);

// 更新选中的表和字段
const updateSelectedTables = () => {
  const result = selectedTableIds.value.map(tableId => ({
    tableId,
    tableName: getTableName(tableId),
    fieldIds: selectedFields.value[tableId] || [],
    fields: getTableFields(tableId).filter(field => 
      (selectedFields.value[tableId] || []).includes(field.id)
    )
  }));
  
  emit('update:selected-tables', result);
};

// 初始化
initSelectedData();

// 监听数据库ID变化，重新加载表数据
watch(
  () => props.databaseId,
  () => {
    // 实际项目中应根据数据库ID重新加载表数据
    console.log('加载数据库ID为', props.databaseId, '的表数据');
    initSelectedData();
  }
);

// 监听外部传入的selectedTables变化
watch(
  () => props.selectedTables,
  () => {
    initSelectedData();
  },
  { deep: true }
);
</script>

<style scoped>
.table-field-selector {
  display: flex;
  gap: 20px;
  height: 100%;
}

.table-selector {
  flex: 1;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  padding: 15px;
  max-height: 500px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.table-selector h3, .field-selector h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #333;
  padding-bottom: 5px;
  border-bottom: 1px solid #f0f0f0;
}

.table-tree {
  flex: 1;
  overflow-y: auto;
}

.field-selector {
  flex: 2;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  padding: 15px;
  max-height: 500px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.el-tabs {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.el-tabs__content {
  flex: 1;
  overflow-y: auto;
  padding-top: 15px;
}

.field-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.field-checkbox {
  width: calc(50% - 15px);
  display: flex;
  align-items: center;
}

.field-name {
  margin-left: 5px;
  flex: 1;
}

.field-type {
  font-size: 12px;
  color: #666;
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
}

@media (max-width: 768px) {
  .table-field-selector {
    flex-direction: column;
  }
  
  .field-checkbox {
    width: 100%;
  }
}
</style>
