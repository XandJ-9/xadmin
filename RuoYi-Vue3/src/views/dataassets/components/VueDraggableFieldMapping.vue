<template>
  <div class="field-mapping-container">
    <!-- 标题和操作区 -->
    <div class="mapping-header">
      <h2 class="text-xl font-bold">字段映射配置</h2>
      <div class="mapping-actions">
        <button class="btn-reset" @click="resetMappings">
          <i class="fa fa-refresh mr-1"></i>重置映射
        </button>
        <button class="btn-save" @click="handleSave">
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
          <span class="field-count">{{ availableSourceFields.length }}</span>
        </div>
        <div class="field-list">
          <!-- 源字段拖拽列表 -->
          <draggable
            v-model="availableSourceFields"
            :group="{ name: 'fields', pull: 'clone', put: false }"
            :sort="false"
            :clone="cloneSourceField"
            @start="handleDragStart"
            @end="handleDragEnd"
            item-key="id"
          >
            <template #item="{ element }">
              <div 
                class="field-item"
                v-memo="[element.id, isFieldMapped(element.id, 'source')]"
              >
                <div class="field-name">{{ element.name }}</div>
                <div class="field-type">{{ element.type }}</div>
              </div>
            </template>
          </draggable>
        </div>
      </div>

      <!-- 连接线区域 -->
      <div class="connection-area">
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
          <!-- 目标字段拖拽列表 -->
          <draggable
            v-model="targetFields"
            :group="{ name: 'fields', pull: false, put: true }"
            :sort="false"
            @add="handleTargetAdd"
            item-key="id"
          >
            <template #item="{ element }">
              <div 
                class="field-item"
                :class="{ 'mapped': element.mappedSourceId }"
                v-memo="[element.id, element.mappedSourceId]"
              >
                <div class="field-name">{{ element.name }}</div>
                <div class="field-type">{{ element.type }}</div>
                <button 
                  v-if="element.mappedSourceId"
                  class="unmap-btn"
                  @click.stop="removeMappingByTarget(element.id)"
                >
                  <i class="fa fa-times"></i>
                </button>
              </div>
            </template>
          </draggable>
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
        <div 
          v-for="mapping in mappings" 
          :key="mapping.id" 
          class="mapping-item"
        >
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
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import draggable from 'vuedraggable';
import { throttle } from 'lodash-es'; // 使用lodash的节流函数

// 原始源字段数据
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

// 目标字段数据（添加mappedSourceId属性记录映射关系）
const targetFields = ref([
  { id: 't1', name: 'id', type: 'bigint', mappedSourceId: null },
  { id: 't2', name: 'user_name', type: 'string', mappedSourceId: null },
  { id: 't3', name: 'contact_email', type: 'string', mappedSourceId: null },
  { id: 't4', name: 'reg_date', type: 'date', mappedSourceId: null },
  { id: 't5', name: 'user_status', type: 'number', mappedSourceId: null },
  { id: 't6', name: 'user_age', type: 'number', mappedSourceId: null },
  { id: 't7', name: 'sex', type: 'string', mappedSourceId: null },
]);

// 映射关系
const mappings = ref([
  { id: 'm1', sourceId: 's1', targetId: 't1' },
  { id: 'm2', sourceId: 's2', targetId: 't2' },
]);

// 可用的源字段（未被映射的）
const availableSourceFields = computed(() => {
  const mappedSourceIds = new Set(mappings.value.map(m => m.sourceId));
  return sourceFields.value.filter(field => !mappedSourceIds.has(field.id));
});

// 状态管理
const draggingSource = ref(null);
const connectionLayer = ref(null);
const svgElements = ref(new Map()); // 缓存SVG元素
const fieldElements = ref({
  source: new Map(),
  target: new Map()
});

// 初始化目标字段的映射关系
const initTargetMappings = () => {
  targetFields.value.forEach(target => {
    const mapping = mappings.value.find(m => m.targetId === target.id);
    target.mappedSourceId = mapping ? mapping.sourceId : null;
  });
};

// 克隆源字段（用于拖拽时的视觉反馈）
const cloneSourceField = (original) => {
  draggingSource.value = { ...original };
  return { ...original, _isClone: true };
};

// 处理拖拽开始
const handleDragStart = () => {
  // 添加拖拽中类名，用于样式控制
  document.querySelector('.connection-area').classList.add('dragging-active');
};

// 处理拖拽结束
const handleDragEnd = () => {
  // 移除拖拽中类名
  document.querySelector('.connection-area')?.classList.remove('dragging-active');
  draggingSource.value = null;
};

// 处理目标字段添加（完成映射）
const handleTargetAdd = (evt) => {
  if (!draggingSource.value || !evt.added || evt.added._isClone) {
    // 移除克隆元素，我们只需要建立映射关系而不是实际移动
    evt.preventDefault();
    
    if (draggingSource.value && evt.newIndex !== undefined) {
      const targetId = targetFields.value[evt.newIndex].id;
      createMapping(draggingSource.value.id, targetId);
    }
    
    return;
  }
};

// 创建映射关系
const createMapping = (sourceId, targetId) => {
  // 移除冲突映射（同一源或目标只能有一个映射）
  const conflictingMappings = mappings.value.filter(
    m => m.sourceId === sourceId || m.targetId === targetId
  );
  
  conflictingMappings.forEach(mapping => {
    removeMapping(mapping.id);
  });
  
  // 添加新映射
  const newMapping = {
    id: `m${Date.now()}`,
    sourceId,
    targetId
  };
  
  mappings.value.push(newMapping);
  initTargetMappings();
};

