<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- 顶部导航 -->
    <header class="bg-white/80 backdrop-blur-xl sticky top-0 z-50 border-b border-indigo-100 shadow-sm">
      <div class="px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="relative">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-indigo-200">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </div>
            <div class="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
          </div>
          <div>
            <span class="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">智能题库</span>
            <span class="text-xs text-slate-400 block -mt-1">AI Teaching System</span>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button class="relative p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <div class="flex items-center gap-3 pl-4 border-l border-slate-200">
            <div class="text-right">
              <div class="text-sm font-medium text-slate-700">李老师</div>
              <div class="text-xs text-slate-400">Python课程组</div>
            </div>
            <div class="avatar">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white font-medium shadow-md">
                李
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="p-6">
      <!-- 欢迎横幅 -->
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
                <div class="text-3xl font-bold text-emerald-600">{{ stats.published }}</div>
                <div class="text-sm text-slate-500 mt-1">已发布</div>
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
            <option value="已发布">已发布</option>
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
          <button class="btn btn-sm bg-emerald-500 hover:bg-emerald-600 border-0 text-white" @click="batchPublish">发布</button>
          <button class="btn btn-sm bg-slate-500 hover:bg-slate-600 border-0 text-white" @click="batchDraft">设为草稿</button>
          <button class="btn btn-sm bg-red-500 hover:bg-red-600 border-0 text-white" @click="batchDelete">删除</button>
        </div>
        <button class="btn btn-sm btn-ghost text-slate-500" @click="clearSelection">取消</button>
      </section>

      <!-- 题目列表 -->
      <section class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="table">
            <thead class="bg-gradient-to-r from-slate-50 to-slate-100">
              <tr>
                <th class="w-12">
                  <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="selectAll" @change="handleSelectAll" />
                </th>
                <th class="w-16 text-slate-500 font-medium">ID</th>
                <th class="text-slate-500 font-medium">题目内容</th>
                <th class="w-24 text-slate-500 font-medium">题型</th>
                <th class="w-24 text-slate-500 font-medium">难度</th>
                <th class="w-24 text-slate-500 font-medium">状态</th>
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
                  <div class="cursor-pointer group" @click="showDetail(item)">
                    <div class="text-slate-700 group-hover:text-indigo-600 transition-colors line-clamp-2">{{ item.content }}</div>
                    <div v-if="item.tags && item.tags.length" class="flex gap-1 mt-2">
                      <span v-for="tag in item.tags" :key="tag" class="px-2 py-0.5 text-xs rounded-full bg-indigo-50 text-indigo-600 border border-indigo-100">{{ tag }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="px-3 py-1 rounded-full text-xs font-medium" :class="getTypeBadgeClass(item.question_type)">{{ item.question_type }}</span>
                </td>
                <td>
                  <span class="px-3 py-1 rounded-full text-xs font-medium" :class="getDifficultyBadgeClass(item.difficulty)">{{ item.difficulty }}</span>
                </td>
                <td>
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full" :class="getStatusDotClass(item.status)"></span>
                    <span class="text-sm" :class="getStatusTextClass(item.status)">{{ item.status }}</span>
                  </div>
                </td>
                <td>
                  <div class="flex gap-1">
                    <button class="btn btn-ghost btn-xs btn-square hover:bg-indigo-100 hover:text-indigo-600" @click="showDetail(item)" title="查看详情">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                      </svg>
                    </button>
                    <button class="btn btn-ghost btn-xs btn-square hover:bg-amber-100 hover:text-amber-600" @click="showEditDialog(item)" title="编辑">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button class="btn btn-ghost btn-xs btn-square hover:bg-red-100 hover:text-red-600" @click="deleteQuestion(item.id)" title="删除">
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
      <div class="modal-box w-11/12 max-w-2xl bg-white rounded-2xl shadow-2xl">
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
          <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 rounded-full text-sm font-medium" :class="getTypeBadgeClass(currentQuestion.question_type)">{{ currentQuestion.question_type }}</span>
            <span class="px-3 py-1 rounded-full text-sm font-medium" :class="getDifficultyBadgeClass(currentQuestion.difficulty)">{{ currentQuestion.difficulty }}</span>
            <span class="px-3 py-1 rounded-full text-sm font-medium bg-slate-100 text-slate-600">{{ currentQuestion.status }}</span>
          </div>
          <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 border border-indigo-100">
            <h4 class="text-sm font-medium text-indigo-600 mb-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              题目内容
            </h4>
            <p class="text-slate-700 leading-relaxed">{{ currentQuestion.content }}</p>
          </div>
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
          <div v-if="currentQuestion.explanation" class="bg-amber-50 rounded-xl p-4 border border-amber-100">
            <h4 class="text-sm font-medium text-amber-600 mb-2 flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
              解析
            </h4>
            <p class="text-slate-700 leading-relaxed">{{ currentQuestion.explanation }}</p>
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showDetailModal = false">关闭</button>
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
      <div class="modal-box w-11/12 max-w-3xl bg-white rounded-2xl shadow-2xl">
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
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">题目内容 <span class="text-red-500">*</span></span></label>
            <textarea class="textarea textarea-bordered h-24 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.content" placeholder="请输入题目内容..."></textarea>
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">题型</span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.question_type">
                <option value="单选">📝 单选题</option>
                <option value="多选">📝 多选题</option>
                <option value="判断">✓ 判断题</option>
                <option value="填空">✏️ 填空题</option>
                <option value="主观">📄 主观题</option>
              </select>
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">难度</span></label>
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
                <option value="已发布">已发布</option>
              </select>
            </div>
          </div>
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
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">解析</span></label>
            <textarea class="textarea textarea-bordered h-20 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.explanation" placeholder="请输入题目解析..."></textarea>
          </div>
          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">标签</span></label>
            <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="form.tagsInput" placeholder="多个标签用逗号分隔，如：基础,重要,考点" />
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showEditModal = false">取消</button>
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
                题型选择
              </span></label>
              <div class="grid grid-cols-5 gap-2">
                <label v-for="type in questionTypes" :key="type.id" :class="['flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all border', aiConfig.types.includes(type.id) ? 'bg-indigo-50 border-indigo-300' : 'bg-slate-50 border-slate-100 hover:bg-indigo-50 hover:border-indigo-200']">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" v-model="aiConfig.types" :value="type.id" />
                    <span class="text-sm font-medium text-slate-700">{{ type.name }}</span>
                  </div>
                  <div v-if="aiConfig.types.includes(type.id)" class="flex items-center gap-1">
                    <button class="btn btn-xs btn-circle btn-ghost" @click.prevent="aiConfig.typeCounts[type.id] > 0 && aiConfig.typeCounts[type.id]--">-</button>
                    <input type="number" min="0" max="20" class="input input-bordered input-xs w-12 text-center" v-model.number="aiConfig.typeCounts[type.id]" />
                    <button class="btn btn-xs btn-circle btn-ghost" @click.prevent="aiConfig.typeCounts[type.id]++">+</button>
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
                  难度配置
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
                      <button class="btn btn-xs btn-circle btn-ghost" @click="aiConfig.difficultyConfig[diff.level].count > 0 && aiConfig.difficultyConfig[diff.level].count--">-</button>
                      <input type="number" min="0" max="20" class="input input-bordered input-sm w-12 text-center font-bold text-sm" v-model.number="aiConfig.difficultyConfig[diff.level].count" @input="updateDifficultyPercent" />
                      <button class="btn btn-xs btn-circle btn-ghost" @click="aiConfig.difficultyConfig[diff.level].count < 20 && aiConfig.difficultyConfig[diff.level].count++">+</button>
                      <span class="text-xs text-slate-500 w-10">{{ aiConfig.difficultyConfig[diff.level].percent }}%</span>
                    </div>
                  </div>
                  <p class="text-xs text-slate-500 leading-relaxed">{{ diff.description }}</p>
                </div>
              </div>
              <div class="mt-2 p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-between text-white">
                <span class="text-sm">总计</span>
                <span class="font-bold">{{ totalDifficultyCount }} 题</span>
              </div>
            </div>
          </div>

          <!-- 高级配置 -->
          <div class="mt-6 form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              高级配置
            </span></label>
            
            <div class="grid grid-cols-2 gap-4">
              <!-- 干扰项设置 -->
              <div class="bg-slate-50 rounded-lg p-4 border border-slate-100">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-medium text-slate-700">干扰项设置</span>
                    <div class="help-tip" @mouseenter="showHelpTip('distractor')" @mouseleave="hideHelpTip">
                      <svg class="w-4 h-4 text-indigo-500 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <div v-if="activeHelpTip === 'distractor'" class="help-tip-content">
                        干扰项是选择题中的错误选项，设计合理的干扰项能有效考察学生对知识的掌握程度
                      </div>
                    </div>
                  </div>
                  <button class="btn btn-xs btn-ghost text-indigo-600" @click="addDistractor">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    添加
                  </button>
                </div>
                <div class="space-y-2">
                  <div v-for="(item, idx) in aiConfig.distractorList" :key="idx" class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-100">
                    <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.name" placeholder="干扰项名称" />
                    <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="aiConfig.distractorList.splice(idx, 1)">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                  <div v-if="aiConfig.distractorList.length === 0" class="text-xs text-slate-400 text-center py-2">
                    点击"添加"按钮添加干扰项类型
                  </div>
                </div>
                <div class="mt-2 text-xs text-slate-500">
                  常用：常见误区型、相似概念型、部分正确型、过度概括型
                </div>
              </div>

              <!-- 内容偏好 -->
              <div class="bg-slate-50 rounded-lg p-4 border border-slate-100">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-medium text-slate-700">内容偏好</span>
                    <div class="help-tip" @mouseenter="showHelpTip('preference')" @mouseleave="hideHelpTip">
                      <svg class="w-4 h-4 text-indigo-500 cursor-help" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <div v-if="activeHelpTip === 'preference'" class="help-tip-content">
                        选择内容偏好可以让AI生成更符合您教学需求的题目
                      </div>
                    </div>
                  </div>
                  <button class="btn btn-xs btn-ghost text-indigo-600" @click="addPreference">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    添加
                  </button>
                </div>
                <div class="space-y-2">
                  <div v-for="(item, idx) in aiConfig.preferenceList" :key="idx" class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-100">
                    <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.name" placeholder="内容偏好" />
                    <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="aiConfig.preferenceList.splice(idx, 1)">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                  <div v-if="aiConfig.preferenceList.length === 0" class="text-xs text-slate-400 text-center py-2">
                    点击"添加"按钮添加内容偏好
                  </div>
                </div>
                <div class="mt-2 text-xs text-slate-500">
                  常用：结合实际案例、包含代码分析、侧重概念理解、包含调试场景
                </div>
              </div>
            </div>

            <!-- 自定义要求 -->
            <div class="mt-4">
              <label class="label"><span class="label-text font-medium text-slate-700">自定义要求</span></label>
              <textarea class="textarea textarea-bordered bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 text-sm w-full" v-model="aiConfig.custom" placeholder="输入自定义要求，如：题目需要结合Python实际编程场景..." rows="3"></textarea>
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
                      题目设计原因
                    </div>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ q.designReason }}</p>
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
  </div>
