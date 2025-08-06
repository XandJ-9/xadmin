<template>
  <div class="field-mapping-container">
    <!-- 标题和操作区 -->
    <div class="mapping-header">
      <h2 class="text-xl font-bold">字段映射配置</h2>
      <div class="mapping-actions">
        <button 
          class="btn-reset" 
          @click="resetMappings"
        >
          <i class="fa fa-refresh mr-1"></i>重置映射
        </button>
        <button 
          class="btn-save" 
          @click="handleSave"
        >
          <i class="fa fa-save mr-1"></i>保存配置
        </button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="mapping-content">
      <!-- 源字段区域 -->
      <div class="field-panel source-panel">
        <div class="panel-header">
          <i class="fa fa-database mr-2"></i>
          <h3>源数据字段</h3>
          <span class="field-count">{{ sourceFields.length }}</span>
        </div>
        <div class="field-list">
          <div 
            v-for="field in sourceFields" 
            :key="field.id"
            :class="['field-item', { 
              'mapped': isFieldMapped(field.id, 'source'),
              'dragging': draggingSourceId === field.id
            }]"
            @mousedown="startDrag(field.id, $event)"
            :draggable="!isFieldMapped(field.id, 'source')"
            @dragstart="handleDragStart(field.id, $event)"
          >
            <div class="field-name">{{ field.name }}</div>
            <div class="field-type">{{ field.type }}</div>
          </div>
        </div>
      </div>

      <!-- 连接线区域 -->
      <div 
        class="connection-area"
        @mousemove="handleMouseMove($event)"
        @mouseup="handleMouseUp"
        @dragover.prevent
        @dragleave="handleDragLeave"
      >
        <svg ref="connectionLayer" class="connection-svg"></svg>
      </div>

      <!-- 目标字段区域 -->
      <div class="field-panel target-panel">
        <div class="panel-header">
          <i class="fa fa-table mr-2"></i>
          <h3>目标数据字段</h3>
          <span class="field-count">{{ targetFields.length }}</span>
        </div>
        <div class="field-list">
          <div 
            v-for="field in targetFields" 
            :key="field.id"
            :class="['field-item', { 
              'mapped': isFieldMapped(field.id, 'target'),
              'dragover': dragOverTargetId === field.id
            }]"
            @mouseup="handleTargetMouseUp(field.id)"
            @dragover.prevent="handleTargetDragOver(field.id, $event)"
            @drop="handleDrop(field.id, $event)"
          >
            <div class="field-name">{{ field.name }}</div>
            <div class="field-type">{{ field.type }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 映射关系列表 -->
    <div class="mapping-list">
      <h3 class="mapping-list-title">已建立的映射关系</h3>
      <div v-if="mappings.length === 0" class="no-mappings">
        暂无映射关系，请从左侧源字段拖拽到右侧目标字段建立映射
      </div>
      <div class="mapping-items">
        <div v-for="mapping in mappings" :key="mapping.id" class="mapping-item">
          <div class="mapping-source">{{ getFieldName(mapping.sourceId, 'source') }}</div>
          <i class="fa fa-arrow-right mx-2 text-gray-400"></i>
          <div class="mapping-target">{{ getFieldName(mapping.targetId, 'target') }}</div>
          <button 
            class="delete-mapping" 
            @click="removeMapping(mapping.id)"
            title="删除映射"
          >
            <i class="fa fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';

// 源字段数据
const sourceFields = ref([
  { id: 's1', name: 'user_id', type: 'int' },
  { id: 's2', name: 'username', type: 'varchar' },
  { id: 's3', name: 'email', type: 'varchar' },
  { id: 's4', name: 'register_time', type: 'datetime' },
  { id: 's5', name: 'status', type: 'tinyint' },
  { id: 's6', name: 'age', type: 'int' },
  { id: 's7', name: 'gender', type: 'varchar' },
  { id: 's8', name: 'phone', type: 'varchar' },
]);

// 目标字段数据
const targetFields = ref([
  { id: 't1', name: 'id', type: 'bigint' },
  { id: 't2', name: 'user_name', type: 'string' },
  { id: 't3', name: 'contact_email', type: 'string' },
  { id: 't4', name: 'reg_date', type: 'date' },
  { id: 't5', name: 'user_status', type: 'number' },
  { id: 't6', name: 'user_age', type: 'number' },
  { id: 't7', name: 'sex', type: 'string' },
]);

// 映射关系
const mappings = ref([
  { id: 'm1', sourceId: 's1', targetId: 't1' },
  { id: 'm2', sourceId: 's2', targetId: 't2' },
]);

// 拖拽状态
const isDragging = ref(false);
const draggingSourceId = ref(null);
const dragOverTargetId = ref(null);
const tempConnection = ref(null);
const connectionLayer = ref(null);

// 开始拖拽（鼠标按下）
const startDrag = (sourceId, event) => {
  // 如果已经映射，不允许再次拖拽
  if (isFieldMapped(sourceId, 'source')) return;
  
  isDragging.value = true;
  draggingSourceId.value = sourceId;
  
  // 获取源字段元素位置
  const sourceEl = event.currentTarget;
  const sourceRect = sourceEl.getBoundingClientRect();
  const svgRect = connectionLayer.value.getBoundingClientRect();
  
  // 记录临时连接线的起点
  tempConnection.value = {
    sourceId,
    startX: sourceRect.right - svgRect.left,
    startY: sourceRect.top + sourceRect.height / 2 - svgRect.top,
    endX: event.clientX - svgRect.left,
    endY: event.clientY - svgRect.top
  };
  
  // 绘制临时连接线
  drawTemporaryConnection();
};

// 处理HTML5拖拽开始
const handleDragStart = (sourceId, event) => {
  if (isFieldMapped(sourceId, 'source')) {
    event.preventDefault();
    return;
  }
  
  // 设置拖拽数据
  event.dataTransfer.setData('text/plain', sourceId);
  // 自定义拖拽图像
  const dragImage = document.createElement('div');
  dragImage.textContent = getFieldName(sourceId, 'source');
  dragImage.classList.add('drag-image');
  document.body.appendChild(dragImage);
  event.dataTransfer.setDragImage(dragImage, 0, 0);
  
  // 延迟移除临时元素
  setTimeout(() => {
    document.body.removeChild(dragImage);
  }, 0);
};

// 鼠标移动 - 更新临时连接线
const handleMouseMove = (event) => {
  if (!isDragging.value || !tempConnection.value || !connectionLayer.value) return;
  
  const svgRect = connectionLayer.value.getBoundingClientRect();
  // 更新临时连接线的终点
  tempConnection.value.endX = event.clientX - svgRect.left;
  tempConnection.value.endY = event.clientY - svgRect.top;
  
  // 重新绘制临时连接线
  drawTemporaryConnection();
};

// 鼠标抬起 - 结束拖拽
const handleMouseUp = () => {
  if (isDragging.value) {
    isDragging.value = false;
    draggingSourceId.value = null;
    tempConnection.value = null;
    dragOverTargetId.value = null;
    
    // 重新绘制所有连接线（清除临时线）
    drawConnections();
  }
};

// 处理目标字段拖拽悬停
const handleTargetDragOver = (targetId, event) => {
  event.preventDefault();
  // 如果目标字段未被映射，才允许拖拽到这里
  if (!isFieldMapped(targetId, 'target')) {
    dragOverTargetId.value = targetId;
  } else {
    dragOverTargetId.value = null;
  }
};

// 处理拖拽离开目标区域
const handleDragLeave = () => {
  dragOverTargetId.value = null;
};

// 处理目标字段鼠标抬起 - 完成映射
const handleTargetMouseUp = (targetId) => {
  if (isDragging.value && tempConnection.value && !isFieldMapped(targetId, 'target')) {
    createMapping(tempConnection.value.sourceId, targetId);
  }
};

// 处理放置事件（HTML5拖拽）
const handleDrop = (targetId, event) => {
  event.preventDefault();
  dragOverTargetId.value = null;
  
  const sourceId = event.dataTransfer.getData('text/plain');
  if (sourceId && !isFieldMapped(targetId, 'target') && !isFieldMapped(sourceId, 'source')) {
    createMapping(sourceId, targetId);
  }
  
  // 重置拖拽状态
  isDragging.value = false;
  draggingSourceId.value = null;
  tempConnection.value = null;
};

// 创建映射关系
const createMapping = (sourceId, targetId) => {
  // 移除可能存在的相关映射
  const existingIndex = mappings.value.findIndex(
    m => m.sourceId === sourceId || m.targetId === targetId
  );
  
  if (existingIndex > -1) {
    mappings.value.splice(existingIndex, 1);
  }
  
  // 添加新的映射关系
  mappings.value.push({
    id: `m${Date.now()}`,
    sourceId,
    targetId
  });
};

// 检查字段是否已映射
const isFieldMapped = (id, type) => {
  return mappings.value.some(m => {
    return type === 'source' ? m.sourceId === id : m.targetId === id;
  });
};

// 移除映射关系
const removeMapping = (id) => {
  const index = mappings.value.findIndex(m => m.id === id);
  if (index > -1) {
    mappings.value.splice(index, 1);
    // 重新绘制连接线
    drawConnections();
  }
};

// 重置所有映射
const resetMappings = () => {
  if (confirm('确定要清空所有映射关系吗？')) {
    mappings.value = [];
    // 重新绘制连接线
    drawConnections();
  }
};

// 保存配置
const handleSave = () => {
  // 实际项目中可以发送API请求保存配置
  console.log('保存映射配置:', mappings.value);
  alert('映射配置已保存');
};

// 根据ID获取字段名称
const getFieldName = (id, type) => {
  const fields = type === 'source' ? sourceFields.value : targetFields.value;
  const field = fields.find(f => f.id === id);
  return field ? field.name : '';
};

// 绘制所有正式连接线
const drawConnections = () => {
  if (!connectionLayer.value) return;
  
  // 清空现有连线
  const svg = connectionLayer.value;
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
  
  // 创建箭头标记定义
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
  marker.setAttribute('id', 'arrow-head');
  marker.setAttribute('viewBox', '0 0 10 10');
  marker.setAttribute('refX', '9');
  marker.setAttribute('refY', '5');
  marker.setAttribute('markerWidth', '6');
  marker.setAttribute('markerHeight', '6');
  marker.setAttribute('orient', 'auto');
  
  const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  arrow.setAttribute('d', 'M 0 0 L 10 5 L 0 10 z');
  arrow.setAttribute('fill', '#165DFF');
  marker.appendChild(arrow);
  defs.appendChild(marker);
  svg.appendChild(defs);
  
  // 绘制每条连接线
  mappings.value.forEach(mapping => {
    // 找到源字段和目标字段的DOM元素
    const sourceEl = document.querySelector(`.source-panel .field-item:nth-child(${
      sourceFields.value.findIndex(f => f.id === mapping.sourceId) + 1
    })`);
    
    const targetEl = document.querySelector(`.target-panel .field-item:nth-child(${
      targetFields.value.findIndex(f => f.id === mapping.targetId) + 1
    })`);
    
    if (!sourceEl || !targetEl) return;
    
    // 计算源字段和目标字段的位置
    const sourceRect = sourceEl.getBoundingClientRect();
    const targetRect = targetEl.getBoundingClientRect();
    const svgRect = svg.getBoundingClientRect();
    
    // 计算相对于SVG的坐标
    const startX = sourceRect.right - svgRect.left;
    const startY = sourceRect.top + sourceRect.height / 2 - svgRect.top;
    const endX = targetRect.left - svgRect.left;
    const endY = targetRect.top + targetRect.height / 2 - svgRect.top;
    
    // 创建路径
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    
    // 计算控制点，创建平滑曲线
    const controlX1 = startX + (endX - startX) / 3;
    const controlX2 = startX + (endX - startX) * 2 / 3;
    
    const d = `M ${startX} ${startY} C ${controlX1} ${startY}, ${controlX2} ${endY}, ${endX} ${endY}`;
    path.setAttribute('d', d);
    path.setAttribute('stroke', '#165DFF');
    path.setAttribute('stroke-width', '2');
    path.setAttribute('fill', 'none');
    path.setAttribute('class', 'connection-path');
    path.setAttribute('marker-end', 'url(#arrow-head)');
    
    // 添加鼠标事件，点击连线删除映射
    path.addEventListener('click', () => {
      removeMapping(mapping.id);
    });
    
    svg.appendChild(path);
  });
};

// 绘制临时连接线（拖拽过程中）
const drawTemporaryConnection = () => {
  if (!connectionLayer.value || !tempConnection.value) return;
  
  // 先绘制正式连接线，再在上面绘制临时线
  drawConnections();
  
  const svg = connectionLayer.value;
  const { startX, startY, endX, endY } = tempConnection.value;
  
  // 创建临时路径
  const tempPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  
  // 计算控制点，创建平滑曲线
  const controlX1 = startX + (endX - startX) / 3;
  const controlX2 = startX + (endX - startX) * 2 / 3;
  
  const d = `M ${startX} ${startY} C ${controlX1} ${startY}, ${controlX2} ${endY}, ${endX} ${endY}`;
  tempPath.setAttribute('d', d);
  tempPath.setAttribute('stroke', '#4080FF');
  tempPath.setAttribute('stroke-width', '2');
  tempPath.setAttribute('stroke-dasharray', '5,5');
  tempPath.setAttribute('fill', 'none');
  
  // 添加箭头
  const tempMarker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
  tempMarker.setAttribute('id', 'temp-arrow-head');
  tempMarker.setAttribute('viewBox', '0 0 10 10');
  tempMarker.setAttribute('refX', '9');
  tempMarker.setAttribute('refY', '5');
  tempMarker.setAttribute('markerWidth', '6');
  tempMarker.setAttribute('markerHeight', '6');
  tempMarker.setAttribute('orient', 'auto');
  
  const tempArrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  tempArrow.setAttribute('d', 'M 0 0 L 10 5 L 0 10 z');
  tempArrow.setAttribute('fill', '#4080FF');
  tempMarker.appendChild(tempArrow);
  
  const defs = svg.querySelector('defs') || document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.appendChild(tempMarker);
  if (!svg.querySelector('defs')) {
    svg.appendChild(defs);
  }
  
  tempPath.setAttribute('marker-end', 'url(#temp-arrow-head)');
  svg.appendChild(tempPath);
};

// 监听映射变化，重新绘制连接线
watch(mappings, () => {
  nextTick(() => {
    drawConnections();
  });
}, { deep: true });

// 监听窗口大小变化，重新绘制连接线
const handleResize = () => {
  nextTick(() => {
    drawConnections();
  });
};

onMounted(() => {
  // 初始化绘制连接线
  drawConnections();
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize);
  
  // 组件卸载时移除监听
  return () => {
    window.removeEventListener('resize', handleResize);
  };
});
</script>

