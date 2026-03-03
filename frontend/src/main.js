import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/tailwind.css'
import VueRouter from 'vue-router'
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/pie'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import axios from './api/axios'

Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.component('el-chart', ECharts)
Vue.prototype.$axios = axios

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./views/Home.vue')
  },
  {
    path: '/question-bank',
    name: 'QuestionBank',
    component: () => import('./views/QuestionBank.vue')
  },
  {
    path: '/ai-generate',
    name: 'AIGenerate',
    component: () => import('./views/AIGenerate.vue')
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('./views/Analysis.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')