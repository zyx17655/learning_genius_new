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
  computed: {
    renderedContent() {
      if (!this.content) return ''
      
      let result = this.content.toString()
      
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
