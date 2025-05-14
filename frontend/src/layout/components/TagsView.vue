<template>
  <div class="tags-view-container">
    <!-- <el-scrollbar class="tags-view-wrapper"> -->
    <div class="tags-view-wrapper">
        <router-link
        v-for="tag in visitedViews"
        :key="tag.path"
        :class="isActive(tag) ? 'active' : ''"
        class="tags-view-item"
        :to="{ path: tag.path, query: tag.query, fullPath: tag.fullPath }"
        tag="span"
        @contextmenu.prevent="openMenu(tag, $event)"
        @click.middle.prevent="closeSelectedTag(tag)"
      >
        {{ tag.title }}
        <el-icon v-if="!isAffix(tag)"
          class="el-icon-close"
          @click.prevent.stop="closeSelectedTag(tag)"
        >
          <Close />
        </el-icon>
      </router-link>
    </div>
    <!-- </el-scrollbar> -->
    <ul v-show="visible" :style="{left: leftOffset+'px', top: topOffset+'px'}" class="contextmenu">
      <li @click="refreshSelectedTag(selectedTag)">刷新页面</li>
      <li @click="closeSelectedTag(selectedTag)">关闭当前</li>
      <li @click="closeOthersTags(selectedTag)">关闭其他</li>
      <li @click="closeAllTags">关闭所有</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTagsViewStore } from '@/store/modules/tagsView'
const route = useRoute()
const router = useRouter()
const tagsViewStore = useTagsViewStore()

const visible = ref(false)
const topOffset = ref(0)
const leftOffset = ref(0)
const selectedTag = ref(null)

// 从store获取访问过的路由
const visitedViews = computed(() => tagsViewStore.visitedViews)


const initTags = () => {
    if (tagsViewStore.visitedViews.length === 0)
    tagsViewStore.addView(route)
}
const addTags = () => {
  tagsViewStore.addView(route)
  // let { name } = route;
  // let currentTagView = null;
    // let parent = route.matched[route.matched.length - 1].parent;
    // if (name) {
    //     if (!route.meta.newTagview) {
    //         currentTagView = parent;
    //     } else {
    //         currentTagView = route;
    //     }
    //     tagsViewStore.addView(currentTagView)
    // }
    return false
}

const isAffix = (tag) => {
    return tag.meta && tag.meta.affix
}

// 关闭选中标签
const closeSelectedTag = (view) => {
  tagsViewStore.delView(view).then(({ visitedViews }) => {
    if (isActive(view)) {
      toLastView(visitedViews)
    }
  })
}

// 关闭其他标签
const closeOthersTags = (view) => {
  tagsViewStore.delOthersViews(view).then(({ visitedViews }) => {
    toLastView(visitedViews)
    visible.value = false
  })
}

// 关闭所有标签
const closeAllTags = () => {
  tagsViewStore.delAllViews().then(({ visitedViews }) => {
    toLastView(visitedViews)
    visible.value = false
  })
}

// 跳转到最后一个标签
const toLastView = (visitedViews) => {
    const latestView = visitedViews.slice(-1)[0]
      if (latestView) {
        router.push(latestView.fullPath)
      } else {
        // now the default is to redirect to the home page if there is no tags-view,
        // you can adjust it according to your needs.
        if (view.name === 'Dashboard') {
          // to reload home page
          router.replace({ path: '/redirect' + view.fullPath })
        } else {
          router.push('/')
        }
      }
}

// 刷新选中标签
const refreshSelectedTag = (view) => {
  // 关闭右键菜单
  visible.value = false
    tagsViewStore.delVisitedView(view).then(() => {
        router.replace({
            path: '/redirect' + view.fullPath
        })
    })
}

// 判断是否是激活标签
const isActive = (tag) => {
  // if (tag.path === route.path || (!route.meta.needTagview && route.path.includes(tag.path))) {
    if (tag.path === route.path) {
    return true
  }
  return false
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

// 监听路由变化，添加到访问记录
watch(() => route.path, () => {
    // tagsViewStore.addView(route)
    addTags()
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

    background-color: #ffffff;
    border-bottom: 1px solid #e6e6e6;
    // display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 10px;
    height:40px !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;

  .tags-view-wrapper {
    height: 100%;
    width: 100%;
    overflow-x: auto;
    white-space: nowrap;
    .tags-view-item {
      display: inline-block;
      cursor: pointer;
      height: 28px;
      line-height: 28px;
      border: 1px solid #e0e3e9;
      background: #fff;
      padding: 0 10px;
      margin: 5px 4px;
      font-size: 12px;
      border-radius: 3px;
      transition: all 0.2s ease;

    &:hover {
      background-color: #f5f7fa;
    }
    
    .el-icon-close {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      vertical-align: middle;
      text-align: center;
      transition: all .2s ease;
      transform-origin: 100% 50%;
      margin-left: 2px;
      &:before {
        transform: scale(.6);
        display: inline-block;
        vertical-align: -3px;
      }
      &:hover {
        background-color: #909399;
        color: #fff;
      }
    }

      &:last-of-type {
        margin-right: 15px;
      }
      &.active {
        background-color: #409EFF;
        color: #fff;
        border-color: #409EFF;
        &::before {
          content: '';
          background: #fff;
          display: inline-block;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          position: relative;
          margin-right: 4px;
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
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    li {
      margin: 0;
      padding: 8px 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      &:hover {
        background: #f5f7fa;
        color: #409EFF;
      }
    }
  }
}

</style>