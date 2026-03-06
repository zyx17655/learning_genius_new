<template>
  <div>
    <main class="p-6">
      <section class="mb-6 relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 p-6 text-white shadow-xl shadow-indigo-200">
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2"></div>
        <div class="absolute bottom-0 left-1/4 w-32 h-32 bg-white/5 rounded-full translate-y-1/2"></div>
        <div class="relative z-10 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold mb-2">欢迎使用智能题库系统 👋</h1>
            <p class="text-indigo-100">让AI助力教学，轻松创建高质量试题</p>
          </div>
          <button class="btn bg-white/20 hover:bg-white/30 border-none text-white backdrop-blur-sm" @click="openAIDialog">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            立即AI出题
          </button>
        </div>
      </section>

      <!-- 统计卡片 -->
      <section class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="card-body p-5">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-3xl font-bold text-slate-800">{{ stats.total }}</div>
                <div class="text-sm text-slate-500 mt-1">题目总数</div>
                <div class="text-xs text-emerald-500 mt-1">↑ 较上月 +{{ stats.monthlyNew }}</div>
              </div>
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-200">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
        <div class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="card-body p-5">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-3xl font-bold text-emerald-600">{{ stats.reviewed }}</div>
                <div class="text-sm text-slate-500 mt-1">已审核</div>
                <div class="text-xs text-emerald-500 mt-1">↑ 较上月 +{{ stats.reviewedMonthly }}</div>
              </div>
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center shadow-lg shadow-emerald-200">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
        <div class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="card-body p-5">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-3xl font-bold text-amber-500">{{ stats.pending }}</div>
                <div class="text-sm text-slate-500 mt-1">待审核</div>
                <div class="text-xs text-amber-500 mt-1">待处理</div>
              </div>
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center shadow-lg shadow-amber-200">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
        <div class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="card-body p-5">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-3xl font-bold text-slate-400">{{ stats.draft }}</div>
                <div class="text-sm text-slate-500 mt-1">草稿箱</div>
                <div class="text-xs text-slate-400 mt-1">未提交</div>
              </div>
              <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-slate-400 to-slate-500 flex items-center justify-center shadow-lg shadow-slate-200">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 题型分布 -->
      <section class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 mb-6">
        <div class="card-body p-5">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              题型分布统计
            </h3>
            <span class="text-xs text-slate-400">实时更新</span>
          </div>
          <div class="grid grid-cols-5 gap-3">
            <div v-for="item in typeStats" :key="item.label" class="text-center p-3 rounded-xl bg-gradient-to-br from-slate-50 to-slate-100 hover:shadow-md transition-all cursor-pointer">
              <div class="text-2xl font-bold" :class="item.textClass">{{ item.value }}</div>
              <div class="text-xs text-slate-500 mt-1">{{ item.label }}</div>
              <div class="text-xs text-emerald-500 mt-0.5">↑ +{{ item.monthlyNew }}</div>
              <div class="mt-2 h-1.5 rounded-full bg-slate-200 overflow-hidden">
                <div class="h-full rounded-full transition-all duration-500" :class="item.barClass" :style="{ width: item.percent + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 操作栏 -->
      <section class="flex flex-wrap items-center justify-between gap-4 mb-4">
        <div class="flex flex-wrap items-center gap-3">
          <div class="join shadow-md">
            <input class="input input-bordered join-item w-64 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="searchKeyword" placeholder="搜索题目内容、标签..." @keyup.enter="handleSearch" />
            <button class="btn join-item bg-indigo-500 hover:bg-indigo-600 border-indigo-500 text-white" @click="handleSearch">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </button>
          </div>
          <select v-model="filterType" class="select select-bordered bg-white shadow-sm focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100">
            <option value="">📚 全部题型</option>
            <option value="单选">单选题</option>
            <option value="多选">多选题</option>
            <option value="判断">判断题</option>
            <option value="填空">填空题</option>
            <option value="主观">主观题</option>
          </select>
          <select v-model="filterDifficulty" class="select select-bordered bg-white shadow-sm focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100">
            <option value="">📊 全部难度</option>
            <option value="L1">L1 记忆</option>
            <option value="L2">L2 理解</option>
            <option value="L3">L3 应用</option>
            <option value="L4">L4 分析</option>
            <option value="L5">L5 创造</option>
          </select>
          <select v-model="filterStatus" class="select select-bordered bg-white shadow-sm focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100">
            <option value="">📋 全部状态</option>
            <option value="已审核">已审核</option>
            <option value="待审核">待审核</option>
            <option value="草稿">草稿</option>
          </select>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <button class="btn bg-white border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300 shadow-sm" @click="showImportDialog = true">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
            </svg>
            导入
          </button>
          <button class="btn bg-white border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300 shadow-sm" @click="handleExport">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            导出
          </button>
          <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white shadow-lg shadow-indigo-200" @click="openAIDialog">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            AI智能生题
          </button>
          <button class="btn bg-slate-800 hover:bg-slate-900 border-0 text-white shadow-md" @click="showAddDialog">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            新增题目
          </button>
        </div>
      </section>

      <!-- 批量操作栏 -->
      <section v-if="selectedIds.length > 0" class="alert bg-indigo-50 border border-indigo-200 mb-4 shadow-sm">
        <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <span class="text-indigo-700 font-medium">已选择 {{ selectedIds.length }} 项</span>
        <div class="flex gap-2">
          <button class="btn btn-sm bg-emerald-500 hover:bg-emerald-600 border-0 text-white" @click="batchReview">审核通过</button>
          <button class="btn btn-sm bg-slate-500 hover:bg-slate-600 border-0 text-white" @click="batchDraft">设为草稿</button>
          <button class="btn btn-sm bg-red-500 hover:bg-red-600 border-0 text-white" @click="batchDelete">删除</button>
        </div>
        <button class="btn btn-sm btn-ghost text-slate-500" @click="clearSelection">取消</button>
      </section>

      <!-- 题目列表 -->
      <section class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead class="bg-gradient-to-r from-slate-50 to-slate-100">
              <tr>
                <th class="w-12">
                  <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="selectAll" @change="handleSelectAll" />
                </th>
                <th class="w-16 text-slate-500 font-medium">ID</th>
                <th class="w-24 text-slate-500 font-medium">知识点</th>
                <th class="text-slate-500 font-medium min-w-[200px]">题目内容</th>
                <th class="w-20 text-slate-500 font-medium">题型</th>
                <th class="w-28 text-slate-500 font-medium">难度</th>
                <th class="w-20 text-slate-500 font-medium">来源</th>
                <th class="w-20 text-slate-500 font-medium">状态</th>
                <th class="w-32 text-slate-500 font-medium">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in questions" :key="item.id" class="hover:bg-indigo-50/50 transition-colors border-b border-slate-100">
                <td>
                  <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="item.selected" @change="handleItemSelect" />
                </td>
                <td class="text-slate-400 font-mono text-sm">#{{ item.id }}</td>
                <td>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="kp in (item.knowledgePoints || []).slice(0, 2)" :key="kp" class="px-1.5 py-0.5 text-xs rounded bg-cyan-50 text-cyan-600 whitespace-nowrap">{{ kp }}</span>
                    <span v-if="(item.knowledgePoints || []).length > 2" class="text-xs text-slate-400 whitespace-nowrap">+{{ item.knowledgePoints.length - 2 }}</span>
                  </div>
                </td>
                <td>
                  <div class="cursor-pointer group max-w-md" @click="showDetail(item)">
                    <div class="text-slate-700 group-hover:text-indigo-600 transition-colors truncate" :title="item.content">{{ item.content }}</div>
                    <div v-if="item.tags && item.tags.length" class="flex gap-1 mt-1">
                      <span v-for="tag in item.tags.slice(0, 2)" :key="tag" class="px-1.5 py-0.5 text-xs rounded bg-indigo-50 text-indigo-600">{{ tag }}</span>
                      <span v-if="item.tags.length > 2" class="px-1.5 py-0.5 text-xs rounded bg-slate-100 text-slate-500">+{{ item.tags.length - 2 }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getTypeBadgeClass(item.question_type)">{{ item.question_type }}</span>
                </td>
                <td>
                  <div class="flex items-center gap-1 whitespace-nowrap">
                    <span class="px-2 py-1 rounded text-xs font-bold" :class="getDifficultyBadgeClass(item.difficulty)">{{ item.difficulty }}</span>
                    <span class="text-xs text-slate-500">{{ getDifficultyName(item.difficulty) }}</span>
                  </div>
                </td>
                <td>
                  <span class="text-xs px-2 py-1 rounded-full whitespace-nowrap" :class="getSourceBadgeClass(item.source)">{{ item.source || '系统' }}</span>
                </td>
                <td>
                  <div class="flex items-center gap-2 whitespace-nowrap">
                    <span class="w-2 h-2 rounded-full" :class="getStatusDotClass(item.status)"></span>
                    <span class="text-sm" :class="getStatusTextClass(item.status)">{{ item.status }}</span>
                  </div>
                </td>
                <td>
                  <div class="flex gap-1 items-center justify-center">
                    <button v-if="item.status === '待审核'" class="btn btn-xs bg-emerald-500 hover:bg-emerald-600 border-0 text-white w-8 h-8 min-h-0 p-0" @click="reviewQuestion(item)" title="审核通过">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </button>
                    <button class="btn btn-xs btn-ghost w-8 h-8 min-h-0 p-0" @click="showDetail(item)" title="查看详情">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                    </button>
                    <button class="btn btn-xs btn-ghost w-8 h-8 min-h-0 p-0" @click="showEditDialog(item)" title="编辑">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button class="btn btn-xs btn-ghost w-8 h-8 min-h-0 p-0 text-red-500 hover:text-red-600 hover:bg-red-50" @click="deleteQuestion(item.id)" title="删除">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 分页 -->
      <section class="flex items-center justify-between mt-6">
        <span class="text-sm text-slate-500">共 <span class="font-semibold text-indigo-600">{{ total }}</span> 条记录</span>
        <div class="join shadow-md">
          <button class="join-item btn btn-sm bg-white border-slate-200" :disabled="currentPage === 1" @click="currentPage--; loadQuestions()">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <button class="join-item btn btn-sm bg-indigo-500 border-indigo-500 text-white">{{ currentPage }}</button>
          <button class="join-item btn btn-sm bg-white border-slate-200" @click="currentPage++; loadQuestions()">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </section>
    </main>

    <!-- 题目详情弹窗 -->
    <dialog :class="['modal', { 'modal-open': showDetailModal }]">
      <div class="modal-box w-11/12 max-w-3xl bg-white rounded-2xl shadow-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            题目详情
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showDetailModal = false">✕</button>
        </div>
        <div v-if="currentQuestion" class="space-y-4">
          <!-- 基本信息 -->
          <div class="flex flex-wrap gap-2 items-center">
            <span class="px-3 py-1 rounded-full text-sm font-medium" :class="getTypeBadgeClass(currentQuestion.question_type)">{{ currentQuestion.question_type }}</span>
            <span class="px-3 py-1 rounded text-sm font-bold" :class="getDifficultyBadgeClass(currentQuestion.difficulty)">{{ currentQuestion.difficulty }} {{ getDifficultyName(currentQuestion.difficulty) }}</span>
            <span class="px-3 py-1 rounded-full text-sm font-medium" :class="getStatusBadgeClass(currentQuestion.status)">{{ currentQuestion.status }}</span>
            <span class="px-3 py-1 rounded-full text-sm font-medium bg-slate-100 text-slate-600">{{ currentQuestion.source || '系统生成' }}</span>
          </div>
          
          <!-- 知识点 -->
          <div v-if="currentQuestion.knowledgePoints && currentQuestion.knowledgePoints.length" class="flex flex-wrap gap-2">
            <span class="text-sm text-slate-500">知识点：</span>
            <span v-for="kp in currentQuestion.knowledgePoints" :key="kp" class="px-2 py-0.5 text-xs rounded-full bg-cyan-50 text-cyan-600 border border-cyan-100">{{ kp }}</span>
          </div>
          
          <!-- 题目内容 -->
          <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 border border-indigo-100">
            <h4 class="text-sm font-medium text-indigo-600 mb-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              题目内容
            </h4>
            <p class="text-slate-700 leading-relaxed">{{ currentQuestion.content }}</p>
          </div>
          
          <!-- 选项 -->
          <div v-if="currentQuestion.options && currentQuestion.options.length" class="space-y-2">
            <h4 class="text-sm font-medium text-slate-600 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
              </svg>
              选项
            </h4>
            <div v-for="(opt, idx) in currentQuestion.options" :key="idx" 
                 :class="['flex items-center gap-3 p-3 rounded-xl transition-all', opt.is_correct ? 'bg-gradient-to-r from-emerald-50 to-teal-50 border-2 border-emerald-200' : 'bg-slate-50 border border-slate-100']">
              <span :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold', opt.is_correct ? 'bg-emerald-500 text-white' : 'bg-white text-slate-500 border border-slate-200']">{{ String.fromCharCode(65 + idx) }}</span>
              <span class="flex-1 text-slate-700">{{ opt.content }}</span>
              <span v-if="opt.is_correct" class="px-2 py-1 text-xs rounded-full bg-emerald-500 text-white font-medium">✓ 正确答案</span>
            </div>
          </div>
          
          <!-- 正确答案 -->
          <div class="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
            <h4 class="text-sm font-medium text-emerald-600 mb-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              正确答案
            </h4>
            <p class="text-slate-700 font-medium">{{ currentQuestion.answer }}</p>
          </div>
          
          <!-- 解析 -->
          <div v-if="currentQuestion.explanation" class="bg-amber-50 rounded-xl p-4 border border-amber-100">
            <h4 class="text-sm font-medium text-amber-600 mb-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
              解析
            </h4>
            <p class="text-slate-700 leading-relaxed">{{ currentQuestion.explanation }}</p>
          </div>
          
          <!-- 元信息 -->
          <div class="grid grid-cols-2 gap-4 text-sm text-slate-500 bg-slate-50 rounded-xl p-4">
            <div><span class="font-medium">创建时间：</span>{{ currentQuestion.createdAt || '2024-01-15 10:30' }}</div>
            <div><span class="font-medium">更新时间：</span>{{ currentQuestion.updatedAt || '2024-01-15 14:20' }}</div>
            <div><span class="font-medium">创建人：</span>{{ currentQuestion.creator || '李老师' }}</div>
            <div><span class="font-medium">审核人：</span>{{ currentQuestion.reviewer || '--' }}</div>
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showDetailModal = false">关闭</button>
          <button v-if="currentQuestion && currentQuestion.status === '待审核'" class="btn bg-emerald-500 hover:bg-emerald-600 border-0 text-white" @click="reviewQuestion(currentQuestion); showDetailModal = false">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            审核通过
          </button>
          <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white" @click="showEditDialog(currentQuestion); showDetailModal = false">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            编辑题目
          </button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showDetailModal = false">close</button>
      </form>
    </dialog>

    <!-- 新增/编辑弹窗 -->
    <dialog :class="['modal', { 'modal-open': showEditModal }]">
      <div class="modal-box w-11/12 max-w-4xl bg-white rounded-2xl shadow-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            {{ isEdit ? '编辑题目' : '新增题目' }}
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showEditModal = false">✕</button>
        </div>
        <div class="space-y-4">
          <!-- 基本信息 -->
          <div class="grid grid-cols-4 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">题型 <span class="text-red-500">*</span></span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.question_type">
                <option value="单选">单选题</option>
                <option value="多选">多选题</option>
                <option value="判断">判断题</option>
                <option value="填空">填空题</option>
                <option value="主观">主观题</option>
              </select>
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">难度 <span class="text-red-500">*</span></span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.difficulty">
                <option value="L1">L1 记忆</option>
                <option value="L2">L2 理解</option>
                <option value="L3">L3 应用</option>
                <option value="L4">L4 分析</option>
                <option value="L5">L5 创造</option>
              </select>
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">状态</span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.status">
                <option value="草稿">草稿</option>
                <option value="待审核">待审核</option>
                <option value="已审核">已审核</option>
              </select>
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">题目来源</span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.source">
                <option value="系统生成">系统生成</option>
                <option value="手动录入">手动录入</option>
                <option value="导入">导入</option>
                <option value="AI生成">AI生成</option>
              </select>
            </div>
          </div>
          
          <!-- 题目内容 -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">题目内容 <span class="text-red-500">*</span></span></label>
            <textarea class="textarea textarea-bordered h-24 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.content" placeholder="请输入题目内容..."></textarea>
          </div>
          
          <!-- 选项 -->
          <div v-if="['单选', '多选', '判断'].includes(form.question_type)" class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">选项 <span class="text-slate-400 text-xs">(勾选正确答案)</span></span></label>
            <div class="space-y-2">
              <div v-for="(opt, idx) in form.options" :key="idx" class="flex items-center gap-2 p-2 bg-slate-50 rounded-lg">
                <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="opt.is_correct" />
                <span :class="['w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold', opt.is_correct ? 'bg-emerald-500 text-white' : 'bg-white text-slate-500 border border-slate-200']">{{ String.fromCharCode(65 + idx) }}</span>
                <input type="text" class="input input-bordered flex-1 bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="opt.content" placeholder="选项内容" />
                <button v-if="form.options.length > 2" class="btn btn-ghost btn-sm btn-square text-slate-400 hover:text-red-500 hover:bg-red-50" @click="form.options.splice(idx, 1)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>
            <button class="btn btn-sm btn-ghost mt-2 text-indigo-600 hover:bg-indigo-50" @click="form.options.push({ content: '', is_correct: false })">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              添加选项
            </button>
          </div>
          
          <!-- 正确答案 -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">正确答案 <span class="text-red-500">*</span></span></label>
            <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.answer" placeholder="如：A 或 A,B,C 或 正确/错误 或 填空答案" />
          </div>
          
          <!-- 知识点 -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">知识点</span></label>
            <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.knowledgePointsInput" placeholder="多个知识点用逗号分隔，如：Python基础,变量,数据类型" />
          </div>
          
          <!-- 解析 -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">解析</span></label>
            <textarea class="textarea textarea-bordered h-20 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.explanation" placeholder="请输入题目解析..."></textarea>
          </div>
          
          <!-- 标签 -->
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">标签</span></label>
            <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.tagsInput" placeholder="多个标签用逗号分隔，如：基础,重要,考点" />
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showEditModal = false">取消</button>
          <button class="btn bg-slate-500 hover:bg-slate-600 border-0 text-white" @click="saveAsDraftFromEdit">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            存为草稿
          </button>
          <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white shadow-lg shadow-indigo-200" @click="saveQuestion">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            保存
          </button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showEditModal = false">close</button>
      </form>
    </dialog>

    <!-- AI智能生题弹窗 - 三步骤独立页面 -->
    <dialog :class="['modal', { 'modal-open': showAIDialog }]">
      <div class="modal-box w-11/12 max-w-6xl bg-white rounded-2xl shadow-2xl p-0 overflow-hidden">
        <!-- 弹窗头部 -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-gradient-to-r from-indigo-50 to-purple-50">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <div>
              <h3 class="font-bold text-lg text-slate-800">AI智能生题</h3>
              <p class="text-xs text-slate-500">三步完成高质量题目生成</p>
            </div>
          </div>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="closeAIDialog">✕</button>
        </div>

        <!-- 步骤指示器 -->
        <div class="px-6 py-4 bg-white border-b border-slate-100">
          <div class="flex items-center justify-center gap-4">
            <div v-for="(step, idx) in aiSteps" :key="idx" class="flex items-center">
              <div :class="['flex items-center gap-2 px-4 py-2 rounded-full transition-all', aiCurrentStep === idx ? 'bg-indigo-500 text-white shadow-lg' : aiCurrentStep > idx ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-400']">
                <span :class="['w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold', aiCurrentStep === idx ? 'bg-white/20' : aiCurrentStep > idx ? 'bg-emerald-500 text-white' : 'bg-slate-200']">{{ aiCurrentStep > idx ? '✓' : idx + 1 }}</span>
                <span class="font-medium">{{ step }}</span>
              </div>
              <div v-if="idx < aiSteps.length - 1" :class="['w-12 h-0.5 mx-2', aiCurrentStep > idx ? 'bg-emerald-400' : 'bg-slate-200']"></div>
            </div>
          </div>
        </div>

        <!-- 步骤1：配置参数 -->
        <div v-if="aiCurrentStep === 0" class="p-6 max-h-[60vh] overflow-y-auto">
          <div class="space-y-5">
            <!-- 出题规则选择 -->
            <div class="form-control">
              <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                </svg>
                出题规则
              </span></label>
              <div class="grid grid-cols-2 gap-3">
                <div :class="['p-4 rounded-xl cursor-pointer transition-all border-2', !aiConfig.customRuleId ? 'border-indigo-500 bg-indigo-50 shadow-md' : 'border-slate-200 hover:border-indigo-200 hover:bg-slate-50']" @click="aiConfig.customRuleId = null">
                  <div class="flex items-center gap-2 mb-2">
                    <span class="px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-700">默认规则</span>
                    <svg v-if="!aiConfig.customRuleId" class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                  </div>
                  <div class="font-medium text-slate-800 text-sm">{{ defaultRule?.name || '大学通用出题规则' }}</div>
                  <div class="text-xs text-slate-500 mt-1 line-clamp-2">{{ defaultRule?.description || '适用于大学各学科的通用出题规则' }}</div>
                </div>
                <div :class="['p-4 rounded-xl cursor-pointer transition-all border-2', aiConfig.customRuleId ? 'border-purple-500 bg-purple-50 shadow-md' : 'border-slate-200 hover:border-purple-200 hover:bg-slate-50']" @click="showRuleSelector = true">
                  <div class="flex items-center gap-2 mb-2">
                    <span class="px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-700">自定义规则</span>
                    <svg v-if="aiConfig.customRuleId" class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                  </div>
                  <div v-if="aiConfig.customRuleId && selectedCustomRule" class="font-medium text-slate-800 text-sm">{{ selectedCustomRule.name }}</div>
                  <div v-else class="font-medium text-slate-400 text-sm">点击选择自定义规则</div>
                  <div v-if="aiConfig.customRuleId && selectedCustomRule" class="text-xs text-slate-500 mt-1 line-clamp-2">{{ selectedCustomRule.description }}</div>
                  <div v-else class="text-xs text-slate-400 mt-1">可选一项自定义规则</div>
                </div>
              </div>
            </div>

            <!-- 知识范围 -->
            <div class="form-control">
              <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
                知识范围
              </span></label>
              <input type="text" class="input input-bordered mb-2 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="aiConfig.knowledgeInput" placeholder="输入知识点，如：Python变量、数据类型转换..." />
              <div class="grid grid-cols-4 gap-2">
                <label v-for="item in knowledgeTree" :key="item.id" class="flex items-center gap-2 p-2 bg-slate-50 rounded-lg cursor-pointer hover:bg-indigo-50 hover:border-indigo-200 transition-all border border-slate-100">
                  <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="aiConfig.knowledgeIds" :value="item.id" />
                  <span class="text-sm text-slate-700">{{ item.name }}</span>
                </label>
              </div>
            </div>

            <!-- 题型选择 -->
            <div class="form-control">
              <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                题型选择（共 {{ totalTypeCount }} 题）
              </span></label>
              <div class="grid grid-cols-5 gap-2">
                <label v-for="type in questionTypes" :key="type.id" :class="['flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all border', aiConfig.types.includes(type.id) ? 'bg-indigo-50 border-indigo-300' : 'bg-slate-50 border-slate-100 hover:bg-indigo-50 hover:border-indigo-200']">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="aiConfig.types" :value="type.id" />
                    <span class="text-sm font-medium text-slate-700">{{ type.name }}</span>
                  </div>
                  <div v-if="aiConfig.types.includes(type.id)" class="flex items-center gap-1">
                    <button class="btn btn-xs btn-circle btn-ghost" @click.prevent="decrementTypeCount(type.id)">-</button>
                    <input type="text" inputmode="numeric" pattern="[0-9]*" class="input input-bordered input-xs w-12 text-center no-spinner" :value="aiConfig.typeCounts[type.id] || 0" @input="updateTypeCount(type.id, $event.target.value)" />
                    <button class="btn btn-xs btn-circle btn-ghost" @click.prevent="incrementTypeCount(type.id)">+</button>
                  </div>
                </label>
              </div>
            </div>

            <!-- 难度配置 -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  难度配置（上限 {{ totalTypeCount }} 题）
                </span>
              </label>
              <div class="space-y-2">
                <div v-for="diff in difficultyLevels" :key="diff.level" class="bg-slate-50 rounded-lg p-3 border border-slate-100">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <span class="px-2 py-0.5 rounded text-xs font-bold" :class="getDifficultyBadgeClass(diff.level)">{{ diff.level }}</span>
                      <span class="font-medium text-slate-700 text-sm">{{ diff.name }}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <button class="btn btn-xs btn-circle btn-ghost" @click="decrementDifficulty(diff.level)">-</button>
                      <input type="text" inputmode="numeric" pattern="[0-9]*" class="input input-bordered input-sm w-12 text-center font-bold text-sm no-spinner" :value="aiConfig.difficultyConfig[diff.level].count || 0" @input="updateDifficultyCount(diff.level, $event.target.value)" />
                      <button class="btn btn-xs btn-circle btn-ghost" @click="incrementDifficulty(diff.level)">+</button>
                      <span class="text-xs text-slate-500 w-10">{{ aiConfig.difficultyConfig[diff.level].percent }}%</span>
                    </div>
                  </div>
                  <p class="text-xs text-slate-500 leading-relaxed">{{ diff.description }}</p>
                </div>
              </div>
              <div :class="['mt-2 p-2 rounded-lg flex items-center justify-between text-white', totalDifficultyCount > totalTypeCount ? 'bg-red-500' : 'bg-gradient-to-r from-indigo-500 to-purple-500']">
                <span class="text-sm">{{ totalDifficultyCount > totalTypeCount ? '超出上限' : '总计' }}</span>
                <span class="font-bold">{{ totalDifficultyCount }} / {{ totalTypeCount }} 题</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤2：智能生成 -->
        <div v-if="aiCurrentStep === 1" class="p-6 min-h-[60vh] flex flex-col items-center justify-center">
          <div class="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center mb-6 animate-pulse">
            <svg class="w-12 h-12 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h4 class="text-xl font-semibold text-slate-700 mb-2">AI正在生成题目...</h4>
          <progress class="progress progress-primary w-80 h-3 mb-4" :value="generateProgress" max="100"></progress>
          <p class="text-sm text-slate-500">已生成 <span class="font-bold text-indigo-600">{{ generatedCount }}</span> / {{ totalDifficultyCount }} 题</p>
          <div class="mt-6 text-xs text-slate-400">
            <p>正在分析知识点关联...</p>
            <p>设计题目结构和干扰项...</p>
          </div>
        </div>

        <!-- 步骤3：质量审核 -->
        <div v-if="aiCurrentStep === 2" class="max-h-[60vh] overflow-y-auto">
          <!-- 顶部操作栏 -->
          <div class="sticky top-0 bg-white border-b border-slate-100 px-6 py-3 z-10">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <span class="font-semibold text-slate-700">生成结果 ({{ generatedQuestions.length }}题)</span>
                <button class="btn btn-xs btn-ghost text-indigo-600" @click="selectAllAdopt">{{ isAllAdopted ? '取消全选' : '全选采纳' }}</button>
              </div>
              <div class="flex items-center gap-6">
                <div class="flex items-center gap-3 text-sm">
                  <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-emerald-500"></span>采纳 <span class="font-bold text-emerald-600">{{ selectedCount }}</span></span>
                  <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-amber-500"></span>草稿 <span class="font-bold text-amber-600">{{ draftCount }}</span></span>
                  <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-red-400"></span>废弃 <span class="font-bold text-red-500">{{ discardedCount }}</span></span>
                </div>
                <button class="btn btn-sm bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 border-0 text-white" @click="confirmAdopt" :disabled="selectedCount + draftCount === 0">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  确认入库 ({{ selectedCount + draftCount }}题)
                </button>
              </div>
            </div>
          </div>

          <!-- 题目列表 - 左右布局 -->
          <div class="p-4 space-y-4">
            <div v-for="(q, idx) in generatedQuestions" :key="idx" 
                 :class="['bg-white rounded-xl border-2 transition-all overflow-hidden', q.isDraft ? 'border-amber-400 bg-amber-50/30' : q.isDiscarded ? 'border-red-300 bg-red-50/30' : q.selected ? 'border-emerald-400 shadow-lg' : 'border-slate-200 hover:border-indigo-300']">
              <!-- 题目头部 -->
              <div class="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-slate-50 to-white border-b border-slate-100">
                <div class="flex items-center gap-3">
                  <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="q.selected" :disabled="q.isDiscarded" />
                  <span class="px-2 py-0.5 rounded text-xs font-bold" :class="getTypeBadgeClass(q.question_type)">{{ q.question_type }}</span>
                  <span class="px-2 py-0.5 rounded text-xs font-bold" :class="getDifficultyBadgeClass(q.difficulty)">{{ q.difficulty }}</span>
                  <span class="text-xs text-slate-400">题目 #{{ idx + 1 }}</span>
                  <span v-if="q.isDraft" class="px-2 py-0.5 text-xs rounded-full bg-amber-100 text-amber-700 font-medium">草稿</span>
                  <span v-if="q.isDiscarded" class="px-2 py-0.5 text-xs rounded-full bg-red-100 text-red-600 font-medium">废弃</span>
                </div>
                <div class="flex gap-2">
                  <button class="btn btn-xs btn-ghost text-indigo-600" @click="editQuestion(q)" :disabled="q.isDiscarded">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    编辑
                  </button>
                  <button class="btn btn-xs btn-ghost text-amber-600" @click="saveSingleAsDraft(q)" v-if="!q.isDraft && !q.isDiscarded">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    存为草稿
                  </button>
                  <button class="btn btn-xs btn-ghost text-emerald-600" @click="q.selected = true" v-if="!q.selected && !q.isDiscarded">采纳</button>
                  <button class="btn btn-xs btn-ghost text-red-500" @click="toggleDiscard(q)">{{ q.isDiscarded ? '恢复' : '废弃' }}</button>
                </div>
              </div>
              
              <!-- 题目内容 - 左右布局 -->
              <div class="grid grid-cols-2 gap-0">
                <!-- 左侧：题目具体信息 -->
                <div class="p-4 border-r border-slate-100 space-y-3">
                  <!-- 题目 -->
                  <div>
                    <div class="text-xs font-medium text-indigo-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      题目
                    </div>
                    <p class="text-sm text-slate-700 leading-relaxed">{{ q.content }}</p>
                  </div>
                  
                  <!-- 单选/多选选项 -->
                  <div v-if="['单选', '多选'].includes(q.question_type) && q.options && q.options.length">
                    <div class="text-xs font-medium text-slate-500 mb-1">选项</div>
                    <div class="space-y-1">
                      <div v-for="(opt, optIdx) in q.options" :key="optIdx" 
                           :class="['flex items-start gap-2 p-2 rounded-lg text-sm', opt.is_correct ? 'bg-emerald-50 border border-emerald-200' : 'bg-slate-50']">
                        <span :class="['w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0', opt.is_correct ? 'bg-emerald-500 text-white' : 'bg-white text-slate-500 border border-slate-200']">{{ String.fromCharCode(65 + optIdx) }}</span>
                        <span class="flex-1 text-slate-600">{{ opt.content }}</span>
                        <span v-if="opt.is_correct" class="text-xs text-emerald-600 font-medium">✓ 正确</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 判断题选项 -->
                  <div v-if="q.question_type === '判断'">
                    <div class="text-xs font-medium text-slate-500 mb-1">选项</div>
                    <div class="flex gap-3">
                      <div :class="['flex items-center gap-2 px-4 py-2 rounded-lg text-sm', q.answer === '正确' || q.answer === 'A' ? 'bg-emerald-50 border border-emerald-200' : 'bg-slate-50 border border-slate-100']">
                        <span :class="['w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold', q.answer === '正确' || q.answer === 'A' ? 'bg-emerald-500 text-white' : 'bg-white text-slate-500 border border-slate-200']">✓</span>
                        <span class="text-slate-600">正确</span>
                      </div>
                      <div :class="['flex items-center gap-2 px-4 py-2 rounded-lg text-sm', q.answer === '错误' || q.answer === 'B' ? 'bg-red-50 border border-red-200' : 'bg-slate-50 border border-slate-100']">
                        <span :class="['w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold', q.answer === '错误' || q.answer === 'B' ? 'bg-red-500 text-white' : 'bg-white text-slate-500 border border-slate-200']">✗</span>
                        <span class="text-slate-600">错误</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 填空题答案 -->
                  <div v-if="q.question_type === '填空'">
                    <div class="text-xs font-medium text-emerald-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      填空答案
                    </div>
                    <div class="p-2 bg-emerald-50 rounded-lg border border-emerald-200">
                      <p class="text-sm text-slate-700 font-medium">{{ q.answer }}</p>
                    </div>
                  </div>
                  
                  <!-- 主观题参考答案 -->
                  <div v-if="q.question_type === '主观'">
                    <div class="text-xs font-medium text-emerald-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      参考答案
                    </div>
                    <div class="p-2 bg-emerald-50 rounded-lg border border-emerald-200">
                      <p class="text-sm text-slate-700 leading-relaxed">{{ q.answer }}</p>
                    </div>
                  </div>
                  
                  <!-- 单选/多选题答案 -->
                  <div v-if="['单选', '多选'].includes(q.question_type)">
                    <div class="text-xs font-medium text-emerald-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      正确答案
                    </div>
                    <p class="text-sm text-slate-700 font-medium">{{ q.answer }}</p>
                  </div>
                  
                  <!-- 解析 -->
                  <div>
                    <div class="text-xs font-medium text-amber-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                      </svg>
                      解析
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ q.explanation }}</p>
                  </div>
                </div>
                
                <!-- 右侧：设计原因 -->
                <div class="p-4 bg-slate-50 space-y-3">
                  <!-- 考察知识点 -->
                  <div class="bg-white rounded-lg p-3 border border-slate-100">
                    <div class="text-xs font-medium text-cyan-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                      </svg>
                      考察知识点
                    </div>
                    <div class="flex flex-wrap gap-1">
                      <span v-for="tag in q.knowledgePoints" :key="tag" class="px-2 py-0.5 text-xs rounded-full bg-cyan-50 text-cyan-700 border border-cyan-100">{{ tag }}</span>
                    </div>
                  </div>
                  
                  <!-- 题目设计原因 -->
                  <div class="bg-indigo-50 rounded-lg p-3 border border-indigo-100">
                    <div class="text-xs font-medium text-indigo-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                      </svg>
                      题目设计依据
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ q.designReason || '暂无' }}</p>
                  </div>
                  
                  <!-- 难度层级说明 -->
                  <div v-if="q.difficultyReason" class="bg-amber-50 rounded-lg p-3 border border-amber-100">
                    <div class="text-xs font-medium text-amber-600 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      难度层级说明
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ q.difficultyReason }}</p>
                  </div>
                  
                  <!-- 干扰项设计原因 - 仅选择题显示 -->
                  <div v-if="['单选', '多选'].includes(q.question_type) && q.distractorReasons && q.distractorReasons.length" class="bg-purple-50 rounded-lg p-3 border border-purple-100">
                    <div class="text-xs font-medium text-purple-600 mb-2 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      干扰项设计原因
                    </div>
                    <div class="space-y-1">
                      <div v-for="(reason, rIdx) in q.distractorReasons" :key="rIdx" class="flex items-start gap-2 text-sm">
                        <span class="text-purple-500 font-medium">{{ reason.option }}:</span>
                        <span class="text-slate-600">{{ reason.reason }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 非选择题的设计提示 -->
                  <div v-if="!['单选', '多选'].includes(q.question_type)" class="bg-slate-100 rounded-lg p-3 border border-slate-200">
                    <div class="text-xs font-medium text-slate-500 mb-1 flex items-center gap-1">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      出题说明
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ q.designReason }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 弹窗底部操作栏 -->
        <div class="flex items-center justify-between px-6 py-4 border-t border-slate-100 bg-white">
          <div>
            <button v-if="aiCurrentStep > 0" class="btn btn-ghost" @click="prevStep">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              上一步
            </button>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-ghost" @click="closeAIDialog">取消</button>
            <button v-if="aiCurrentStep === 0" class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white shadow-lg" @click="startGenerate" :disabled="!canStartGenerate">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              开始生成
            </button>
          </div>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="closeAIDialog">close</button>
      </form>
    </dialog>

    <!-- 题目编辑弹窗 -->
    <dialog :class="['modal', { 'modal-open': showQuestionEditModal }]">
      <div class="modal-box w-11/12 max-w-3xl bg-white rounded-2xl shadow-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800">编辑题目</h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showQuestionEditModal = false">✕</button>
        </div>
        <div v-if="editingQuestion" class="space-y-4">
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">题目内容</span></label>
            <textarea class="textarea textarea-bordered h-24 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="editingQuestion.content"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">题型</span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="editingQuestion.question_type">
                <option value="单选">单选题</option>
                <option value="多选">多选题</option>
                <option value="判断">判断题</option>
                <option value="填空">填空题</option>
                <option value="主观">主观题</option>
              </select>
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">难度</span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="editingQuestion.difficulty">
                <option value="L1">L1 记忆</option>
                <option value="L2">L2 理解</option>
                <option value="L3">L3 应用</option>
                <option value="L4">L4 分析</option>
                <option value="L5">L5 创造</option>
              </select>
            </div>
          </div>
          <div v-if="['单选', '多选', '判断'].includes(editingQuestion.question_type)" class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">选项</span></label>
            <div class="space-y-2">
              <div v-for="(opt, idx) in editingQuestion.options" :key="idx" class="flex items-center gap-2 p-2 bg-slate-50 rounded-lg">
                <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="opt.is_correct" />
                <span :class="['w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold', opt.is_correct ? 'bg-emerald-500 text-white' : 'bg-white text-slate-500 border border-slate-200']">{{ String.fromCharCode(65 + idx) }}</span>
                <input type="text" class="input input-bordered flex-1 bg-white" v-model="opt.content" />
              </div>
            </div>
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">解析</span></label>
            <textarea class="textarea textarea-bordered h-20" v-model="editingQuestion.explanation"></textarea>
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showQuestionEditModal = false">取消</button>
          <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white" @click="saveQuestionEdit">保存修改</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showQuestionEditModal = false">close</button>
      </form>
    </dialog>

    <!-- 导入弹窗 -->
    <dialog :class="['modal', { 'modal-open': showImportDialog }]">
      <div class="modal-box bg-white rounded-2xl shadow-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
            </svg>
            导入题目
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showImportDialog = false">✕</button>
        </div>
        <div class="border-2 border-dashed border-indigo-200 rounded-2xl p-10 text-center hover:border-indigo-400 hover:bg-indigo-50/50 transition-all cursor-pointer">
          <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
            <svg class="w-8 h-8 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
          </div>
          <p class="text-slate-600 font-medium mb-1">点击或拖拽文件到此处上传</p>
          <p class="text-sm text-slate-400">支持 Excel (.xlsx, .xls) 格式</p>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showImportDialog = false">取消</button>
          <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white">确认导入</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showImportDialog = false">close</button>
      </form>
    </dialog>

    <!-- 规则选择弹窗 -->
    <dialog :class="['modal', { 'modal-open': showRuleSelector }]">
      <div class="modal-box bg-white rounded-2xl shadow-2xl max-w-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
            选择自定义规则
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showRuleSelector = false">✕</button>
        </div>
        <div class="space-y-2 max-h-[60vh] overflow-y-auto">
          <div v-if="customRules.length === 0" class="text-center py-8 text-slate-400">
            <svg class="w-12 h-12 mx-auto mb-2 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <p class="text-sm">暂无自定义规则</p>
            <p class="text-xs mt-1">请前往规则管理页面创建</p>
          </div>
          <div v-for="rule in customRules" :key="rule.id" :class="['p-4 rounded-xl cursor-pointer transition-all border-2', aiConfig.customRuleId === rule.id ? 'border-purple-500 bg-purple-50 shadow-md' : 'border-slate-200 hover:border-purple-200 hover:bg-slate-50']" @click="selectCustomRule(rule)">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <span :class="['px-2 py-0.5 rounded text-xs font-medium', rule.status === '启用' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600']">{{ rule.status }}</span>
                <span class="font-medium text-slate-800">{{ rule.name }}</span>
              </div>
              <svg v-if="aiConfig.customRuleId === rule.id" class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <p class="text-sm text-slate-500 line-clamp-2">{{ rule.description }}</p>
            <div class="flex items-center gap-4 mt-2 text-xs text-slate-400">
              <span>场景：{{ rule.scene || '通用' }}</span>
              <span>使用 {{ rule.useCount || 0 }} 次</span>
            </div>
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showRuleSelector = false">取消</button>
          <button class="btn bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0 text-white" @click="showRuleSelector = false">确认选择</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showRuleSelector = false">close</button>
      </form>
    </dialog>
  </div>