<style scoped>
.field-mapping-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 600px;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.mapping-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.mapping-actions {
  display: flex;
  gap: 10px;
}

.btn-reset, .btn-save {
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-reset {
  background-color: #ffffff;
  color: #666666;
  border: 1px solid #dddddd;
}

.btn-reset:hover {
  background-color: #f5f5f5;
}

.btn-save {
  background-color: #165DFF;
  color: white;
}

.btn-save:hover {
  background-color: #0E42D2;
}

.mapping-content {
  display: flex;
  flex: 1;
  gap: 20px;
  margin-bottom: 20px;
  position: relative;
}

.field-panel {
  flex: 1;
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.panel-header {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.field-count {
  background-color: #f0f2f5;
  color: #666;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
}

.field-list {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
}

.field-item {
  padding: 10px 12px;
  margin-bottom: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  user-select: none;
}

.field-item:hover {
  background-color: #f5f7fa;
  border-color: #e5e7eb;
}

.field-item.mapped {
  border-left: 3px solid #165DFF;
  background-color: #f0f7ff;
}

.field-item.dragging {
  opacity: 0.7;
  background-color: #e8f3ff;
}

.field-item.dragover {
  background-color: #e6f7ff;
  border-color: #91d5ff;
}

.field-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.field-type {
  font-size: 12px;
  color: #666;
  background-color: #f5f5f5;
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
}

.connection-area {
  flex: 0.8;
  position: relative;
  min-width: 100px;
  background-color: rgba(240, 247, 255, 0.5);
  border-radius: 6px;
}

.connection-svg {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.connection-path {
  transition: all 0.2s;
  cursor: pointer;
}

.connection-path:hover {
  stroke: #0E42D2;
  stroke-width: 3;
}

.mapping-list {
  background-color: white;
  border-radius: 6px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.mapping-list-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.mapping-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.mapping-item {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.2s;
}

.mapping-item:hover {
  background-color: #eef2f7;
}

.delete-mapping {
  background: none;
  border: none;
  color: #ff4d4f;
  cursor: pointer;
  margin-left: 8px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.delete-mapping:hover {
  background-color: rgba(255, 77, 79, 0.1);
}

.no-mappings {
  color: #666;
  text-align: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
  font-size: 14px;
}

.drag-image {
  position: absolute;
  padding: 4px 8px;
  background-color: #165DFF;
  color: white;
  border-radius: 4px;
  font-size: 12px;
  pointer-events: none;
  opacity: 0.8;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .mapping-content {
    flex-direction: column;
  }
  
  .connection-area {
    height: 150px;
    min-width: auto;
  }
  
  .mapping-items {
    flex-direction: column;
  }
}
</style>