// 检查字段是否已映射
const isFieldMapped = (id, type) => {
  return mappings.value.some(m => 
    type === 'source' ? m.sourceId === id : m.targetId === id
  );
};

// 移除映射关系
const removeMapping = (id) => {
  const index = mappings.value.findIndex(m => m.id === id);
  if (index > -1) {
    mappings.value.splice(index, 1);
    
    // 更新目标字段映射状态
    initTargetMappings();
    
    // 移除对应的SVG元素
    if (svgElements.value.has(id)) {
      connectionLayer.value?.removeChild(svgElements.value.get(id));
      svgElements.value.delete(id);
    }
  }
};

// 根据目标字段ID移除映射
const removeMappingByTarget = (targetId) => {
  const mapping = mappings.value.find(m => m.targetId === targetId);
  if (mapping) {
    removeMapping(mapping.id);
  }
};

// 重置所有映射
const resetMappings = () => {
  if (confirm('确定要清空所有映射关系吗？')) {
    mappings.value = [];
    initTargetMappings();
    
    // 清空SVG缓存和元素
    svgElements.value.forEach(el => connectionLayer.value?.removeChild(el));
    svgElements.value.clear();
  }
};

// 保存配置
const handleSave = () => {
  console.log('保存映射配置:', mappings.value);
  alert('映射配置已保存');
};

// 根据ID获取字段名称
const getFieldName = (id, type) => {
  if (type === 'source') {
    const field = sourceFields.value.find(f => f.id === id);
    return field ? field.name : '';
  } else {
    const field = targetFields.value.find(f => f.id === id);
    return field ? field.name : '';
  }
};

// 缓存字段DOM元素
const cacheFieldElements = () => {
  // 缓存源字段元素（只缓存可用的源字段）
  availableSourceFields.value.forEach((field, index) => {
    fieldElements.value.source.set(
      field.id,
      document.querySelector(`.source-panel .field-item:nth-child(${index + 1})`)
    );
  });
  
  // 缓存目标字段元素
  targetFields.value.forEach((field, index) => {
    fieldElements.value.target.set(
      field.id,
      document.querySelector(`.target-panel .field-item:nth-child(${index + 1})`)
    );
  });
};

// 绘制所有连接线
const drawConnections = () => {
  if (!connectionLayer.value) return;
  
  const svg = connectionLayer.value;
  const svgRect = svg.getBoundingClientRect();
  
  // 清空现有连线
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
  svgElements.value.clear();
  
  // 创建箭头标记
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
    const sourceEl = fieldElements.value.source.get(mapping.sourceId);
    const targetEl = fieldElements.value.target.get(mapping.targetId);
    
    if (!sourceEl || !targetEl) return;
    
    // 计算位置
    const sourceRect = sourceEl.getBoundingClientRect();
    const targetRect = targetEl.getBoundingClientRect();
    
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
    
    // 添加点击删除事件
    path.addEventListener('click', () => removeMapping(mapping.id));
    
    svg.appendChild(path);
    svgElements.value.set(mapping.id, path);
  });
};

// 节流处理窗口大小变化
const handleResizeThrottled = throttle(() => {
  nextTick(() => {
    cacheFieldElements();
    drawConnections();
  });
}, 100);

// 监听映射变化
watch(mappings, () => {
  nextTick(() => {
    cacheFieldElements();
    drawConnections();
  });
}, { deep: true });

// 监听可用源字段变化（用于重新缓存元素）
watch(availableSourceFields, () => {
  nextTick(() => {
    cacheFieldElements();
    drawConnections();
  });
}, { deep: true });

onMounted(() => {
  // 初始化目标字段映射状态
  initTargetMappings();
  
  // 缓存字段元素并绘制连接线
  nextTick(() => {
    cacheFieldElements();
    drawConnections();
  });
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResizeThrottled);
  
  return () => {
    window.removeEventListener('resize', handleResizeThrottled);
  };
});
</script>

<style scoped>
/* 基础样式保持一致 */
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

/* 字段项样式增强 */
.field-item {
  padding: 10px 12px;
  margin-bottom: 8px;
  border-radius: 4px;
  cursor: grab;
  transition: all 0.2s;
  border: 1px solid transparent;
  position: relative;
}

.field-item:hover {
  background-color: #f5f7fa;
  border-color: #e5e7eb;
}

.field-item.mapped {
  border-left: 3px solid #165DFF;
  background-color: #f0f7ff;
}

/* 拖拽相关样式 */
.field-item.sortable-ghost {
  opacity: 0.3;
  background-color: #e6f7ff;
}

.field-item.sortable-chosen {
  background-color: #e8f3ff;
  border-color: #91d5ff;
  cursor: grabbing;
}

.connection-area {
  flex: 0.8;
  position: relative;
  min-width: 100px;
  background-color: rgba(240, 247, 255, 0.5);
  border-radius: 6px;
  transition: background-color 0.2s;
}

.connection-area.dragging-active {
  background-color: rgba(224, 242, 254, 0.7);
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

/* 映射列表样式 */
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

/* 目标字段的取消映射按钮 */
.unmap-btn {
  position: absolute;
  right: 6px;
  top: 6px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: all 0.2s;
}

.unmap-btn:hover {
  background-color: rgba(255, 77, 79, 0.1);
  color: #ff4d4f;
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
