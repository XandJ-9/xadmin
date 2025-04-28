<template>
  <div class="tags-view-container">
    <el-scrollbar class="tags-view-wrapper">
      <router-link
        v-for="tag in visitedViews"
        :key="tag.path"
        :class="isActive(tag) ? 'active' : ''"
        class="tags-view-item"
        :to="{ path: tag.path, query: tag.query }"
        tag="span"
        @contextmenu.prevent="openMenu(tag, $event)"
        @click.middle.prevent="closeSelectedTag(tag)"
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
import { ref, watch, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTagViewsStore } from '@/store/tagviews'

const route = useRoute()
const router = useRouter()
const tagViewsStore = useTagViewsStore()

const visible = ref(false)
const topOffset = ref(0)
const leftOffset = ref(0)
const selectedTag = ref(null)

// 从store获取访问过的路由
const visitedViews = computed(() => tagViewsStore.visitedViews)

// 关闭选中标签
const closeSelectedTag = (view) => {
  const updatedViews = tagViewsStore.delVisitedView(view)
  if (isActive(view)) {
    toLastView(updatedViews)
  }
}

// 关闭其他标签
const closeOthersTags = (view) => {
  tagViewsStore.delOthersVisitedViews(view)
  visible.value = false
}

// 关闭所有标签
const closeAllTags = () => {
  const updatedViews = tagViewsStore.delAllVisitedViews()
  toLastView(updatedViews)
  visible.value = false
}

// 跳转到最后一个标签
const toLastView = (visitedViews) => {
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) {
    router.push(latestView)
  } else {
    router.push('/dashboard')
  }
}

// 刷新选中标签
const refreshSelectedTag = (view) => {
  // 关闭右键菜单
  visible.value = false
  
  // 更新store中的视图
  tagViewsStore.updateVisitedView(view)
  
  // 使用重定向组件刷新页面
  const { currentRoute } = router
  const { fullPath } = currentRoute.value
  
  router.replace({
    path: '/redirect',
    query: { path: fullPath }
  })
}

// 判断是否是激活标签
const isActive = (tag) => {
    if (tag.path === route.path || (!route.meta.needTagview && route.path.includes(tag.path))) {
        // 如果needTagview为false, 
        // console.log(tag.path, route)
    return true
  }
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
  tagViewsStore.addVisitedView(route)
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
  height: 10%;
  width: 100%;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .12), 0 0 3px 0 rgba(0, 0, 0, .04);
  .tags-view-wrapper {
    .tags-view-item {
      display: inline-block;
      position: relative;
      cursor: pointer;
      height: 100%;
      line-height: 26px;
      border: 1px solid #d8dce5;
      color: #495060;
      background: #fff;
      padding: 0 8px;
      font-size: 12px;
      margin-left: 5px;
      margin-top: 4px;
      overflow: hidden;
    //   &:first-of-type {
        // margin-left: 15px;
    //   }
      &:last-of-type {
        margin-right: 15px;
      }
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
          margin-right: 2px;
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
}

.tags-view-wrapper {
  .tags-view-item {
    .el-icon-close {
      width: 16px;
      height: 16px;
    //   vertical-align: 2px;
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


// .tags-view-container {
//   height: 34px;
//   width: 100%;
//   background: #fff;
//   border-bottom: 1px solid #d8dce5;
//   box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .12), 0 0 3px 0 rgba(0, 0, 0, .04);
//   padding-left: 20px;
// }

// .tags-view-wrapper {
//   .tags-view-item {
//     display: inline-block;
//     position: relative;
//     cursor: pointer;
//     height: 26px;
//     line-height: 26px;
//     border: 1px solid #d8dce5;
//     color: #495060;
//     background: #fff;
//     padding: 0 8px;
//     font-size: 12px;
//     margin-right: 5px;
//     margin-top: 4px;
//     text-decoration: none;

//     &.active {
//       background-color: #42b983;
//       color: #fff;
//       border-color: #42b983;
//       &::before {
//         content: '';
//         background: #fff;
//         display: inline-block;
//         width: 8px;
//         height: 8px;
//         border-radius: 50%;
//         position: relative;
//         margin-right: 4px;
//       }
//     }
//     // vertical-align: 2px;
//     .el-icon-close {
//       width: 16px;
//       height: 16px;
      
//       border-radius: 50%;
//       text-align: center;
//       transition: all .3s cubic-bezier(.645, .045, .355, 1);
//       transform-origin: 100% 50%;

//       &:before {
//         transform: scale(.6);
//         display: inline-block;
//         vertical-align: -3px;
//       }

//       &:hover {
//         background-color: #b4bccc;
//         color: #fff;
//       }
//     }
//   }
// }

// .contextmenu {
//   margin: 0;
//   background: #fff;
//   z-index: 3000;
//   position: absolute;
//   list-style-type: none;
//   padding: 5px 0;
//   border-radius: 4px;
//   font-size: 12px;
//   font-weight: 400;
//   color: #333;
//   box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, .3);

//   li {
//     margin: 0;
//     padding: 7px 16px;
//     cursor: pointer;
//     &:hover {
//       background: #eee;
//     }
//   }
// }
</style>