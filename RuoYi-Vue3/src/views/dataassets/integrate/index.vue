<template>
    <!-- 数据集成页面 -->
  <div class="app-container">

       <!-- 步骤条 -->
    <el-steps :active="activeStep" finish-status="success" class="mb-4">
      <el-step title="选择数据源" description="配置源端和目标端" />
      <el-step title="配置同步规则" description="设置同步方式和规则" />
      <el-step title="确认并执行" description="检查配置并启动同步" />
    </el-steps>
    <!-- 步骤控制按钮 -->
    <div class="step-actions">
      <el-button v-if="activeStep > 0" @click="prevStep">上一步</el-button>
      <el-button
        v-if="activeStep < 2"
        type="primary"
        @click="nextStep"
      >下一步</el-button>
      <el-button
        v-else
        type="success"
        :disabled="!canSync"
        @click="handleSync"
      >开始同步</el-button>
    </div>
        <!-- 步骤内容区 -->
    <div class="step-content">
      <!-- 第一步：数据源配置 -->
      <div v-show="activeStep === 0">
        <el-form :inline="true" class="form-inline">
            <el-select v-model="selectedSource" placeholder="请选择数据源" style="width: 220px">
            <el-option
                v-for="source in dataSourceOptions"
                :key="source.id"
                :label="source.name"
                :value="source.id"
            />
            </el-select>
        </el-form>
      </div>

      <!-- 第二步：同步规则配置 -->
      <div v-show="activeStep === 1">
        <el-card class="rule-card">
          <el-tabs v-model="ruleTab">
            <el-tab-pane label="基础配置" name="basic">
              <el-form :model="syncRule" label-width="120px">
                <el-form-item value="同步方式">
                  <el-radio-group v-model="syncRule.type">
                    <el-radio value="full">全量同步</el-radio>
                    <el-radio value="increment">增量同步</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="同步周期">
                  <el-select v-model="syncRule.schedule">
                    <el-option label="实时同步" value="realtime" />
                    <el-option label="每天" value="daily" />
                    <el-option label="每周" value="weekly" />
                  </el-select>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="高级配置" name="advanced">
              <!-- <json-editor v-model="syncRule.advanced" /> -->
               <!-- 选择需要同步的数据表 -->
                <!-- 1. 单租户单表同步 -->
                <!-- 2. 多租户单表同步 -->
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>

      <!-- 第三步：确认配置 -->
      <div v-show="activeStep === 2">
        <el-card>
          <el-descriptions title="同步配置确认" :column="1" border>
            <el-descriptions-item label="数据源">
              {{ selectedSource }}
            </el-descriptions-item>
            <el-descriptions-item label="目标租户">
              {{ selectedTenants }}
            </el-descriptions-item>
            <el-descriptions-item label="同步方式">
              {{ syncRule.type === 'full' ? '全量同步' : '增量同步' }}
            </el-descriptions-item>
            <el-descriptions-item label="同步周期">
              {{ syncRule.schedule }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDataSourceList, getDataSourceTypeList, createDataSource, updateDataSource, deleteDataSource, saveSqlQuery } from '@/api/dataassets/datasource'

// 模拟数据源、模板库、租户库
const dataSourceOptions = ref([])


const selectedSource = ref('')
const selectedTemplate = ref('')
const selectedTenants = ref([])
const syncResult = ref('')

const canSync = computed(() =>
  selectedSource.value && selectedTemplate.value && selectedTenants.value.length > 0
)

function handleSync() {
  // 这里应调用后端API进行同步，下面为模拟逻辑
  syncResult.value = `同步成功：数据源【${getSourceName()}】，模板库【${getTemplateName()}】，租户【${getTenantNames().join('、')}】`
  ElMessage.success('同步任务已提交')
}

const fetchdataSources = async () => {
    await getDataSourceList().then(res => {
        dataSourceOptions.value = res.data
    })
    .then(res => {

     })
    .catch(error => {
          ElMessage.error('获取数据源列表失败')
     })
}


// ...existing code...

const activeStep = ref(0)
const ruleTab = ref('basic')
const syncRule = ref({
  type: 'full',
  schedule: 'daily',
  advanced: {}
})

const nextStep = () => {
  if (activeStep.value < 2) activeStep.value++
}

const prevStep = () => {
  if (activeStep.value > 0) activeStep.value--
}

// 可在 onMounted 时请求后端接口获取真实数据
onMounted(() => {
    // TODO: fetch dataSources, templateList, tenantList from API
  fetchdataSources()
})
</script>

<style scoped>

.form-inline {
  margin-bottom: 20px;
}
.tenant-card {
  margin-top: 10px;
  padding: 16px;
}
.card-header {
  font-weight: bold;
  font-size: 15px;
}
</style>