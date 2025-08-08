<template>
  <div class="data-sync-container">
    <div class="sync-header">
      <h1>数据同步配置</h1>
      <p>配置源数据库、目标数据库及同步规则，实现数据的高效同步</p>
    </div>

    <el-steps :active="activeStep" class="sync-steps" finish-status="success">
      <el-step title="源数据库配置"></el-step>
      <el-step title="选择同步表和字段"></el-step>
      <el-step title="目标数据库配置"></el-step>
      <el-step title="同步方式设置"></el-step>
      <el-step title="确认并执行"></el-step>
    </el-steps>

    <div class="sync-content">
      <!-- 步骤1：源数据库配置 -->
      <template v-if="activeStep === 0">
        <database-config 
          title="源数据库信息" 
          :databases="databases"
          :selected-db="sourceDb"
          @save="handleSourceDbSave"
        />
      </template>

      <!-- 步骤2：选择同步表和字段 -->
      <template v-if="activeStep === 1 && sourceDb">
        <table-field-selector
          :database-id="sourceDb.id"
          :selected-tables="selectedTables"
          @update:selected-tables="selectedTables = $event"
        />
      </template>

      <!-- 步骤3：目标数据库配置 -->
      <template v-if="activeStep === 2 && selectedTables.length > 0">
        <database-config 
          title="目标数据库信息" 
          :databases="databases"
          :selected-db="targetDb"
          :exclude-id="sourceDb?.id"
          @save="handleTargetDbSave"
        />
      </template>

      <!-- 步骤4：同步方式设置 -->
      <template v-if="activeStep === 3 && targetDb">
        <sync-method-config
          :sync-method="syncMethod"
          :increment-field-options="getIncrementFieldOptions()"
          @update:sync-method="syncMethod = $event"
        />
      </template>

      <!-- 步骤5：确认并执行 -->
      <template v-if="activeStep === 4">
        <sync-confirmation
          :source-db="sourceDb"
          :target-db="targetDb"
          :selected-tables="selectedTables"
          :sync-method="syncMethod"
          @confirm="executeSync"
        />
      </template>
    </div>

    <div class="sync-actions">
      <el-button 
        @click="prevStep" 
        :disabled="activeStep === 0"
        class="prev-btn"
      >
        上一步
      </el-button>
      
      <el-button 
        type="primary" 
        @click="nextStep" 
        :disabled="!canProceed"
        class="next-btn"
      >
        {{ activeStep === 4 ? '执行同步' : '下一步' }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DatabaseConfig from './components/DatabaseConfig.vue';
import TableFieldSelector from './components/TableFieldSelector.vue';
import SyncMethodConfig from './components/SyncMethodConfig.vue';
import SyncConfirmation from './components/SyncConfirmation.vue';

import { getDataSourceList } from '@/api/dataassets/datasource'

// 数据库类型选项
const dbTypes = [
  { label: 'MySQL', value: 'mysql' },
  { label: 'PostgreSQL', value: 'postgresql' },
  { label: 'Oracle', value: 'oracle' },
  { label: 'SQL Server', value: 'sqlserver' },
  { label: 'MongoDB', value: 'mongodb' }
];

// 模拟数据库列表
const databases = ref([]);

// 状态管理
const activeStep = ref(0);
const sourceDb = ref(null);
const targetDb = ref(null);
const selectedTables = ref([]);
const syncMethod = ref({
  type: 'full', // full: 全量, increment: 增量
  incrementField: '',
  syncFrequency: 'manual' // manual: 手动, daily: 每日, weekly: 每周
});

// 获取数据源
const fetchDataSource = async () => {
  getDataSourceList().then(res => {
    databases.value = res.data
  }).catch(err => {

  })
};

// 处理源数据库保存
const handleSourceDbSave = (dbConfig) => {
  sourceDb.value = dbConfig;
};

// 处理目标数据库保存
const handleTargetDbSave = (dbConfig) => {
  targetDb.value = dbConfig;
};

// 获取增量字段选项
const getIncrementFieldOptions = () => {
  if (selectedTables.length === 0) return [];
  
  // 这里简化处理，实际应根据选中的表获取共同的时间字段
  return [
    { label: '创建时间 (create_time)', value: 'create_time' },
    { label: '更新时间 (update_time)', value: 'update_time' },
    { label: '时间戳 (timestamp)', value: 'timestamp' }
  ];
};

// 检查当前步骤是否可以继续
const canProceed = computed(() => {
  switch (activeStep.value) {
    case 0:
      return sourceDb.value != null
      // return !!sourceDb.value;
    case 1:
      return selectedTables.value.length > 0;
    case 2:
      return !targetDb.value;
    case 3:
      // 增量同步需要选择增量字段
      return syncMethod.value.type === 'full' || 
             (syncMethod.value.type === 'increment' && syncMethod.value.incrementField);
    case 4:
      return true;
    default:
      return false;
  }
});

// 下一步
const nextStep = () => {
  if (activeStep.value < 4) {
    activeStep.value++;
  }
};

// 上一步
const prevStep = () => {
  if (activeStep.value > 0) {
    activeStep.value--;
  }
};

// 执行同步
const executeSync = () => {
  // 模拟执行同步操作
  console.log('开始执行数据同步:', {
    sourceDb: sourceDb.value,
    targetDb: targetDb.value,
    selectedTables: selectedTables.value,
    syncMethod: syncMethod.value
  });
  
  // 显示成功消息，实际项目中可以跳转到同步任务列表或结果页面
  alert('数据同步任务已启动！');
};


fetchDataSource();
</script>

<style scoped>
.data-sync-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.sync-header {
  text-align: center;
  margin-bottom: 30px;
}

.sync-header h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.sync-header p {
  color: #666;
  font-size: 14px;
}

.sync-steps {
  margin-bottom: 40px;
}

.sync-content {
  min-height: 400px;
  padding: 20px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  margin-bottom: 30px;
}

.sync-actions {
  display: flex;
  justify-content: space-between;
}

.prev-btn {
  width: 120px;
}

.next-btn {
  width: 120px;
}
</style>
