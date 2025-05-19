<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
onMounted(() => {
    const { params, query } = route 
    const { path } = params
    console.log('redirect to: ', path, 'params: ', params, 'query: ', query)
    router.replace({
        path: '/' + path,
        query
    })
})
</script>

<style scoped>

</style>