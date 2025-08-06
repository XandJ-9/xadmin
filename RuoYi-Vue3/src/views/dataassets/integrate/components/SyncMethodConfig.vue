<template>
  <div class="sync-method-config">
    <h2>同步方式设置</h2>
    
    <el-radio-group 
      v-model="syncMethod.type" 
      class="sync-type-group"
      @change="handleSyncTypeChange"
    >
      <el-radio label="full">全量同步</el-radio>
      <el-radio label="increment">增量同步</el-radio>
    </el-radio-group>
    
    <!-- 全量同步选项 -->
    <div v-if="syncMethod.type === 'full'" class="sync-option-panel">
      <el-form-item label="同步策略">
        <el-select v-model="syncMethod.fullStrategy" placeholder="请选择同步策略">
          <el-option label="覆盖目标表数据" value="overwrite" />
          <el-option label="追加到目标表" value="append" />
          <el-option label="先清空目标表再插入" value="truncate_insert" />
        </el-select>
      </el-form-item>
    </div>
    
    <!-- 增量同步选项 -->
    <div v-if="syncMethod.type === 'increment'" class="sync-option-panel">
      <el-form-item label="增量字段" prop="incrementField">
        <el-select 
          v-model="syncMethod.incrementField" 
          placeholder="请选择增量字段"
        >
          <el-option
            v-for="option in incrementFieldOptions"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </el-select>
        <div class="help-text">
          用于判断数据是否需要同步的字段，通常为时间戳或自增ID
        </div>
      </el-form-item>
      
      <el-form-item label="同步频率">
        <el-radio-group v-model="syncMethod.syncFrequency">
          <el-radio label="manual">手动触发</el-radio>
          <el-radio label="daily">每日同步</el-radio>
          <el-radio label="weekly">每周同步</el-radio>
          <el-radio label="custom">自定义 cron 表达式</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item 
        label="cron 表达式" 
        v-if="syncMethod.syncFrequency === 'custom'"
      >
        <el-input 
          v-model="syncMethod.cronExpression" 
          placeholder="请输入 cron 表达式"
        />
        <div class="help-text">
          例如：0 0 1 * * ? 表示每天凌晨1点执行
        </div>
      </el-form-item>
      
      <el-form-item label="同步范围">
        <el-radio-group v-model="syncMethod.incrementRange">
          <el-radio label="latest">仅同步最新数据</el-radio>
          <el-radio label="range">指定时间范围</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <div v-if="syncMethod.incrementRange === 'range'" class="date-range">
        <el-form-item label="开始时间">
          <el-date-picker
            v-model="syncMethod.startTime"
            type="datetime"
            placeholder="选择开始时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="syncMethod.endTime"
            type="datetime"
            placeholder="选择结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
      </div>
    </div>
    
    <el-form-item label="数据转换">
      <el-switch 
        v-model="syncMethod.dataTransformation" 
        active-text="启用"
        inactive-text="禁用"
      />
      <div class="help-text">
        启用后可对字段进行重命名、格式转换等操作
      </div>
    </el-form-item>
    
    <el-form-item label="同步日志">
      <el-switch 
        v-model="syncMethod.logEnabled" 
        active-text="启用"
        inactive-text="禁用"
        :checked="true"
      />
      <div class="help-text">
        记录同步过程日志，便于问题排查
      </div>
    </el-form-item>
    
    <el-form-item label="错误处理">
      <el-select v-model="syncMethod.errorHandling">
        <el-option label="忽略错误继续执行" value="ignore" />
        <el-option label="遇到错误停止执行" value="stop" />
        <el-option label="重试失败的记录" value="retry" />
      </el-select>
    </el-form-item>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  syncMethod: {
    type: Object,
    default: () => ({
      type: 'full',
      fullStrategy: 'overwrite',
      incrementField: '',
      syncFrequency: 'manual',
      cronExpression: '',
      incrementRange: 'latest',
      startTime: '',
      endTime: '',
      dataTransformation: false,
      logEnabled: true,
      errorHandling: 'ignore'
    })
  },
  incrementFieldOptions: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits();

// 同步方式配置
const localSyncMethod = ref({ ...props.syncMethod });

// 处理同步类型变化
const handleSyncTypeChange = (type) => {
  // 重置相关配置
  if (type === 'full') {
    localSyncMethod.value.fullStrategy = 'overwrite';
  } else if (type === 'increment') {
    localSyncMethod.value.incrementRange = 'latest';
  }
  emitUpdate();
};

// 触发更新
const emitUpdate = () => {
  emit('update:sync-method', { ...localSyncMethod.value });
};

// 监听本地配置变化
watch(
  localSyncMethod,
  () => {
    emitUpdate();
  },
  { deep: true }
);

// 监听外部配置变化
watch(
  () => props.syncMethod,
  (newVal) => {
    localSyncMethod.value = { ...newVal };
  },
  { deep: true }
);
</script>

<style scoped>
.sync-method-config {
  padding: 10px 0;
}

.sync-method-config h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
}

.sync-type-group {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.sync-option-panel {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
}

.el-form-item {
  margin-bottom: 18px;
}

.help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #666;
  line-height: 1.5;
}

.date-range {
  margin-left: 120px;
}

.date-range .el-form-item {
  margin-bottom: 18px;
}

@media (max-width: 768px) {
  .date-range {
    margin-left: 0;
  }
}
</style>