</template>

<script>
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
      stats: { total: 128, published: 95, pending: 20, draft: 13 },
      typeStats: [
        { label: '单选', value: 45, percent: 35, textClass: 'text-indigo-600', barClass: 'bg-indigo-500' },
        { label: '多选', value: 32, percent: 25, textClass: 'text-emerald-600', barClass: 'bg-emerald-500' },
        { label: '判断', value: 28, percent: 22, textClass: 'text-amber-600', barClass: 'bg-amber-500' },
        { label: '填空', value: 15, percent: 12, textClass: 'text-purple-600', barClass: 'bg-purple-500' },
        { label: '主观', value: 8, percent: 6, textClass: 'text-cyan-600', barClass: 'bg-cyan-500' }
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
        explanation: '',
        options: [
          { content: '', is_correct: false },
          { content: '', is_correct: false },
          { content: '', is_correct: false },
          { content: '', is_correct: false }
        ],
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
      aiConfig: {
        knowledgeInput: '',
        knowledgeIds: [],
        types: ['单选', '多选'],
        typeCounts: { '单选': 5, '多选': 3, '判断': 2, '填空': 0, '主观': 0 },
        difficultyConfig: {
          L1: { count: 2, percent: 20 },
          L2: { count: 3, percent: 30 },
          L3: { count: 3, percent: 30 },
          L4: { count: 1, percent: 10 },
          L5: { count: 1, percent: 10 }
        },
        distractorList: [
          { name: '常见误区型' },
          { name: '相似概念型' }
        ],
        preferenceList: [
          { name: '结合实际案例' }
        ],
        custom: ''
      },
      isGenerating: false,
      generateProgress: 0,
      generatedCount: 0,
      generatedQuestions: [],
      activeHelpTip: null
    }
  },
  computed: {
    selectedGenerated() {
      return this.generatedQuestions.filter(q => q.selected)
    },
    totalDifficultyCount() {
      return Object.values(this.aiConfig.difficultyConfig).reduce((sum, d) => sum + d.count, 0)
    },
    canStartGenerate() {
      return (this.aiConfig.knowledgeInput || this.aiConfig.knowledgeIds.length > 0) && 
             this.aiConfig.types.length > 0 && 
             this.totalDifficultyCount > 0
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
    }
  },
  mounted() {
    this.loadQuestions()
  },
  methods: {
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
        '已发布': 'text-emerald-600',
        '待审核': 'text-amber-600',
        '草稿': 'text-slate-500'
      }
      return map[status] || 'text-slate-500'
    },
    updateDifficultyPercent() {
      const total = this.totalDifficultyCount
      if (total > 0) {
        Object.keys(this.aiConfig.difficultyConfig).forEach(key => {
          this.aiConfig.difficultyConfig[key].percent = Math.round((this.aiConfig.difficultyConfig[key].count / total) * 100)
        })
      }
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
      this.questions = [
        { id: 1, content: '下列关于Python的说法，正确的是：Python是一种高级编程语言，具有简洁易学的特点。', question_type: '单选', difficulty: 'L2', status: '已发布', tags: ['基础', '重要'], selected: false },
        { id: 2, content: '以下哪些是Python的内置数据类型？请选择所有正确的选项。', question_type: '多选', difficulty: 'L2', status: '已发布', tags: ['基础'], selected: false },
        { id: 3, content: 'Python中可以使用for循环遍历列表。', question_type: '判断', difficulty: 'L1', status: '待审核', tags: ['基础'], selected: false },
        { id: 4, content: '请简述Python中列表和元组的区别。', question_type: '主观', difficulty: 'L3', status: '草稿', tags: ['进阶'], selected: false },
        { id: 5, content: 'Python中的______函数用于获取列表的长度。', question_type: '填空', difficulty: 'L1', status: '已发布', tags: ['基础'], selected: false }
      ]
      this.total = 5
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
      this.form = { id: null, content: '', question_type: '单选', difficulty: 'L2', status: '草稿', explanation: '', options: [{ content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }, { content: '', is_correct: false }], tagsInput: '' }
      this.showEditModal = true
    },
    showEditDialog(item) {
      this.isEdit = true
      this.form = { ...item, tagsInput: (item.tags || []).join(', ') }
      this.showEditModal = true
    },
    showDetail(item) {
      this.currentQuestion = item
      this.showDetailModal = true
    },
    saveQuestion() {
      this.showEditModal = false
      this.$message.success(this.isEdit ? '更新成功' : '创建成功')
      this.loadQuestions()
    },
    deleteQuestion(id) {
      this.$confirm('确定删除？', '提示', { type: 'warning' }).then(() => {
        this.$message.success('删除成功')
        this.loadQuestions()
      }).catch(() => {})
    },
    batchPublish() {
      this.$message.success(`已发布 ${this.selectedIds.length} 题`)
      this.clearSelection()
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
      
      const total = this.totalDifficultyCount
      let generated = 0
      
      const interval = setInterval(() => {
        generated++
        this.generatedCount = generated
        this.generateProgress = (generated / total) * 100
        
        const difficulties = []
        Object.keys(this.aiConfig.difficultyConfig).forEach(key => {
          for (let i = 0; i < this.aiConfig.difficultyConfig[key].count; i++) {
            difficulties.push(key)
          }
        })
        
        const diff = difficulties[generated - 1] || 'L2'
        const type = this.aiConfig.types[generated % this.aiConfig.types.length]
        const knowledge = this.aiConfig.knowledgeInput || this.knowledgeTree[this.aiConfig.knowledgeIds[generated % this.aiConfig.knowledgeIds.length] - 1]?.name || '基础知识'
        
        let questionData = {
          selected: false,
          isDraft: false,
          isDiscarded: false,
          content: '',
          question_type: type,
          difficulty: diff,
          answer: '',
          explanation: '',
          designReason: '',
          knowledgePoints: [knowledge, 'Python基础'],
          distractorReasons: []
        }
        
        if (type === '单选' || type === '多选') {
          questionData.content = `关于Python中${knowledge}的概念理解，下列说法正确的是？`
          questionData.options = [
            { content: 'Python是一种解释型语言，代码逐行执行', is_correct: true },
            { content: 'Python是一种编译型语言，需要先编译再执行', is_correct: false },
            { content: 'Python只能用于Web开发', is_correct: false },
            { content: 'Python不支持面向对象编程', is_correct: false }
          ]
          questionData.answer = type === '单选' ? 'A' : 'A,B'
          questionData.explanation = 'Python是一种解释型语言，代码在运行时由解释器逐行执行，不需要预先编译。这使得Python具有跨平台、开发效率高等特点。'
          questionData.designReason = '本题考察学生对Python语言基本特性的理解，属于L2理解层次。题目设计覆盖了解释型vs编译型语言的核心区别。'
          questionData.distractorReasons = [
            { option: 'B', reason: '常见误区型：部分学生可能混淆解释型和编译型语言的概念' },
            { option: 'C', reason: '过度概括型：学生可能因Python在Web开发中广泛应用而误以为只能用于Web' },
            { option: 'D', reason: '相似概念型：学生可能将Python与某些不支持OOP的语言混淆' }
          ]
        } else if (type === '判断') {
          questionData.content = `Python中${knowledge}的特性描述：Python是一种解释型语言。`
          questionData.answer = '正确'
          questionData.explanation = 'Python确实是解释型语言，代码在运行时由解释器逐行执行。'
          questionData.designReason = '本题考察学生对Python语言特性的判断能力，属于L1记忆层次。'
        } else if (type === '填空') {
          questionData.content = `Python中使用______函数可以获取列表的长度。`
          questionData.answer = 'len()'
          questionData.explanation = 'len()函数是Python内置函数，用于返回序列（如列表、元组、字符串）的长度。'
          questionData.designReason = '本题考察学生对Python常用内置函数的掌握，属于L1记忆层次。'
        } else if (type === '主观') {
          questionData.content = `请简述Python中${knowledge}的概念及其应用场景。`
          questionData.answer = 'Python是一种解释型、面向对象的编程语言，具有简洁易读的语法特点。应用场景包括Web开发、数据分析、人工智能、自动化脚本等领域。'
          questionData.explanation = '该题目考察学生对Python语言整体特性的理解和表达能力，需要学生综合运用所学知识进行阐述。'
          questionData.designReason = '本题考察学生对Python的综合理解能力，属于L3应用层次，要求学生能够用自己的语言描述概念并结合实际应用场景。'
        }
        
        this.generatedQuestions.push(questionData)
        
        if (generated >= total) {
          clearInterval(interval)
          this.isGenerating = false
          this.aiCurrentStep = 2
          this.$message.success('生成完成')
        }
      }, 800)
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
      this.$message.success(`已入库 ${count} 题（采纳 ${this.selectedCount} 题，草稿 ${this.draftCount} 题）`)
      this.showAIDialog = false
      this.loadQuestions()
    }
  }
}
</script>

<style scoped>
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
  padding: 8px 12px;
  background: #1e293b;
  color: white;
  font-size: 12px;
  border-radius: 8px;
  white-space: normal;
  z-index: 1000;
  margin-bottom: 8px;
  width: max-content;
  max-width: 280px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.help-tip-content::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: #1e293b;
}

.modal-box {
  overflow-x: hidden;
}

.modal-box::-webkit-scrollbar {
  width: 6px;
}

.modal-box::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.modal-box::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.modal-box::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
