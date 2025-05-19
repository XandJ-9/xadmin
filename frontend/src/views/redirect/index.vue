<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
onMounted(() => {
    const { params, query } = route 
    const { path } = params
    console.log('redirect to: ', path)
    console.log('params: ', params)
    console.log('query: ', query)
    router.replace({
        path: '/' + path,
        query
    })
})
</script>

<template>
    
</template>
<style scoped>

</style>