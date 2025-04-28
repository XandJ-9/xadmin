<template>
  <div class="interface-data-view">
    <interface-data-view-item :interface_id="interface_id" :interface_code="interface_code" :interface_name="interface_name"></interface-data-view-item>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue'
import { useRouter,useRoute, onBeforeRouteUpdate } from 'vue-router'
import InterfaceDataViewItem from './components/InterfaceDataViewItem.vue'

const route = useRoute()
const router = useRouter()
const interface_id = ref(parseInt(route.query.interface_id))
const interface_code = ref(route.query.interface_code)
const interface_name = ref(route.query.interface_name)

router.beforeResolve(async (to, from) => {
    if (to.query.interface_name) {
        console.log('to.query.interface_name', route.query.interface_name)
        const title = to.meta.title
        to.meta.title = route.query.interface_name
    }
})

// onBeforeRouteUpdate((to, form) => {
//       console.log('onBeforeRouteUpdate to', to)
//       if (route.query.interface_name) {
//           const title = to.meta.title
//           to.meta.title = title + ' - ' + route.query.interface_name
//           console.log('meta title', to.meta.title)
//       }
//   })
</script>

<style>

</style>