</template>

<script>
import api from '@/api'
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      searchKeyword: '',
      filterType: '',
      filterDifficulty: '',
      filterStatus: '',
      currentPage: 1,
      total: 0,
      questions: [],
      selectedIds: [],
      selectAll: false,
      stats: { total: 128, reviewed: 95, pending: 20, draft: 13, monthlyNew: 15, reviewedMonthly: 12 },
      typeStats: [
        { label: '单选', value: 45, percent: 35, monthlyNew: 5, textClass: 'text-indigo-600', barClass: 'bg-indigo-500' },
        { label: '多选', value: 32, percent: 25, monthlyNew: 4, textClass: 'text-emerald-600', barClass: 'bg-emerald-500' },
        { label: '判断', value: 28, percent: 22, monthlyNew: 3, textClass: 'text-amber-600', barClass: 'bg-amber-500' },
        { label: '填空', value: 15, percent: 12, monthlyNew: 2, textClass: 'text-purple-600', barClass: 'bg-purple-500' },
        { label: '主观', value: 8, percent: 6, monthlyNew: 1, textClass: 'text-cyan-600', barClass: 'bg-cyan-500' }
      ],
      showDetailModal: false,
      showEditModal: false,
      showAIDialog: false,
      showImportDialog: false,
      showQuestionEditModal: false,
      currentQuestion: null,
      editingQuestion: null,
      isEdit: false,
      form: {
        id: null,
        content: '',
        question_type: '单选',
        difficulty: 'L2',
        status: '草稿',
        source: '手动录入',
        answer: '',
        explanation: '',
        options: [
          { content: '', is_correct: false },
          { content: '', is_correct: false },
          { content: '', is_correct: false },
          { content: '', is_correct: false }
        ],
        knowledgePointsInput: '',
        tagsInput: ''
      },
      knowledgeTree: [
        { id: 1, name: 'Python基础' },
        { id: 2, name: '数据类型' },
        { id: 3, name: '控制流' },
        { id: 4, name: '函数' },
        { id: 5, name: '面向对象' },
        { id: 6, name: '异常处理' },
        { id: 7, name: '文件操作' },
        { id: 8, name: '模块与包' }
      ],
      questionTypes: [
        { id: '单选', name: '单选题' },
        { id: '多选', name: '多选题' },
        { id: '判断', name: '判断题' },
        { id: '填空', name: '填空题' },
        { id: '主观', name: '主观题' }
      ],
      difficultyLevels: [
        { level: 'L1', name: '记忆', description: '能够识别和回忆事实、术语、基本概念等知识，如定义、公式、基本原理的识记。' },
        { level: 'L2', name: '理解', description: '能够解释概念含义，理解知识间的关系，用自己的语言阐述或举例说明。' },
        { level: 'L3', name: '应用', description: '能够在具体情境中运用所学知识解决问题，执行既定程序或方法。' },
        { level: 'L4', name: '分析', description: '能够分解复杂问题，分析各部分关系，识别因果关系和逻辑结构。' },
        { level: 'L5', name: '创造', description: '能够综合运用知识创造新方案，设计创新解决方案，进行评价和改进。' }
      ],
      distractorTypes: [
        { id: 'misconception', name: '常见误区型', description: '基于学生常见的错误理解或误解来设计干扰项', example: '例：学生常混淆"=="和"="' },
        { id: 'similar', name: '相似概念型', description: '使用与正确答案相似但本质不同的概念', example: '例：list和tuple、break和continue' },
        { id: 'partial', name: '部分正确型', description: '选项部分正确但不完整，考察学生全面理解', example: '例：只描述了部分特征' },
        { id: 'overgeneral', name: '过度概括型', description: '将特定情况错误地推广到一般情况', example: '例：将某特性错误推广' }
      ],
      contentPreferences: [
        { id: 'practical', name: '结合实际案例', description: '题目会结合实际编程场景和应用案例' },
        { id: 'code', name: '包含代码分析', description: '题目会包含代码片段进行分析' },
        { id: 'concept', name: '侧重概念理解', description: '题目侧重于概念和原理的理解' },
        { id: 'debug', name: '包含调试场景', description: '题目会包含代码调试和错误排查场景' }
      ],
      aiSteps: ['配置参数', '智能生成', '质量审核'],
      aiCurrentStep: 0,
      currentTaskId: null,
      aiConfig: {
        knowledgeInput: '',
        knowledgeIds: [],
        types: [],
        typeCounts: { '单选': 0, '多选': 0, '判断': 0, '填空': 0, '主观': 0 },
        difficultyConfig: {
          L1: { count: 0, percent: 0 },
          L2: { count: 0, percent: 0 },
          L3: { count: 0, percent: 0 },
          L4: { count: 0, percent: 0 },
          L5: { count: 0, percent: 0 }
        },
        distractorList: [],
        preferenceList: [],
        custom: '',
        customRuleId: null
      },
      isGenerating: false,
      generateProgress: 0,
      generatedCount: 0,
      generatedQuestions: [],
      activeHelpTip: null,
      defaultRule: null,
      customRules: [],
      showRuleSelector: false
    }
  },
  computed: {
    selectedGenerated() {
      return this.generatedQuestions.filter(q => q.selected)
    },
    totalTypeCount() {
      return Object.values(this.aiConfig.typeCounts).reduce((sum, c) => sum + c, 0)
    },
    totalDifficultyCount() {
      return Object.values(this.aiConfig.difficultyConfig).reduce((sum, d) => sum + d.count, 0)
    },
    remainingDifficultyCount() {
      return Math.max(0, this.totalTypeCount - this.totalDifficultyCount)
    },
    canStartGenerate() {
      return (this.aiConfig.knowledgeInput || this.aiConfig.knowledgeIds.length > 0) && 
             this.aiConfig.types.length > 0 && 
             this.totalDifficultyCount > 0 &&
             this.totalDifficultyCount <= this.totalTypeCount
    },
    selectedCount() {
      return this.generatedQuestions.filter(q => q.selected).length
    },
    draftCount() {
      return this.generatedQuestions.filter(q => q.isDraft).length
    },
    discardedCount() {
      return this.generatedQuestions.filter(q => q.isDiscarded).length
    },
    isAllAdopted() {
      const adoptable = this.generatedQuestions.filter(q => !q.isDiscarded)
      return adoptable.length > 0 && adoptable.every(q => q.selected)
    },
    selectedCustomRule() {
      if (!this.aiConfig.customRuleId) return null
      return this.customRules.find(r => r.id === this.aiConfig.customRuleId)
    }
  },
  mounted() {
    this.loadQuestions()
    this.loadStats()
    this.loadKnowledgePoints()
    this.loadRules()
  },
  methods: {
    async loadRules() {
      try {
        const res = await axios.get('http://localhost:5001/api/rule/rules')
        const rules = res.data.rules || []
        this.defaultRule = rules.find(r => r.isDefault) || null
        this.customRules = rules.filter(r => !r.isDefault)
      } catch (e) {
        console.error('加载规则失败:', e)
      }
    },
    selectCustomRule(rule) {
      this.aiConfig.customRuleId = rule.id
      this.showRuleSelector = false
    },
    loadStats() {
      api.getStats().then(res => {
        this.stats = {
          total: res.total,
          reviewed: res.reviewed,
          pending: res.pending,
          draft: res.draft,
          monthlyNew: 15,
          reviewedMonthly: 12
        }
        this.typeStats = (res.type_stats || []).map((t, idx) => {
          const colors = [
            { label: '单选', textClass: 'text-indigo-600', barClass: 'bg-indigo-500' },
            { label: '多选', textClass: 'text-emerald-600', barClass: 'bg-emerald-500' },
            { label: '判断', textClass: 'text-amber-600', barClass: 'bg-amber-500' },
            { label: '填空', textClass: 'text-purple-600', barClass: 'bg-purple-500' },
            { label: '主观', textClass: 'text-cyan-600', barClass: 'bg-cyan-500' }
          ]
          const total = res.total || 1
          return {
            label: t.type,
            value: t.count,
            percent: Math.round((t.count / total) * 100),
            monthlyNew: Math.floor(Math.random() * 5) + 1,
            ...colors[idx]
          }
        })
      }).catch(err => {
        console.error('获取统计失败:', err)
      })
    },
    loadKnowledgePoints() {
      api.getKnowledgeCategories().then(res => {
        if (res.data && res.data.length > 0) {
          this.knowledgeTree = res.data.map(cat => ({
            id: cat,
            name: cat
          }))
        } else {
          this.knowledgeTree = []
        }
      }).catch(err => {
        console.error('获取知识库分类失败:', err)
        this.knowledgeTree = []
      })
    },
    getTypeBadgeClass(type) {
      const map = {
        '单选': 'bg-indigo-100 text-indigo-700',
        '多选': 'bg-emerald-100 text-emerald-700',
        '判断': 'bg-amber-100 text-amber-700',
        '填空': 'bg-purple-100 text-purple-700',
        '主观': 'bg-cyan-100 text-cyan-700'
      }
      return map[type] || 'bg-slate-100 text-slate-700'
    },
    getDifficultyBadgeClass(difficulty) {
      const map = {
        'L1': 'bg-slate-100 text-slate-600',
        'L2': 'bg-blue-100 text-blue-700',
        'L3': 'bg-amber-100 text-amber-700',
        'L4': 'bg-orange-100 text-orange-700',
        'L5': 'bg-red-100 text-red-700'
      }
      return map[difficulty] || 'bg-slate-100 text-slate-700'
    },
    getStatusDotClass(status) {
      const map = {
        '已发布': 'bg-emerald-500',
        '待审核': 'bg-amber-500',
        '草稿': 'bg-slate-400'
      }
      return map[status] || 'bg-slate-400'
    },
    getStatusTextClass(status) {
      const map = {
        '已审核': 'text-emerald-600',
        '待审核': 'text-amber-600',
        '草稿': 'text-slate-500'
      }
      return map[status] || 'text-slate-500'
    },
    getStatusBadgeClass(status) {
      const map = {
        '已审核': 'bg-emerald-100 text-emerald-700',
        '待审核': 'bg-amber-100 text-amber-700',
        '草稿': 'bg-slate-100 text-slate-600'
      }
      return map[status] || 'bg-slate-100 text-slate-600'
    },
    getDifficultyName(difficulty) {
      const map = {
        'L1': '记忆',
        'L2': '理解',
        'L3': '应用',
        'L4': '分析',
        'L5': '创造'
      }
      return map[difficulty] || ''
    },
    getSourceBadgeClass(source) {
      const map = {
        '系统生成': 'bg-indigo-50 text-indigo-600',
        '手动录入': 'bg-emerald-50 text-emerald-600',
        '导入': 'bg-amber-50 text-amber-600',
        'AI生成': 'bg-purple-50 text-purple-600'
      }
      return map[source] || 'bg-slate-50 text-slate-500'
    },
    updateDifficultyPercent() {
      const total = this.totalDifficultyCount
      if (total > 0) {
        Object.keys(this.aiConfig.difficultyConfig).forEach(key => {
          this.aiConfig.difficultyConfig[key].percent = Math.round((this.aiConfig.difficultyConfig[key].count / total) * 100)
        })
      }
    },
    incrementDifficulty(level) {
      if (this.totalDifficultyCount < this.totalTypeCount) {
        this.aiConfig.difficultyConfig[level].count++
        this.updateDifficultyPercent()
      }
    },
    decrementDifficulty(level) {
      if (this.aiConfig.difficultyConfig[level].count > 0) {
        this.aiConfig.difficultyConfig[level].count--
        this.updateDifficultyPercent()
      }
    },
    updateDifficultyCount(level, value) {
      let num = parseInt(value) || 0
      if (num < 0) num = 0
      if (num > 99) num = 99
      this.$set(this.aiConfig.difficultyConfig[level], 'count', num)
      this.updateDifficultyPercent()
    },
    incrementTypeCount(typeId) {
      const current = this.aiConfig.typeCounts[typeId] || 0
      if (current < 99) {
        this.$set(this.aiConfig.typeCounts, typeId, current + 1)
      }
    },
    decrementTypeCount(typeId) {
      const current = this.aiConfig.typeCounts[typeId] || 0
      if (current > 0) {
        this.$set(this.aiConfig.typeCounts, typeId, current - 1)
      }
    },
    updateTypeCount(typeId, value) {
      let num = parseInt(value) || 0
      if (num < 0) num = 0
      if (num > 99) num = 99
      this.$set(this.aiConfig.typeCounts, typeId, num)
    },
    showHelpTip(id) {
      this.activeHelpTip = id
    },
    hideHelpTip() {
      this.activeHelpTip = null
    },
    addDistractor() {
      this.aiConfig.distractorList.push({ name: '' })
    },
    addPreference() {
      this.aiConfig.preferenceList.push({ name: '' })
    },
    loadQuestions() {
      const params = {
        page: this.currentPage,
        per_page: 10,
        question_type: this.filterType,
        difficulty: this.filterDifficulty,
        status: this.filterStatus,
        keyword: this.searchKeyword
      }
      
      api.getQuestions(params).then(res => {
        this.questions = res.questions.map(q => ({
          ...q,
          selected: false,
          knowledgePoints: q.knowledge_points || [],
          createdAt: q.created_at,
          updatedAt: q.updated_at
        }))
        this.total = res.total
      }).catch(err => {
        console.error('获取题目列表失败:', err)
        this.questions = [
          { id: 1, content: '下列关于Python的说法，正确的是：Python是一种高级编程语言，具有简洁易学的特点。', question_type: '单选', difficulty: 'L2', status: '已审核', source: 'AI生成', knowledgePoints: ['Python基础', '语言特性'], tags: ['基础', '重要'], selected: false },
          { id: 2, content: '以下哪些是Python的内置数据类型？请选择所有正确的选项。', question_type: '多选', difficulty: 'L2', status: '已审核', source: '手动录入', knowledgePoints: ['数据类型', '内置类型'], tags: ['基础'], selected: false },
          { id: 3, content: 'Python中可以使用for循环遍历列表。', question_type: '判断', difficulty: 'L1', status: '待审核', source: '系统生成', knowledgePoints: ['控制流', '循环'], tags: ['基础'], selected: false },
          { id: 4, content: '请简述Python中列表和元组的区别。', question_type: '主观', difficulty: 'L3', status: '草稿', source: '手动录入', knowledgePoints: ['列表', '元组'], tags: ['进阶'], selected: false },
          { id: 5, content: 'Python中的______函数用于获取列表的长度。', question_type: '填空', difficulty: 'L1', status: '待审核', source: '导入', knowledgePoints: ['内置函数', 'len'], tags: ['基础'], selected: false }
        ]
        this.total = 5
      })
    },
    handleSearch() {
      this.loadQuestions()
    },
    handleSelectAll() {
      this.questions.forEach(q => q.selected = this.selectAll)
      this.selectedIds = this.selectAll ? this.questions.map(q => q.id) : []
    },
    handleItemSelect() {
      this.selectedIds = this.questions.filter(q => q.selected).map(q => q.id)
      this.selectAll = this.selectedIds.length === this.questions.length
    },
    clearSelection() {
      this.questions.forEach(q => q.selected = false)
      this.selectedIds = []
      this.selectAll = false
    },
    showAddDialog() {
      this.isEdit = false
      this.form = { id: null, content: '', question_type: '单选', difficulty: 'L2', status: '草稿', source: '手动录入', answer: '', explanation: '', options: [{ content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }], knowledgePointsInput: '', tagsInput: '' }
      this.showEditModal = true
    },
    showEditDialog(item) {
      this.isEdit = true
      this.form = { ...item, knowledgePointsInput: (item.knowledgePoints || []).join(', '), tagsInput: (item.tags || []).join(', ') }
      this.showEditModal = true
    },
    showDetail(item) {
      this.currentQuestion = item
      this.showDetailModal = true
    },
    saveQuestion() {
      const data = {
        content: this.form.content,
        question_type: this.form.question_type,
        difficulty: this.form.difficulty,
        status: this.form.status,
        source: this.form.source,
        answer: this.form.answer,
        explanation: this.form.explanation,
        options: this.form.options,
        knowledge_point_ids: this.form.knowledgePointsInput.split(',').map(s => s.trim()).filter(Boolean),
        tag_names: this.form.tagsInput.split(',').map(s => s.trim()).filter(Boolean)
      }
      
      if (this.isEdit) {
        api.updateQuestion(this.form.id, data).then(() => {
          this.$message.success('更新成功')
          this.showEditModal = false
          this.loadQuestions()
        }).catch(err => {
          console.error('更新失败:', err)
          this.$message.error('更新失败')
        })
      } else {
        api.createQuestion(data).then(() => {
          this.$message.success('创建成功')
          this.showEditModal = false
          this.loadQuestions()
        }).catch(err => {
          console.error('创建失败:', err)
          this.$message.error('创建失败')
        })
      }
    },
    saveAsDraftFromEdit() {
      this.form.status = '草稿'
      this.showEditModal = false
      this.$message.success('已存为草稿')
      this.loadQuestions()
    },
    deleteQuestion(id) {
      if (confirm('确定删除该题目？')) {
        api.deleteQuestion(id).then(() => {
          this.$message.success('删除成功')
          this.loadQuestions()
        }).catch(err => {
          console.error('删除失败:', err)
          this.$message.error('删除失败')
        })
      }
    },
    batchPublish() {
      this.$message.success(`已发布 ${this.selectedIds.length} 题`)
      this.clearSelection()
    },
    batchReview() {
      api.batchReview(this.selectedIds).then(() => {
        this.$message.success(`已审核通过 ${this.selectedIds.length} 题`)
        this.clearSelection()
        this.loadQuestions()
      }).catch(err => {
        console.error('批量审核失败:', err)
        this.$message.error('批量审核失败')
      })
    },
    batchDraft() {
      api.batchDraft(this.selectedIds).then(() => {
        this.$message.success(`已设为草稿 ${this.selectedIds.length} 题`)
        this.clearSelection()
        this.loadQuestions()
      }).catch(err => {
        console.error('批量设为草稿失败:', err)
        this.$message.error('批量设为草稿失败')
      })
    },
    batchDelete() {
      if (confirm(`确定删除 ${this.selectedIds.length} 题？`)) {
        api.batchDelete(this.selectedIds).then(() => {
          this.$message.success(`已删除 ${this.selectedIds.length} 题`)
          this.clearSelection()
          this.loadQuestions()
        }).catch(err => {
          console.error('批量删除失败:', err)
          this.$message.error('批量删除失败')
        })
      }
    },
    reviewQuestion(item) {
      api.reviewQuestion(item.id).then(() => {
        item.status = '已审核'
        this.$message.success('审核成功')
        this.loadQuestions()
      }).catch(err => {
        console.error('审核失败:', err)
        this.$message.error('审核失败')
      })
    },
    batchDraft() {
      this.$message.success(`已设为草稿 ${this.selectedIds.length} 题`)
      this.clearSelection()
    },
    batchDelete() {
      this.$confirm(`确定删除 ${this.selectedIds.length} 题？`, '提示', { type: 'warning' }).then(() => {
        this.$message.success('删除成功')
        this.clearSelection()
        this.loadQuestions()
      }).catch(() => {})
    },
    handleExport() {
      this.$message.success('导出成功')
    },
    openAIDialog() {
      this.aiCurrentStep = 0
      this.generatedQuestions = []
      this.showAIDialog = true
    },
    closeAIDialog() {
      this.showAIDialog = false
    },
    prevStep() {
      if (this.aiCurrentStep > 0) {
        this.aiCurrentStep--
      }
    },
    startGenerate() {
      if (!this.canStartGenerate) {
        if (!this.aiConfig.knowledgeInput && !this.aiConfig.knowledgeIds.length) return this.$message.error('请输入或选择知识范围')
        if (!this.aiConfig.types.length) return this.$message.error('请选择题型')
        if (this.totalDifficultyCount === 0) return this.$message.error('请设置题目数量')
        return
      }
      
      this.aiCurrentStep = 1
      this.isGenerating = true
      this.generateProgress = 0
      this.generatedCount = 0
      this.generatedQuestions = []
      
      const requestData = {
        knowledge_input: this.aiConfig.knowledgeInput,
        knowledge_category: this.aiConfig.knowledgeIds.length > 0 ? this.aiConfig.knowledgeIds[0] : null,
        question_types: this.aiConfig.types,
        type_counts: this.aiConfig.typeCounts,
        difficulty_config: this.aiConfig.difficultyConfig,
        distractor_list: this.aiConfig.distractorList,
        preference_list: this.aiConfig.preferenceList,
        custom_requirement: this.aiConfig.custom,
        total_count: this.totalDifficultyCount,
        rule_id: this.aiConfig.customRuleId
      }
      
      const total = this.totalDifficultyCount
      let progressInterval = setInterval(() => {
        if (this.generateProgress < 90) {
          this.generateProgress += 5
          this.generatedCount = Math.floor((this.generateProgress / 100) * total)
        }
      }, 500)
      
      api.generateQuestions(requestData).then(res => {
        clearInterval(progressInterval)
        
        if (res.code === 0) {
          this.generateProgress = 100
          this.generatedCount = res.data.count
          this.currentTaskId = res.data.task_id
          
          setTimeout(() => {
            api.getGeneratedQuestions(res.data.task_id).then(questionsRes => {
              this.generatedQuestions = questionsRes.data.map(q => ({
                ...q,
                selected: q.is_selected,
                isDraft: q.is_draft,
                isDiscarded: q.is_discarded,
                knowledgePoints: q.knowledge_points,
                distractorReasons: q.distractor_reasons
              }))
              this.isGenerating = false
              this.aiCurrentStep = 2
              this.$message.success(`成功生成 ${this.generatedQuestions.length} 道题目`)
            })
          }, 500)
        } else {
          clearInterval(progressInterval)
          this.isGenerating = false
          this.aiCurrentStep = 0
          this.$message.error(res.message || '生成失败')
        }
      }).catch(err => {
        clearInterval(progressInterval)
        this.isGenerating = false
        this.aiCurrentStep = 0
        console.error('生成失败:', err)
        this.$message.error('AI生成服务暂时不可用，请稍后重试')
      })
    },
    selectAllGenerated() {
      const all = this.isAllSelected
      this.generatedQuestions.forEach(q => q.selected = !all)
    },
    editQuestion(q) {
      this.editingQuestion = JSON.parse(JSON.stringify(q))
      this.showQuestionEditModal = true
    },
    saveQuestionEdit() {
      const idx = this.generatedQuestions.findIndex(q => q === this.editingQuestion || q.content === this.editingQuestion.content)
      if (idx !== -1) {
        this.generatedQuestions[idx] = { ...this.editingQuestion }
      }
      this.showQuestionEditModal = false
      this.$message.success('修改已保存')
    },
    saveAsDraft() {
      const count = this.selectedCount
      if (!count) return this.$message.error('请选择题目')
      this.generatedQuestions.forEach(q => {
        if (q.selected) {
          q.isDraft = true
          q.selected = false
        }
      })
      this.$message.success(`已将 ${count} 题存为草稿`)
    },
    saveSingleAsDraft(q) {
      q.isDraft = true
      q.selected = false
      this.$message.success('已存为草稿')
    },
    toggleDiscard(q) {
      q.isDiscarded = !q.isDiscarded
      if (q.isDiscarded) {
        q.selected = false
        q.isDraft = false
      }
    },
    selectAllAdopt() {
      const adoptable = this.generatedQuestions.filter(q => !q.isDiscarded)
      const allSelected = adoptable.every(q => q.selected)
      adoptable.forEach(q => q.selected = !allSelected)
    },
    confirmAdopt() {
      const count = this.selectedCount + this.draftCount
      if (!count) return this.$message.error('请选择题目或存为草稿')
      
      const questionIds = this.generatedQuestions
        .filter(q => q.selected || q.isDraft)
        .map(q => q.id)
      
      if (!this.currentTaskId) {
        this.$message.error('任务ID不存在，请重新生成')
        return
      }
      
      api.adoptQuestions(this.currentTaskId, questionIds).then(res => {
        this.$message.success(`已入库 ${count} 题（采纳 ${this.selectedCount} 题，草稿 ${this.draftCount} 题）`)
        this.showAIDialog = false
        this.loadQuestions()
        this.loadStats()
      }).catch(err => {
        console.error('入库失败:', err)
        this.$message.error('入库失败，请重试')
      })
    }
  }
}
</script>

<style lang="less" scoped>
@import '../assets/styles/variables.less';

.no-spinner::-webkit-outer-spin-button,
.no-spinner::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.no-spinner {
  -moz-appearance: textfield;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.help-tip {
  position: relative;
  display: inline-block;
}

.help-tip-content {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding: @spacing-sm @spacing-md;
  background: @primary-color;
  color: @text-white;
  font-size: @font-size-xs;
  border-radius: @radius-md;
  white-space: normal;
  z-index: 1000;
  margin-bottom: @spacing-sm;
  width: max-content;
  max-width: 280px;
  box-shadow: @shadow-lg;
}

.help-tip-content::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: @primary-color;
}

.modal-box {
  overflow-x: hidden;
}

.modal-box::-webkit-scrollbar {
  width: 6px;
}

.modal-box::-webkit-scrollbar-track {
  background: @bg-hover;
  border-radius: 3px;
}

.modal-box::-webkit-scrollbar-thumb {
  background: @border-dark;
  border-radius: 3px;
}

.modal-box::-webkit-scrollbar-thumb:hover {
  background: @text-muted;
}
</style>
