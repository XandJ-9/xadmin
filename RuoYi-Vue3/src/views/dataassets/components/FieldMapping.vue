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
              'selected': selectedSourceId === field.id,
              'mapped': isFieldMapped(field.id, 'source')
            }]"
            @click="selectSourceField(field.id)"
          >
            <div class="field-name">{{ field.name }}</div>
            <div class="field-type">{{ field.type }}</div>
          </div>
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
          <div 
            v-for="field in targetFields" 
            :key="field.id"
            :class="['field-item', { 
              'selected': selectedTargetId === field.id,
              'mapped': isFieldMapped(field.id, 'target')
            }]"
            @click="selectTargetField(field.id)"
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
        暂无映射关系，请在左侧选择源字段，右侧选择目标字段建立映射
      </div>
      <div class="mapping-items">
        <div v-for="mapping in mappings" :key="mapping.id" class="mapping-item">
          <div class="mapping-source">{{ getFieldName(mapping.sourceId, 'source') }}</div>
          <i class="fa fa-arrow-right mx-2 text-gray-400"></i>
          <div class="mapping-target">{{ getFieldName(mapping.targetId, 'target') }}</div>
          <button 
            class="delete-mapping" 
            @click="removeMapping(mapping.id)"
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
  { id: 'm3', sourceId: 's3', targetId: 't3' },
]);

// 选中状态
const selectedSourceId = ref(null);
const selectedTargetId = ref(null);
const connectionLayer = ref(null);

// 选择源字段
const selectSourceField = (id) => {
  // 如果点击已选中的字段，则取消选择
  if (selectedSourceId.value === id) {
    selectedSourceId.value = null;
    return;
  }
  
  selectedSourceId.value = id;
  selectedTargetId.value = null;
};

// 选择目标字段
const selectTargetField = (id) => {
  // 如果没有选中源字段，不处理
  if (!selectedSourceId.value) return;
  
  // 如果已经存在映射关系，先移除
  const existingIndex = mappings.value.findIndex(
    m => m.sourceId === selectedSourceId.value || m.targetId === id
  );
  
  if (existingIndex > -1) {
    mappings.value.splice(existingIndex, 1);
  }
  
  // 添加新的映射关系
  mappings.value.push({
    id: `m${Date.now()}`,
    sourceId: selectedSourceId.value,
    targetId: id
  });
  
  // 清空选择
  selectedSourceId.value = null;
  selectedTargetId.value = null;
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
  }
};

// 重置所有映射
const resetMappings = () => {
  if (confirm('确定要清空所有映射关系吗？')) {
    mappings.value = [];
    selectedSourceId.value = null;
    selectedTargetId.value = null;
  }
};

// 保存配置
const handleSave = () => {
  // 这里只是模拟保存，实际项目中可以发送API请求
  console.log('保存映射配置:', mappings.value);
  alert('映射配置已保存');
};

// 根据ID获取字段名称
const getFieldName = (id, type) => {
  const fields = type === 'source' ? sourceFields.value : targetFields.value;
  const field = fields.find(f => f.id === id);
  return field ? field.name : '';
};

// 绘制连接线
const drawConnections = () => {
  if (!connectionLayer.value) return;
  
  // 清空现有连线
  const svg = connectionLayer.value;
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
  
  // 获取SVG位置和尺寸
  const svgRect = svg.getBoundingClientRect();
  
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
    
    // 添加鼠标事件，点击连线删除映射
    path.addEventListener('click', () => {
      removeMapping(mapping.id);
    });
    
    svg.appendChild(path);
    
    // 添加箭头标记
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', `arrow-${mapping.id}`);
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
    
    path.setAttribute('marker-end', `url(#arrow-${mapping.id})`);
  });
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
}

.field-panel {
  flex: 1;
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
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
}

.field-item:hover {
  background-color: #f5f7fa;
  border-color: #e5e7eb;
}

.field-item.selected {
  background-color: #e8f3ff;
  border-color: #165DFF;
}

.field-item.mapped {
  border-left: 3px solid #165DFF;
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
