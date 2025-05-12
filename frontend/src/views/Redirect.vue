<template>
  <div>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
onMounted(() => {
    // 将redirect_to参数移除
    const { redirect_to, ...newQuery } = route.query
    router.replace(
        {
            path: route.query.redirect_to,
            query: newQuery
        }
    )
})
</script>

<style scoped>

</style>