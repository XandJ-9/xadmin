<template>
  <div class="database-config">
    <h2>{{ title }}</h2>
    <div class="config-tabs">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="选择已有数据库">
          <el-select
            v-model="selectedDbId"
            placeholder="请选择数据库"
            clearable
            class="db-select"
          >
            <el-option
              v-for="db in filteredDatabases"
              :key="db.id"
              :label="db.name"
              :value="db.id"
            />
          </el-select>
          
          <el-card v-if="selectedDb" class="db-info-card">
            <div class="db-info-item">
              <span class="label">数据库名称：</span>
              <span class="value">{{ selectedDb.name }}</span>
            </div>
            <div class="db-info-item">
              <span class="label">数据库类型：</span>
              <span class="value">{{ getDbTypeName(selectedDb.type) }}</span>
            </div>
            <div class="db-info-item">
              <span class="label">连接地址：</span>
              <span class="value">{{ selectedDb.host }}:{{ selectedDb.port }}</span>
            </div>
            <div class="db-info-item">
              <span class="label">数据库名：</span>
              <span class="value">{{ selectedDb.dbName }}</span>
            </div>
            <div class="db-info-item">
              <span class="label">用户名：</span>
              <span class="value">{{ selectedDb.username }}</span>
            </div>
          </el-card>
        </el-tab-pane>
        
        <el-tab-pane label="新增数据库">
          <el-form
            ref="dbForm"
            :model="newDbConfig"
            :rules="dbRules"
            label-width="120px"
            class="db-form"
          >
            <el-form-item label="数据库名称" prop="name">
              <el-input v-model="newDbConfig.name" placeholder="请输入数据库名称" />
            </el-form-item>
            
            <el-form-item label="数据库类型" prop="type">
              <el-select v-model="newDbConfig.type" placeholder="请选择数据库类型">
                <el-option
                  v-for="type in dbTypes"
                  :key="type.value"
                  :label="type.label"
                  :value="type.value"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item label="主机地址" prop="host">
              <el-input v-model="newDbConfig.host" placeholder="请输入主机地址" />
            </el-form-item>
            
            <el-form-item label="端口号" prop="port">
              <el-input v-model="newDbConfig.port" placeholder="请输入端口号" />
            </el-form-item>
            
            <el-form-item label="数据库名" prop="dbName">
              <el-input v-model="newDbConfig.dbName" placeholder="请输入数据库名" />
            </el-form-item>
            
            <el-form-item label="用户名" prop="username">
              <el-input v-model="newDbConfig.username" placeholder="请输入用户名" />
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input v-model="newDbConfig.password" type="password" placeholder="请输入密码" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="testConnection">测试连接</el-button>
              <span v-if="connectionStatus === 'success'" class="connection-status success">
                <i class="el-icon-success"></i> 连接成功
              </span>
              <span v-if="connectionStatus === 'error'" class="connection-status error">
                <i class="el-icon-error"></i> 连接失败
              </span>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      
      <div class="config-actions">
        <el-button 
          type="primary" 
          @click="handleSave"
          :disabled="!canSave"
        >
          保存配置
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, useSlots, useAttrs } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: '数据库配置'
  },
  databases: {
    type: Array,
    default: () => []
  },
  selectedDb: {
    type: Object,
    default: null
  },
  excludeId: {
    type: Number,
    default: null
  }
});

const emit = defineEmits();

// 数据库类型
const dbTypes = [
  { label: 'MySQL', value: 'mysql' },
  { label: 'PostgreSQL', value: 'postgresql' },
  { label: 'Oracle', value: 'oracle' },
  { label: 'SQL Server', value: 'sqlserver' },
  { label: 'MongoDB', value: 'mongodb' }
];

// 过滤排除的数据库
const filteredDatabases = computed(() => {
  return props.databases.filter(db => db.id !== props.excludeId);
});

// 状态管理
const activeTab = ref('0');
const selectedDbId = ref(props.selectedDb?.id || null);
const newDbConfig = ref({
  name: '',
  type: '',
  host: '',
  port: '',
  dbName: '',
  username: '',
  password: ''
});
const connectionStatus = ref(''); // '' | 'success' | 'error'
const dbForm = ref(null);

// 数据库表单验证规则
const dbRules = {
  name: [{ required: true, message: '请输入数据库名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择数据库类型', trigger: 'change' }],
  host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  port: [{ required: true, message: '请输入端口号', trigger: 'blur' }],
  dbName: [{ required: true, message: '请输入数据库名', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }]
};

// 当前选中的数据库
const selectedDb = computed(() => {
  return props.databases.find(db => db.id === selectedDbId.value) || null;
});

// 是否可以保存
const canSave = computed(() => {
  if (activeTab.value === '0') {
    return !!selectedDb.value;
  } else {
    // 简单验证，实际项目中应使用表单验证
    return newDbConfig.value.name && 
           newDbConfig.value.type && 
           newDbConfig.value.host && 
           newDbConfig.value.port && 
           newDbConfig.value.dbName && 
           newDbConfig.value.username;
  }
});

// 获取数据库类型名称
const getDbTypeName = (type) => {
  const dbType = dbTypes.find(t => t.value === type);
  return dbType ? dbType.label : type;
};

// 测试连接
const testConnection = () => {
  // 模拟测试连接
  connectionStatus.value = '';
  setTimeout(() => {
    // 随机模拟成功或失败，实际项目中应真实测试连接
    connectionStatus.value = Math.random() > 0.3 ? 'success' : 'error';
  }, 1000);
};

// 保存配置
const handleSave = () => {
  if (activeTab.value === '0' && selectedDb.value) {
    emit('save', selectedDb.value);
  } else {
    // 模拟新增数据库，实际项目中应保存到后端
    const newDb = {
      id: Date.now(), // 临时ID
      ...newDbConfig.value
    };
    emit('save', newDb);
  }
};

// 监听外部传入的selectedDb变化
watch(
  () => props.selectedDb,
  (newVal) => {
    if (newVal) {
      selectedDbId.value = newVal.id;
      activeTab.value = '0';
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.database-config {
  padding: 10px 0;
}

.database-config h2 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
}

.config-tabs {
  margin-top: 15px;
}

.db-select {
  width: 100%;
  margin-bottom: 20px;
}

.db-info-card {
  margin-top: 15px;
}

.db-info-item {
  margin-bottom: 10px;
  padding: 5px 0;
  border-bottom: 1px dashed #f0f0f0;
}

.db-info-item:last-child {
  border-bottom: none;
}

.label {
  display: inline-block;
  width: 100px;
  color: #666;
}

.value {
  color: #333;
}

.db-form {
  margin-top: 15px;
}

.config-actions {
  margin-top: 30px;
  text-align: right;
}

.connection-status {
  margin-left: 15px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}

.success {
  background-color: #f0f9eb;
  color: #52c41a;
}

.error {
  background-color: #fef0f0;
  color: #f5222d;
}
</style>
