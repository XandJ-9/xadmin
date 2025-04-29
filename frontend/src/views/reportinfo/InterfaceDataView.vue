<template>
  <div class="interface-data-view">
    <interface-data-view-item :interface_id="interface_id" :interface_name="interface_name"></interface-data-view-item>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'
import InterfaceDataViewItem from './components/InterfaceDataViewItem.vue'

export default {
  name: 'InterfaceDataView',
  components: {
    InterfaceDataViewItem
  },
  data: () => {
    const route = useRoute()
    return {
      interface_id: parseInt(route.params.id),
      // interface_code: route.query.interface_code,
      interface_name: route.query.interface_name
    }
    },

  // 路由监听
  // 修改路由元信息，这样就可以使得复用同一个组件时，元信息是不同的，可以区分部分动态路由
  beforeRouteEnter(to, from, next) {
    if (to.query.interface_name) {
        const title = to.meta.title
        to.meta.title = title +'-'+ to.query.interface_name
    }
    next()
  }

}

// const route = useRoute()
// const router = useRouter()
// const interface_id = ref(parseInt(route.query.interface_id))
// const interface_code = ref(route.query.interface_code)
// const interface_name = ref(route.query.interface_name)

// router.beforeEach(async (to, from) => {
//     if (to.query.interface_name) {
//         to.meta.title = '接口查询-' + to.query.interface_name
//         console.log('meta title',from.path, to.path)
//     }
// })

// onBeforeRouteUpdate((to, form) => {
//       console.log('onBeforeRouteUpdate to', to)
//       if (route.query.interface_name) {
//           const title = to.meta.title
//           to.meta.title = title + ' - ' + to.query.interface_name
//           console.log('meta title', to.meta.title)
//       }
//   })
</script>

<style>

</style>