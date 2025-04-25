<template>
  <div class="login-container">
    <div class="login-box">
      <!-- <h2>后台管理系统</h2> -->
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%">登录</el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="primary" @click="goToRegister" style="width: 100%; text-align: center;">没有账号？去注册</el-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const goToRegister = () => {
  router.push('/register')
}

const userStore = useUserStore()

const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
        try {
            // 创建FormData对象并添加表单数据
            const formdata = new FormData()
            formdata.append('username', loginForm.username)
            formdata.append('password', loginForm.password)
            // 使用Pinia store进行登录
            const result = await userStore.login(formdata)
            if (result.success) {
                ElMessage.success(result.message)
                router.push('/dashboard')
            } else {
                ElMessage.error(result.message)
                router.push('/login')
            }
      } catch (error) {
        ElMessage.error('登录失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 35px;
  color: #303133;
  font-size: 24px;
  font-weight: 500;
}

.el-input {
  margin-bottom: 5px;
}

.el-button--primary {
  margin-top: 10px;
  height: 42px;
  font-size: 16px;
}
</style>