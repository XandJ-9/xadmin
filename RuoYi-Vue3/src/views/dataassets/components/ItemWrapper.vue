<template>
  <div class="item-box">
    <component
      :is="currentComponent"
      v-model="modelValue"
      v-bind="componentProps"
      @change="onChange"
    >
      <!-- 仅 el-select 和 el-radio-group 需要插入选项 -->
      <template v-if="isSelectLike" v-for="item in selectOptions" :key="item.value">
        <el-option
          v-if="currentComponent === 'el-select'"
          :label="item.label"
          :value="item.value"
        />
        <el-radio
          v-else-if="currentComponent === 'el-radio-group'"
          :label="item.value"
        >{{ item.label }}</el-radio>
      </template>
    </component>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

// props: type, options, value, placeholder, min, max, step, etc.
const props = defineProps({
  type: { type: String, default: 'input' }, // select, radio, input, input-number
  options: { type: Array, default: () => [] }, // 选项数组
  modelValue: [String, Number, Array], // v-model
  placeholder: String,
  min: Number,
  max: Number,
  step: Number
})

const emit = defineEmits(['update:modelValue', 'change'])

const modelValue = ref(props.modelValue)
watch(() => props.modelValue, val => { modelValue.value = val })
watch(modelValue, val => emit('update:modelValue', val))

const componentMap = {
  select: 'el-select',
  radio: 'el-radio-group',
  input: 'el-input',
  'input-number': 'el-input-number'
}
const currentComponent = computed(() => componentMap[props.type] || 'el-input')
const isSelectLike = computed(() => ['select', 'radio'].includes(props.type))

const selectOptions = computed(() => props.options || [])

const componentProps = computed(() => {
  const base = { placeholder: props.placeholder }
  if (props.type === 'input-number') {
    base.min = props.min
    base.max = props.max
    base.step = props.step
  }
  return base
})

function onChange(val) {
  emit('change', val)
}
</script>

<style scoped>
.item-box {
  width: 100%;
}
</style>