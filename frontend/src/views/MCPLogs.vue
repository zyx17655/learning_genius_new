<template>
  <div>
    <main class="p-4">
      <!-- 统一标题区域 -->
      <section class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-800 mb-1">MCP服务</h1>
            <p class="text-sm text-slate-500">智能题库MCP服务 - 为外部AI系统提供智能出题能力</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-2 px-3 py-1.5 rounded-full text-sm" :class="serviceStatus === 'running' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'">
              <span class="w-2 h-2 rounded-full" :class="serviceStatus === 'running' ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'"></span>
              {{ serviceStatus === 'running' ? '服务运行中' : '服务已停止' }}
            </div>
            <button class="btn bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-sm" @click="checkServiceStatus">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              刷新状态
            </button>
          </div>
        </div>
      </section>

      <!-- 服务信息 -->
      <section class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h3 class="text-base font-semibold text-slate-800 mb-4">服务信息</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="bg-slate-50 rounded-lg p-4">
            <div class="text-xs text-slate-500 mb-1">服务地址</div>
            <div class="text-sm font-mono text-slate-700 break-all">{{ serviceUrl }}</div>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <div class="text-xs text-slate-500 mb-1">服务端口</div>
            <div class="text-sm font-mono text-slate-700">8765</div>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <div class="text-xs text-slate-500 mb-1">协议版本</div>
            <div class="text-sm text-slate-700">MCP 1.0</div>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <div class="text-xs text-slate-500 mb-1">运行状态</div>
            <div class="text-sm" :class="serviceStatus === 'running' ? 'text-emerald-600' : 'text-red-600'">
              {{ serviceStatus === 'running' ? '正常运行' : '已停止' }}
            </div>
          </div>
        </div>
      </section>

      <!-- 统计数据区域 -->
      <section class="bg-slate-800 rounded-xl shadow-sm border border-slate-700 p-6 mb-6">
        <div class="flex items-center justify-between mb-5">
          <h3 class="text-base font-semibold text-white">调用概览</h3>
          <span class="text-xs text-slate-400">MCP服务状态监控</span>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-lg bg-slate-700 flex items-center justify-center border border-slate-600 shadow-inner">
              <svg class="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm3 10.5a.75.75 0 000-1.5H9a.75.75 0 000 1.5h6z"/>
              </svg>
            </div>
            <div>
              <div class="text-xl font-bold text-white">{{ stats.total_calls }}</div>
              <div class="text-xs text-slate-400">总调用次数</div>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-lg bg-slate-700 flex items-center justify-center border border-slate-600 shadow-inner">
              <svg class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm1.313 14.25a1.125 1.125 0 11-2.25 0 1.125 1.125 0 012.25 0zm-6.428-4.334a.75.75 0 001.06 0l3-3a.75.75 0 10-1.06-1.06l-2.47 2.47V6a.75.75 0 00-1.5 0v3.793l-2.47-2.47a.75.75 0 10-1.06 1.06l3 3z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div>
              <div class="text-xl font-bold text-white">{{ stats.completed_calls }}</div>
              <div class="text-xs text-slate-400">成功次数</div>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-lg bg-slate-700 flex items-center justify-center border border-slate-600 shadow-inner">
              <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm4.28 10.28a.75.75 0 010 1.06l-3 3a.75.75 0 11-1.06-1.06l3-3a.75.75 0 011.06 0zm0-7.5a.75.75 0 010 1.06l-3 3a.75.75 0 11-1.06-1.06l3-3a.75.75 0 011.06 0z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div>
              <div class="text-xl font-bold text-white">{{ stats.failed_calls }}</div>
              <div class="text-xs text-slate-400">失败次数</div>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-lg bg-slate-700 flex items-center justify-center border border-slate-600 shadow-inner">
              <svg class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-2.625 6c-.54 0-.828.419-.936.634a1.96 1.96 0 00-.189.866c0 .298.059.605.189.866.108.215.395.634.936.634.54 0 .828-.419.936-.634.13-.26.189-.568.189-.866 0-.298-.059-.605-.189-.866-.108-.215-.395-.634-.936-.634zm4.314.634c.108-.215.395-.634.936-.634.54 0 .828.419.936.634.13.26.189.568.189.866 0 .298-.059.605-.189.866a1.96 1.96 0 01-.189.866c-.108.215-.395.634-.936.634-.54 0-.828-.419-.936-.634a1.96 1.96 0 01-.189-.866c0-.298.059-.605.189-.866.108-.215.395-.634.936-.634zm-3 9a.75.75 0 100-1.5.75.75 0 000 1.5z" clip-rule="evenodd"/>
              </svg>
            </div>
            <div>
              <div class="text-xl font-bold text-white">{{ stats.avg_duration_ms }}ms</div>
              <div class="text-xs text-slate-400">平均耗时</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 接口文档 -->
      <section class="bg-white rounded-xl shadow-sm border border-slate-200 mb-6 overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50">
          <h3 class="text-base font-semibold text-slate-800">接口文档</h3>
        </div>
        <div class="p-6">
          <div class="mb-6">
            <div class="flex items-center gap-2 mb-3">
              <span class="px-2 py-1 rounded text-xs font-bold bg-emerald-100 text-emerald-700">POST</span>
              <code class="text-sm font-mono text-slate-700">/mcp/generate_questions</code>
            </div>
            <p class="text-sm text-slate-600 mb-4">根据知识素材和规则生成高质量考试题目</p>
            
            <div class="bg-slate-800 rounded-lg p-4 mb-4">
              <div class="text-xs text-slate-400 mb-2">请求参数</div>
              <pre class="text-sm text-slate-200 overflow-x-auto">{{ requestExample }}</pre>
            </div>

            <div class="overflow-x-auto">
              <table class="table table-sm w-full">
                <thead>
                  <tr class="bg-slate-50">
                    <th class="text-xs text-slate-500">参数名</th>
                    <th class="text-xs text-slate-500">类型</th>
                    <th class="text-xs text-slate-500">必填</th>
                    <th class="text-xs text-slate-500">说明</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="border-b border-slate-100">
                    <td class="text-sm font-mono text-slate-700">knowledge_input</td>
                    <td class="text-sm text-slate-600">string</td>
                    <td><span class="text-xs text-red-500">是</span></td>
                    <td class="text-sm text-slate-600">知识素材内容</td>
                  </tr>
                  <tr class="border-b border-slate-100">
                    <td class="text-sm font-mono text-slate-700">question_types</td>
                    <td class="text-sm text-slate-600">array[string]</td>
                    <td><span class="text-xs text-red-500">是</span></td>
                    <td class="text-sm text-slate-600">题型列表：单选、多选、判断、填空、主观</td>
                  </tr>
                  <tr class="border-b border-slate-100">
                    <td class="text-sm font-mono text-slate-700">type_counts</td>
                    <td class="text-sm text-slate-600">object</td>
                    <td><span class="text-xs text-red-500">是</span></td>
                    <td class="text-sm text-slate-600">各题型数量，如 {"单选": 5, "判断": 3}</td>
                  </tr>
                  <tr class="border-b border-slate-100">
                    <td class="text-sm font-mono text-slate-700">difficulty_config</td>
                    <td class="text-sm text-slate-600">object</td>
                    <td><span class="text-xs text-red-500">是</span></td>
                    <td class="text-sm text-slate-600">难度配置</td>
                  </tr>
                  <tr>
                    <td class="text-sm font-mono text-slate-700">rule_id</td>
                    <td class="text-sm text-slate-600">integer</td>
                    <td><span class="text-xs text-slate-400">否</span></td>
                    <td class="text-sm text-slate-600">自定义规则ID，不传则使用默认规则</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- 调用日志 -->
      <section class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <h3 class="text-base font-semibold text-slate-800">调用日志</h3>
          <select v-model="filterStatus" class="select select-bordered bg-white select-sm" @change="loadLogs">
            <option value="">全部状态</option>
            <option value="completed">成功</option>
            <option value="failed">失败</option>
          </select>
        </div>
        
        <table class="table w-full">
          <thead class="bg-slate-50 border-b border-slate-200">
            <tr>
              <th class="text-slate-500 font-medium text-xs">ID</th>
              <th class="text-slate-500 font-medium text-xs">调用时间</th>
              <th class="text-slate-500 font-medium text-xs">状态</th>
              <th class="text-slate-500 font-medium text-xs">耗时</th>
              <th class="text-slate-500 font-medium text-xs">请求参数</th>
              <th class="text-slate-500 font-medium text-xs">错误信息</th>
              <th class="text-slate-500 font-medium text-xs">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id" class="hover:bg-slate-50 border-b border-slate-100">
              <td class="font-mono text-sm text-slate-600">{{ log.id }}</td>
              <td class="text-sm text-slate-600">{{ log.created_at }}</td>
              <td>
                <span :class="['px-2 py-1 rounded-full text-xs font-medium', log.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700']">
                  {{ log.status === 'completed' ? '成功' : '失败' }}
                </span>
              </td>
              <td class="text-sm text-slate-600">{{ log.duration_ms }}ms</td>
              <td class="text-sm text-slate-600 max-w-[200px] truncate">
                {{ formatRequestParams(log.request_params) }}
              </td>
              <td class="text-sm text-red-500 max-w-[150px] truncate" v-if="log.error_message">
                {{ log.error_message }}
              </td>
              <td class="text-sm text-slate-400" v-else>-</td>
              <td>
                <button class="btn btn-xs btn-ghost text-slate-600 hover:bg-slate-100" @click="showDetail(log)">查看详情</button>
              </td>
            </tr>
            <tr v-if="logs.length === 0">
              <td colspan="7" class="text-center py-12 text-slate-400">
                <svg class="w-12 h-12 mx-auto mb-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                暂无调用记录
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div v-if="total > perPage" class="flex items-center justify-between p-4 border-t border-slate-200">
          <div class="text-sm text-slate-500">
            第 {{ (page - 1) * perPage + 1 }} - {{ Math.min(page * perPage, total) }} 条，共 {{ total }} 条
          </div>
          <div class="join">
            <button class="join-item btn btn-sm bg-white border-slate-200" :disabled="page <= 1" @click="page--; loadLogs()">上一页</button>
            <button class="join-item btn btn-sm bg-white border-slate-200">{{ page }} / {{ totalPages }}</button>
            <button class="join-item btn btn-sm bg-white border-slate-200" :disabled="page >= totalPages" @click="page++; loadLogs()">下一页</button>
          </div>
        </div>
      </section>
    </main>

    <!-- 详情弹窗 -->
    <div class="modal modal-open" v-if="showDetailModal">
      <div class="modal-box w-11/12 max-w-4xl bg-white">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-200">
          <h3 class="text-lg font-bold text-slate-800">调用详情</h3>
          <button class="btn btn-sm btn-circle btn-ghost" @click="showDetailModal = false">✕</button>
        </div>
        
        <div v-if="currentLog" class="space-y-4">
          <!-- 基本信息 -->
          <div class="bg-slate-50 rounded-lg p-4">
            <h4 class="text-sm font-semibold text-slate-700 mb-3">基本信息</h4>
            <div class="grid grid-cols-4 gap-4">
              <div>
                <span class="text-xs text-slate-500">日志ID</span>
                <div class="font-mono text-sm text-slate-700">{{ currentLog.id }}</div>
              </div>
              <div>
                <span class="text-xs text-slate-500">状态</span>
                <div>
                  <span :class="['px-2 py-1 rounded-full text-xs font-medium', currentLog.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700']">
                    {{ currentLog.status === 'completed' ? '成功' : '失败' }}
                  </span>
                </div>
              </div>
              <div>
                <span class="text-xs text-slate-500">耗时</span>
                <div class="text-sm text-slate-700">{{ currentLog.duration_ms }}ms</div>
              </div>
              <div>
                <span class="text-xs text-slate-500">调用时间</span>
                <div class="text-sm text-slate-700">{{ currentLog.created_at }}</div>
              </div>
            </div>
          </div>

          <!-- 错误信息 -->
          <div v-if="currentLog.error_message" class="bg-red-50 rounded-lg p-4 border border-red-200">
            <h4 class="text-sm font-semibold text-red-700 mb-2">错误信息</h4>
            <pre class="text-sm text-red-600 whitespace-pre-wrap">{{ currentLog.error_message }}</pre>
          </div>

          <!-- 请求参数 -->
          <div class="bg-slate-50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-sm font-semibold text-slate-700">请求参数</h4>
              <button class="btn btn-xs btn-ghost text-slate-500 hover:text-slate-700 hover:bg-slate-200" @click="copyToClipboard(JSON.stringify(currentLog.request_params, null, 2), '请求参数')">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                复制
              </button>
            </div>
            <pre class="text-sm text-white bg-slate-800 p-3 rounded-lg overflow-x-auto max-h-60 overflow-y-auto">{{ JSON.stringify(currentLog.request_params, null, 2) }}</pre>
          </div>

          <!-- 响应结果 -->
          <div v-if="currentLog.response_result" class="bg-slate-50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-sm font-semibold text-slate-700">响应结果</h4>
              <button class="btn btn-xs btn-ghost text-slate-500 hover:text-slate-700 hover:bg-slate-200" @click="copyToClipboard(JSON.stringify(currentLog.response_result, null, 2), '响应结果')">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                复制
              </button>
            </div>
            <pre class="text-sm text-white bg-slate-800 p-3 rounded-lg overflow-x-auto max-h-60 overflow-y-auto">{{ JSON.stringify(currentLog.response_result, null, 2) }}</pre>
          </div>
        </div>

        <div class="modal-action">
          <button class="btn bg-slate-700 hover:bg-slate-600 border-0 text-white" @click="showDetailModal = false">关闭</button>
        </div>
      </div>
      <div class="modal-backdrop bg-black/50" @click="showDetailModal = false"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MCPLogs',
  data() {
    return {
      serviceStatus: 'unknown',
      serviceUrl: window.location.origin + ':8765',
      logs: [],
      stats: {
        total_calls: 0,
        completed_calls: 0,
        failed_calls: 0,
        avg_duration_ms: 0
      },
      page: 1,
      perPage: 20,
      total: 0,
      filterStatus: '',
      showDetailModal: false,
      currentLog: null,
      requestExample: `{
  "knowledge_input": "Python基础语法：变量、数据类型...",
  "question_types": ["单选", "判断"],
  "type_counts": {"单选": 5, "判断": 3},
  "difficulty_config": {
    "简单": {"count": 5, "percent": 62},
    "中等": {"count": 3, "percent": 38}
  },
  "rule_id": 1
}`
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.total / this.perPage)
    }
  },
  mounted() {
    this.checkServiceStatus()
    this.loadStats()
    this.loadLogs()
  },
  methods: {
    async checkServiceStatus() {
      try {
        const response = await fetch('http://localhost:8765/health')
        if (response.ok) {
          this.serviceStatus = 'running'
        } else {
          this.serviceStatus = 'stopped'
        }
      } catch (error) {
        this.serviceStatus = 'stopped'
      }
    },
    async loadStats() {
      try {
        const response = await this.$axios.get('/mcp/stats')
        if (response.code === 0) {
          this.stats = response.data
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }
    },
    async loadLogs() {
      try {
        const params = {
          page: this.page,
          per_page: this.perPage
        }
        if (this.filterStatus) {
          params.status = this.filterStatus
        }
        const response = await this.$axios.get('/mcp/logs', { params })
        if (response.code === 0) {
          this.logs = response.data.logs
          this.total = response.data.total
        }
      } catch (error) {
        console.error('加载日志失败:', error)
      }
    },
    formatRequestParams(params) {
      try {
        const obj = typeof params === 'string' ? JSON.parse(params) : params
        const types = obj.question_types ? obj.question_types.join(', ') : ''
        const counts = obj.type_counts ? JSON.stringify(obj.type_counts) : ''
        return `题型: ${types} | 数量: ${counts}`
      } catch {
        return String(params).substring(0, 50)
      }
    },
    showDetail(log) {
      try {
        this.currentLog = {
          ...log,
          request_params: typeof log.request_params === 'string' ? JSON.parse(log.request_params) : log.request_params,
          response_result: log.response_result ? (typeof log.response_result === 'string' ? JSON.parse(log.response_result) : log.response_result) : null
        }
        this.showDetailModal = true
      } catch (error) {
        console.error('解析日志详情失败:', error)
        this.currentLog = log
        this.showDetailModal = true
      }
    },
    async copyToClipboard(text, label = '内容') {
      try {
        await navigator.clipboard.writeText(text)
        this.$toast && this.$toast.success(`${label}已复制到剪贴板`)
        alert(`${label}已复制到剪贴板`)
      } catch (error) {
        console.error('复制失败:', error)
        const textarea = document.createElement('textarea')
        textarea.value = text
        textarea.style.position = 'fixed'
        textarea.style.left = '-9999px'
        document.body.appendChild(textarea)
        textarea.select()
        try {
          document.execCommand('copy')
          alert(`${label}已复制到剪贴板`)
        } catch (e) {
          alert('复制失败，请手动复制')
        }
        document.body.removeChild(textarea)
      }
    }
  }
}
</script>
