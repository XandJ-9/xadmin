<template>
  <div class="app-container">
    <interface-data-view-item :interface_id="interface_id" :interface_name="interface_name"></interface-data-view-item>
  </div>
</template>



<script>
import { useRoute, useRouter } from 'vue-router'

export default {
 name: 'InterfaceDataView',
  // 路由监听
  // 修改路由元信息，这样就可以使得复用同一个组件时，元信息是不同的，可以区分不同动态路由
  beforeRouteEnter(to, from, next) {
    if (to.query.interface_name) {
        const title = to.meta.title
        to.meta.title = title + '-' + to.query.interface_name
        to.meta.activeMenu = '/report/interface/interfaceManage'
      }
    next()
  },

}
</script>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router';
import InterfaceDataViewItem from './components/InterfaceDataViewItem.vue';

const route = useRoute()

const interface_id = ref(parseInt(route.params.id))
const interface_name = ref(route.query.interface_name)

</script>

<style>

</style>