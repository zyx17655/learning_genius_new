import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/tailwind.css'
import './assets/styles/global.less'
import './assets/styles/design-system.less'
import VueRouter from 'vue-router'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/pie'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import axios from './api/axios'
import LatexRenderer from './components/LatexRenderer.vue'

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.component('el-chart', ECharts)
Vue.component('latex-renderer', LatexRenderer)
Vue.prototype.$axios = axios

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./views/Home.vue'),
    meta: { title: '题库管理', navIndex: 0 }
  },
  {
    path: '/rules',
    name: 'RuleManagement',
    component: () => import('./views/RuleManagement.vue'),
    meta: { title: '规则管理', navIndex: 1 }
  },
  {
    path: '/question-bank',
    name: 'QuestionBank',
    component: () => import('./views/QuestionBank.vue'),
    meta: { title: '题库管理', navIndex: 0 }
  },
  {
    path: '/ai-generate',
    name: 'AIGenerate',
    component: () => import('./views/AIGenerate.vue'),
    meta: { title: 'AI生成', navIndex: 2 }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('./views/Analysis.vue'),
    meta: { title: '数据分析', navIndex: 3 }
  },
  {
    path: '/question-compare',
    name: 'QuestionCompare',
    component: () => import('./views/QuestionCompare.vue'),
    meta: { title: '题目对比', navIndex: 4 }
  },
  {
    path: '/mcp-logs',
    name: 'MCPLogs',
    component: () => import('./views/MCPLogs.vue'),
    meta: { title: 'MCP日志', navIndex: 5 }
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta && to.meta.title) {
    document.title = to.meta.title + ' - 智能教学系统'
  }
  next()
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
