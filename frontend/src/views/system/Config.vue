<template>
  <div class="system-config-container">
      <el-form :model="configForm" label-width="120px">
        <el-form-item label="系统名称">
          <el-input v-model="configForm.systemName"></el-input>
        </el-form-item>
        <el-form-item label="系统版本">
          <el-input v-model="configForm.version"></el-input>
        </el-form-item>
        <el-form-item label="管理员邮箱">
          <el-input v-model="configForm.adminEmail"></el-input>
        </el-form-item>
        <el-form-item label="是否开启注册">
          <el-switch v-model="configForm.enableRegister"></el-switch>
        </el-form-item>
        <el-form-item label="是否开启日志">
          <el-switch v-model="configForm.enableLog"></el-switch>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveConfig">保存配置</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
  </div>
</template>

<script>
export default { name: 'SysConfig' }
</script>
<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const configForm = ref({
  systemName: 'XAdmin管理系统',
  version: '1.0.0',
  adminEmail: 'admin@example.com',
  enableRegister: true,
  enableLog: true
})

const saveConfig = () => {
  // 这里添加保存配置的逻辑
  ElMessage.success('配置保存成功')
}

const resetForm = () => {
  // 重置表单
  configForm.value = {
    systemName: 'XAdmin管理系统',
    version: '1.0.0',
    adminEmail: 'admin@example.com',
    enableRegister: true,
    enableLog: true
  }
}
</script>

<style scoped>
.system-config-container {
  padding: 20px;
}

.box-card {
  margin-top: 20px;
}
</style>