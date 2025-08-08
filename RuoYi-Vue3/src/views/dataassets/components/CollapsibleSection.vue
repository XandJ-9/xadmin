<template>
  <div class="collapsible-section">
    <!-- 标题栏 -->
    <div class="section-header" @click="handleToggle">
      <div class="section-title">
        <i class="title-icon"></i>
        <h2>{{ title }}</h2>
      </div>
      <button 
        class="toggle-btn" 
        :aria-expanded="expanded"
        aria-label="切换展开/折叠状态"
      >
        <i 
          class="el-icon-arrow" 
          :class="{ 'rotate-90': expanded, 'transition-transform': true }"
        ></i>
      </button>
    </div>
    
    <!-- 内容区域 (带动画效果) -->
    <transition name="section-collapse">
      <div 
        class="section-content" 
        v-if="expanded"
        role="region"
        :aria-labelledby="sectionKey"
      >
        <slot></slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // 部分标题
  title: {
    type: String,
    required: true
  },
  // 是否展开状态
  expanded: {
    type: Boolean,
    default: false
  },
  // 部分唯一标识
  sectionKey: {
    type: String,
    required: true
  },
  // 自定义图标
  icon: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['toggle'])

// 处理展开/折叠切换
const handleToggle = () => {
  emit('toggle');
};

// 计算显示的图标
const sectionIcon = computed(() => {
  if (props.icon) return props.icon;
  
  // 根据sectionKey设置默认图标
  switch (props.sectionKey) {
    case 'basic':
      return 'el-icon-info';
    case 'data':
      return 'el-icon-data-board';
    case 'records':
      return 'el-icon-notebook-2';
    default:
      return 'el-icon-menu';
  }
});
</script>

<style scoped>
.collapsible-section {
  margin-bottom: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.2s;
}

.collapsible-section:hover {
  border-color: #e5e7eb;
}

/* 标题栏样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background-color: #fafafa;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.section-header:hover {
  background-color: #f5f5f5;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  color: #1890ff;
  font-size: 18px;
}

.section-title h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2329;
}

/* 切换按钮样式 */
.toggle-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #6b7280;
  transition: color 0.2s;
}

.toggle-btn:hover {
  color: #1890ff;
}

.toggle-btn i {
  font-size: 16px;
  transition: transform 0.3s ease;
}

.rotate-90 {
  transform: rotate(90deg);
}

/* 内容区域样式 */
.section-content {
  padding: 20px;
  background-color: #fff;
}

/* 折叠动画 */
.section-collapse-enter-from,
.section-collapse-leave-to {
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
  overflow: hidden;
}

.section-collapse-enter-active,
.section-collapse-leave-active {
  transition: all 0.3s ease;
}

.section-collapse-enter-to,
.section-collapse-leave-from {
  max-height: 2000px; /* 足够大的值以容纳内容 */
}
</style>
