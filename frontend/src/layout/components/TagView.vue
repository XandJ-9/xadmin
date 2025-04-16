<template>
  <div class="tags-view-container">
    <el-scrollbar class="tags-view-wrapper">
      <router-link
        v-for="tag in visitedViews"
        :key="tag.path"
        :class="isActive(tag) ? 'active' : ''"
        class="tags-view-item"
        :to="{ path: tag.path, query: tag.query }"
        @contextmenu.prevent="openMenu(tag, $event)"
      >
        {{ tag.title }}
        <el-icon v-if="tag.path !== '/dashboard'"
          class="el-icon-close"
          @click.prevent.stop="closeSelectedTag(tag)"
        >
          <Close />
        </el-icon>
      </router-link>
    </el-scrollbar>
    <ul v-show="visible" :style="{left: leftOffset+'px', top: topOffset+'px'}" class="contextmenu">
      <li @click="refreshSelectedTag(selectedTag)">刷新页面</li>
      <li @click="closeSelectedTag(selectedTag)">关闭当前</li>
      <li @click="closeOthersTags(selectedTag)">关闭其他</li>
      <li @click="closeAllTags">关闭所有</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 提供TagView相关的状态和方法
// provide('visitedViews', visitedViews)
// provide('addView', addView)
// provide('delView', delView)

// 注入Layout组件提供的状态和方法
// const visitedViews = inject('visitedViews')
// const addView = inject('addView')
// const delView = inject('delView')

const visible = ref(false)
const topOffset = ref(0)
const leftOffset = ref(0)
const selectedTag = ref(null)

// TagView状态管理
const visitedViews = ref([{
  name: 'Dashboard',
  path: '/dashboard',
  title: '首页',
  query: {}
}])
const addView = (view) => {
  const isExists = visitedViews.value.some(v => v.path === view.path)
  if (view.meta.needTagview && !isExists) {
    visitedViews.value.push({
      name: view.name,
      path: view.path,
      title: view.meta?.title || '未命名',
      query: view.query
    })
  }
}

const delView = (view) => {
  if(view.path === '/dashboard') return
  const index = visitedViews.value.findIndex(v => v.path === view.path)
  if (index > -1) {
    visitedViews.value.splice(index, 1)
  }
}

// 关闭选中标签
const closeSelectedTag = (view) => {
  delView(view)
  if (isActive(view)) {
    toLastView(visitedViews.value)
  }
}

// 关闭其他标签
const closeOthersTags = (view) => {
  visitedViews.value = visitedViews.value.filter(v => v.path === '/dashboard' || v.path === view.path)
  visible.value = false
}

// 关闭所有标签
const closeAllTags = () => {
  visitedViews.value = visitedViews.value.filter(v => v.path === '/dashboard')
  toLastView(visitedViews.value)
  // router.push('/dashboard')
  visible.value = false
}

// 刷新选中标签
const refreshSelectedTag = (view) => {
  // 关闭右键菜单
  visible.value = false
  
  // 创建一个新的query对象，添加时间戳参数触发组件重新渲染
  const query = { ...view.query, _t: Date.now() }
  
  // 先跳转到一个空路径（但不存在的路径会导致404，所以使用重定向方式）
  const { currentRoute } = router
  const { fullPath } = currentRoute.value
  
  // 通过添加时间戳参数强制路由重新加载
  router.replace({
    path: '/redirect',
    query: { path: fullPath }
  }).then(() => {
    router.replace({
      path: view.path,
      query
    })
  })
}

// 判断是否是激活标签
const isActive = (tag) => {
    if (tag.path === route.path || (!route.meta.needTagview && route.path.includes(tag.path))) {
        // 如果needTagview为false, 
        console.log(tag.path, route)
        return true
    }
  // 如果当前访问的是子路由
}

// 打开右键菜单
const openMenu = (tag, e) => {
  const menuMinWidth = 105
  const offsetLeft = document.querySelector('.tags-view-container').getBoundingClientRect().left
  const offsetWidth = document.querySelector('.tags-view-container').offsetWidth
  const maxLeft = offsetWidth - menuMinWidth
  const left = e.clientX - offsetLeft + 15
  leftOffset.value = left > maxLeft ? maxLeft : left
  topOffset.value = e.clientY
  visible.value = true
  selectedTag.value = tag
}

// 关闭右键菜单
const closeMenu = () => {
  visible.value = false
}

// 跳转到最后一个标签
const toLastView = (visitedViews) => {
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) {
    router.push(latestView.path)
  } else {
    router.push('/dashboard')
  }
}

// 监听路由变化
watch(() => route.path, () => {
  addView(route)
}, { immediate: true })

// 点击页面时关闭右键菜单
const handleClickOutside = (e) => {
  const menu = document.querySelector('.contextmenu')
  if (menu && !menu.contains(e.target)) {
    closeMenu()
  }
}

// 添加点击事件监听
document.addEventListener('click', handleClickOutside)

// 组件卸载时移除监听
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped lang="scss">
.tags-view-container {
  height: 34px;
  width: 100%;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .12), 0 0 3px 0 rgba(0, 0, 0, .04);
  padding-left: 20px;
}

.tags-view-wrapper {
  .tags-view-item {
    display: inline-block;
    position: relative;
    cursor: pointer;
    height: 26px;
    line-height: 26px;
    border: 1px solid #d8dce5;
    color: #495060;
    background: #fff;
    padding: 0 8px;
    font-size: 12px;
    margin-right: 5px;
    margin-top: 4px;
    text-decoration: none;

    &.active {
      background-color: #42b983;
      color: #fff;
      border-color: #42b983;
      &::before {
        content: '';
        background: #fff;
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        position: relative;
        margin-right: 4px;
      }
    }

    .el-icon-close {
      width: 16px;
      height: 16px;
      vertical-align: 2px;
      border-radius: 50%;
      text-align: center;
      transition: all .3s cubic-bezier(.645, .045, .355, 1);
      transform-origin: 100% 50%;

      &:before {
        transform: scale(.6);
        display: inline-block;
        vertical-align: -3px;
      }

      &:hover {
        background-color: #b4bccc;
        color: #fff;
      }
    }
  }
}

.contextmenu {
  margin: 0;
  background: #fff;
  z-index: 3000;
  position: absolute;
  list-style-type: none;
  padding: 5px 0;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 400;
  color: #333;
  box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, .3);

  li {
    margin: 0;
    padding: 7px 16px;
    cursor: pointer;
    &:hover {
      background: #eee;
    }
  }
}
</style>