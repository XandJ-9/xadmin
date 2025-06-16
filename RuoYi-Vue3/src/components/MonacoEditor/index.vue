<template>
  <div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script setup>
import * as monaco from 'monaco-editor'
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

// 配置Monaco Editor支持的语言
const configureLanguages = () => {
  // 配置JavaScript语言特性
  monaco.languages.typescript.javascriptDefaults.setDiagnosticsOptions({
    noSemanticValidation: false,
    noSyntaxValidation: false,
  })
  monaco.languages.typescript.javascriptDefaults.setCompilerOptions({
    target: monaco.languages.typescript.ScriptTarget.ES2020,
    allowNonTsExtensions: true
  })

  // 配置TypeScript语言特性
  monaco.languages.typescript.typescriptDefaults.setDiagnosticsOptions({
    noSemanticValidation: false,
    noSyntaxValidation: false,
  })
  monaco.languages.typescript.typescriptDefaults.setCompilerOptions({
    target: monaco.languages.typescript.ScriptTarget.ES2020,
    allowNonTsExtensions: true
  })

  // 配置SQL语言特性
  monaco.languages.registerCompletionItemProvider('sql', {
    provideCompletionItems: () => ({
      suggestions: [
        {
          label: 'SELECT',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'SELECT',
        },
        {
          label: 'FROM',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'FROM',
        },
        {
          label: 'WHERE',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'WHERE',
        },
        {
          label: 'GROUP BY',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'GROUP BY',
        },
        {
          label: 'ORDER BY',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'ORDER BY',
        },
        {
          label: 'HAVING',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'HAVING',
        },
        {
          label: 'JOIN',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'JOIN',
        },
        {
          label: 'LEFT JOIN',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'LEFT JOIN',
        },
        {
          label: 'RIGHT JOIN',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'RIGHT JOIN',
        },
        {
          label: 'INNER JOIN',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'INNER JOIN',
        },
        {
          label: 'LIMIT',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'LIMIT',
        },
        {
          label: 'OFFSET',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'OFFSET',
        },
        {
          label: 'INSERT INTO',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'INSERT INTO',
        },
        {
          label: 'UPDATE',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'UPDATE',
        },
        {
          label: 'DELETE FROM',
          kind: monaco.languages.CompletionItemKind.Keyword,
          insertText: 'DELETE FROM',
        },
      ],
    }),
  })
}

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'javascript'
  },
  theme: {
    type: String,
    default: 'vs-dark'
  },
  options: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'cursor-change'])

const editorContainer = ref(null)
let editor = null

onMounted(() => {
    configureLanguages()
    initMonaco()
})

onBeforeUnmount(() => {
  if (editor) {
    editor.dispose()
  }
})

const initMonaco = () => {

  const defaultOptions = {
    value: props.modelValue,
    language: props.language,
    theme: props.theme,
    automaticLayout: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    fontSize: 14,
    tabSize: 2,
    lineHeight: 22,
    padding: { top: 8, bottom: 8 },
    scrollbar: {
      vertical: 'visible',
      horizontal: 'visible',
      useShadows: false,
      verticalScrollbarSize: 8,
      horizontalScrollbarSize: 8
    },
    renderLineHighlight: 'all',
    roundedSelection: false,
    selectOnLineNumbers: true,
    wordWrap: 'on',
    // 性能优化配置
    quickSuggestions: {
      other: true,
      comments: false,
      strings: false
    },
    acceptSuggestionOnCommitCharacter: true,
    suggestOnTriggerCharacters: true,
    wordBasedSuggestions: true,
    parameterHints: {
      enabled: true
    },
    renderWhitespace: 'none',
    renderControlCharacters: false,
    // 大文件性能优化
    largeFileOptimizations: true,
    maxTokenizationLineLength: 20000
  }

  editor = monaco.editor.create(editorContainer.value, {
    ...defaultOptions,
    ...props.options
  })



  editor.onDidChangeModelContent(() => {
    const value = editor.getValue()
    emit('update:modelValue', value)
    emit('change', value)
  })

  editor.onDidChangeCursorPosition((e) => {
    const position = editor.getPosition()
    emit('cursor-change', position)
    // console.log('光标位置变化：', position)
  })

  
}

watch(() => props.modelValue, (newValue) => {
  if (editor && newValue !== editor.getValue()) {
    editor.setValue(newValue)
  }
})

watch(() => props.language, (newValue) => {
  if (editor) {
    const model = editor.getModel()
    if (model) {
      monaco.editor.setModelLanguage(model, newValue)
    }
  }
})

watch(() => props.theme, (newValue) => {
  if (editor) {
    monaco.editor.setTheme(newValue)
  }
})
</script>

<style scoped>
.monaco-editor-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  background-color: #1e1e1e;
}

:deep(.monaco-editor) {
  padding: 0px 0;
}

/* :deep(.monaco-editor .margin) {
  background-color: #1e1e1e;
} */

:deep(.monaco-editor .monaco-scrollable-element) {
  padding: 0;
}
</style>