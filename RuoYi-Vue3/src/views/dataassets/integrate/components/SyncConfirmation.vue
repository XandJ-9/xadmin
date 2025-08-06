<template>
  <div class="sync-confirmation">
    <h2>同步配置确认</h2>
    
    <el-card class="confirmation-card">
      <div class="section">
        <h3>源数据库信息</h3>
        <div class="info-item">
          <span class="label">数据库名称：</span>
          <span class="value">{{ sourceDb.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">数据库类型：</span>
          <span class="value">{{ getDbTypeName(sourceDb.type) }}</span>
        </div>
        <div class="info-item">
          <span class="label">连接地址：</span>
          <span class="value">{{ sourceDb.host }}:{{ sourceDb.port }}</span>
        </div>
        <div class="info-item">
          <span class="label">数据库名：</span>
          <span class="value">{{ sourceDb.dbName }}</span>
        </div>
      </div>
      
      <div class="section">
        <h3>目标数据库信息</h3>
        <div class="info-item">
          <span class="label">数据库名称：</span>
          <span class="value">{{ targetDb.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">数据库类型：</span>
          <span class="value">{{ getDbTypeName(targetDb.type) }}</span>
        </div>
        <div class="info-item">
          <span class="label">连接地址：</span>
          <span class="value">{{ targetDb.host }}:{{ targetDb.port }}</span>
        </div>
        <div class="info-item">
          <span class="label">数据库名：</span>
          <span class="value">{{ targetDb.dbName }}</span>
        </div>
      </div>
      
      <div class="section">
        <h3>同步表和字段</h3>
        <div v-for="table in selectedTables" :key="table.tableId" class="table-info">
          <div class="table-name">{{ table.tableName }}</div>
          <div class="field-list">
            <span v-for="field in table.fields" :key="field.id" class="field-tag">
              {{ field.name }} ({{ field.type }})
            </span>
          </div>
        </div>
      </div>
      
      <div class="section">
        <h3>同步方式</h3>
        <div class="info-item">
          <span class="label">同步类型：</span>
          <span class="value">{{ syncMethod.type === 'full' ? '全量同步' : '增量同步' }}</span>
        </div>
        
        <div v-if="syncMethod.type === 'full'" class="info-item">
          <span class="label">同步策略：</span>
          <span class="value">
            {{ syncMethod.fullStrategy === 'overwrite' ? '覆盖目标表数据' : 
               syncMethod.fullStrategy === 'append' ? '追加到目标表' : 
               '先清空目标表再插入' }}
          </span>
        </div>
        
        <div v-if="syncMethod.type === 'increment'" class="info-item">
          <span class="label">增量字段：</span>
          <span class="value">{{ syncMethod.incrementField }}</span>
        </div>
        
        <div v-if="syncMethod.type === 'increment'" class="info-item">
          <span class="label">同步频率：</span>
          <span class="value">
            {{ syncMethod.syncFrequency === 'manual' ? '手动触发' : 
               syncMethod.syncFrequency === 'daily' ? '每日同步' : 
               syncMethod.syncFrequency === 'weekly' ? '每周同步' : 
               `自定义 (${syncMethod.cronExpression})` }}
          </span>
        </div>
        
        <div class="info-item">
          <span class="label">数据转换：</span>
          <span class="value">{{ syncMethod.dataTransformation ? '启用' : '禁用' }}</span>
        </div>
        
        <div class="info-item">
          <span class="label">错误处理：</span>
          <span class="value">
            {{ syncMethod.errorHandling === 'ignore' ? '忽略错误继续执行' : 
               syncMethod.errorHandling === 'stop' ? '遇到错误停止执行' : 
               '重试失败的记录' }}
          </span>
        </div>
      </div>
    </el-card>
    
    <div class="sync-warning">
      <i class="el-icon-warning-outline"></i>
      <span>注意：执行数据同步可能会影响目标数据库中的现有数据，请确认配置无误后再执行。</span>
    </div>
    
    <div class="action-buttons">
      <el-button 
        type="primary" 
        size="large"
        @click="handleConfirm"
      >
        <i class="el-icon-check"></i> 确认并执行同步
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  sourceDb: {
    type: Object,
    required: true
  },
  targetDb: {
    type: Object,
    required: true
  },
  selectedTables: {
    type: Array,
    required: true
  },
  syncMethod: {
    type: Object,
    required: true
  }
});

const emit = defineEmits();

// 数据库类型映射
const dbTypes = [
  { label: 'MySQL', value: 'mysql' },
  { label: 'PostgreSQL', value: 'postgresql' },
  { label: 'Oracle', value: 'oracle' },
  { label: 'SQL Server', value: 'sqlserver' },
  { label: 'MongoDB', value: 'mongodb' }
];

// 获取数据库类型名称
const getDbTypeName = (type) => {
  const dbType = dbTypes.find(t => t.value === type);
  return dbType ? dbType.label : type;
};

// 处理确认
const handleConfirm = () => {
  emit('confirm');
};
</script>

<style scoped>
.sync-confirmation {
  padding: 10px 0;
}

.sync-confirmation h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
}

.confirmation-card {
  margin-bottom: 20px;
}

.section {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #f0f0f0;
}

.section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #444;
  display: flex;
  align-items: center;
}

.section h3::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #1890ff;
  margin-right: 8px;
}

.info-item {
  margin-bottom: 10px;
  line-height: 1.8;
}

.label {
  display: inline-block;
  width: 120px;
  color: #666;
  text-align: right;
  margin-right: 15px;
}

.value {
  color: #333;
}

.table-info {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.table-name {
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.field-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.field-tag {
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 12px;
}

.sync-warning {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 4px;
  padding: 12px 15px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  color: #faad14;
}

.sync-warning i {
  margin-right: 8px;
  font-size: 16px;
}

.action-buttons {
  text-align: center;
}
</style>
