<template>
  <div class="interface-data-view">
    <el-input v-model="content" type="text" />
    <interface-data-view-item :interface_id="interface_id" :interface_name="interface_name"></interface-data-view-item>
  </div>
</template>



<script>
import { useRoute } from 'vue-router'

export default {
  name: 'InterfaceDataView',

  // 路由监听
  // 修改路由元信息，这样就可以使得复用同一个组件时，元信息是不同的，可以区分部分动态路由
  beforeRouteEnter(to, from, next) {
    if (to.query.interface_name) {
        const title = to.meta.title
        to.meta.title = title + '-' + to.query.interface_name
    }
    next()
  },
}
</script>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router';
import InterfaceDataViewItem from './components/InterfaceDataViewItem.vue';

const route = useRoute()

const interface_id = ref(parseInt(route.params.id))
const interface_name = ref(route.query.interface_name)
const content = ref('')

</script>

<style>

</style>