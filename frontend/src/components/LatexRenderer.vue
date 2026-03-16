<template>
  <span class="latex-content" v-html="renderedContent"></span>
</template>

<script>
import katex from 'katex'
import 'katex/dist/katex.min.css'

export default {
  name: 'LatexRenderer',
  props: {
    content: {
      type: String,
      default: ''
    }
  },
  methods: {
    /**
     * 预处理 LaTeX 内容，修复常见的格式问题
     */
    preprocessLatex(text) {
      if (!text || typeof text !== 'string') return text
      
      let result = text
      
      // 1. 通用修复：所有双反斜杠后跟字母或下划线开头的命令，改为单反斜杠
      // 匹配 \\ 后跟字母或下划线开头的字符序列
      result = result.replace(/\\\\([a-zA-Z_][a-zA-Z0-9_]*)(?![a-zA-Z])/g, '\\$1')
      
      // 2. 额外修复：括号相关的命令（确保覆盖所有情况）
      const bracketCommands = [
        'big', 'Big', 'bigg', 'Bigg',
        'bigl', 'bigr', 'Bigl', 'Bigr', 'biggl', 'biggr', 'Biggl', 'Biggr',
        'bigm', 'Bigm', 'biggm', 'Biggm'
      ]
      for (const cmd of bracketCommands) {
        result = result.replace(new RegExp('\\\\\\\\' + cmd.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '\\' + cmd)
      }
      
      // 3. 修复空格命令
      const spaceCommands = [' ', ',', ';', '!', 'quad', 'qquad', 'thinspace', 'thickspace', 'medspace', 'negthinspace']
      for (const cmd of spaceCommands) {
        result = result.replace(new RegExp('\\\\\\\\' + cmd.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '\\' + cmd)
      }
      
      // 4. 修复旧版 {\rm ...} 格式为 \mathrm{...}
      // 先处理带花括号的: {\rm A} -> \mathrm{A}
      result = result.replace(/\{\\rm\s+([^}]+)\}/g, '\\mathrm{$1}')
      // 再处理不带花括号的（在数学模式内）: \rm A -> \mathrm{A}
      result = result.replace(/\\rm\s+([a-zA-Z0-9_]+)/g, '\\mathrm{$1}')
      
      return result
    }
  },
  computed: {
    renderedContent() {
      if (!this.content) return ''
      
      // 预处理 LaTeX 内容
      let result = this.preprocessLatex(this.content.toString())
      
      // 处理 $$...$$ 块级公式
      result = result.replace(/\$\$([^$]+)\$\$/g, (match, latex) => {
        try {
          return `<div class="latex-block">${katex.renderToString(latex, {
            throwOnError: false,
            displayMode: true
          })}</div>`
        } catch (e) {
          console.error('KaTeX render error:', e)
          return match
        }
      })
      
      // 处理 $...$ 行内公式
      result = result.replace(/\$([^$]+)\$/g, (match, latex) => {
        try {
          return katex.renderToString(latex, {
            throwOnError: false,
            displayMode: false
          })
        } catch (e) {
          console.error('KaTeX render error:', e)
          return match
        }
      })
      
      return result
    }
  }
}
</script>

<style scoped>
.latex-content {
  display: inline;
}
.latex-content :deep(.katex) {
  white-space: nowrap;
}
.latex-content :deep(.katex-html) {
  white-space: nowrap;
}
.latex-content :deep(.katex .base) {
  white-space: nowrap;
}
.latex-content :deep(.latex-block) {
  display: block;
  text-align: center;
  margin: 0.5em 0;
  overflow-x: auto;
  overflow-y: hidden;
}
.latex-content :deep(.latex-block .katex) {
  white-space: normal;
}
</style>
