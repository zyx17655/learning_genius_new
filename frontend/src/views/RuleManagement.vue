<template>
  <div>
    <main class="p-6">
      <section class="mb-6 relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 p-6 text-white shadow-xl shadow-indigo-200">
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2"></div>
        <div class="absolute bottom-0 left-1/4 w-32 h-32 bg-white/5 rounded-full translate-y-1/2"></div>
        <div class="relative z-10 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold mb-2">规则管理中心 📋</h1>
            <p class="text-indigo-100">定义AI出题提示词模板，精准控制生题质量</p>
          </div>
          <div class="flex gap-3">
            <button class="btn bg-white/20 hover:bg-white/30 border-none text-white backdrop-blur-sm" @click="openAnalysisDialog">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              试题分析生成规则
            </button>
            <button class="btn bg-white text-indigo-600 hover:bg-indigo-50 border-0 shadow-lg" @click="openCreateDialog">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              新建规则
            </button>
          </div>
        </div>
      </section>

      <section class="grid grid-cols-12 gap-6">
        <div class="col-span-4 space-y-6">
          <div class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-50 to-purple-50 px-5 py-3 border-b border-indigo-100">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <h3 class="font-semibold text-slate-700">默认规则</h3>
                <span class="ml-auto text-xs text-slate-400">通用模板</span>
              </div>
            </div>
            <div class="p-3">
              <div v-if="defaultRule" :class="['p-4 rounded-xl cursor-pointer transition-all border-2', selectedRule?.id === defaultRule.id ? 'border-indigo-500 bg-indigo-50 shadow-md' : 'border-transparent hover:border-indigo-200 hover:bg-slate-50']" @click="selectRule(defaultRule)">
                <div class="flex items-center justify-between mb-2">
                  <span class="px-2 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">系统默认</span>
                  <span class="text-xs text-slate-400">不可删除</span>
                </div>
                <h4 class="font-medium text-slate-800 mb-1">{{ defaultRule.name }}</h4>
                <p class="text-sm text-slate-500 line-clamp-2">{{ defaultRule.description }}</p>
                <div class="flex items-center gap-4 mt-3 text-xs text-slate-400">
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    使用 {{ defaultRule.useCount }} 次
                  </span>
                </div>
              </div>
              <div v-else class="text-center py-6 text-slate-400">
                <p class="text-sm">加载中...</p>
              </div>
            </div>
          </div>

          <div class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
            <div class="bg-gradient-to-r from-purple-50 to-pink-50 px-5 py-3 border-b border-purple-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                  </svg>
                  <h3 class="font-semibold text-slate-700">自定义规则</h3>
                </div>
                <span class="text-xs text-slate-400">{{ customRules.length }} 条</span>
              </div>
            </div>
            <div class="p-3 space-y-2 max-h-[500px] overflow-y-auto">
              <div v-if="customRules.length === 0" class="text-center py-8 text-slate-400">
                <svg class="w-12 h-12 mx-auto mb-2 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <p class="text-sm">暂无自定义规则</p>
                <p class="text-xs mt-1">点击右上角"新建规则"创建</p>
              </div>
              <div v-for="rule in customRules" :key="rule.id" :class="['p-4 rounded-xl cursor-pointer transition-all border-2', selectedRule?.id === rule.id ? 'border-purple-500 bg-purple-50 shadow-md' : 'border-transparent hover:border-purple-200 hover:bg-slate-50']" @click="selectRule(rule)">
                <div class="flex items-center justify-between mb-2">
                  <span :class="['px-2 py-1 rounded-full text-xs font-medium', getStatusBadgeClass(rule.status)]">{{ rule.status }}</span>
                  <span class="text-xs text-slate-400">{{ rule.createdAt }}</span>
                </div>
                <h4 class="font-medium text-slate-800 mb-1">{{ rule.name }}</h4>
                <p class="text-sm text-slate-500 line-clamp-2">{{ rule.description }}</p>
                <div class="flex items-center gap-4 mt-3 text-xs text-slate-400">
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                    </svg>
                    {{ rule.scene || '通用场景' }}
                  </span>
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    使用 {{ rule.useCount }} 次
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-span-8">
          <div v-if="!selectedRule" class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 h-full flex items-center justify-center">
            <div class="text-center text-slate-400">
              <svg class="w-16 h-16 mx-auto mb-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              <p class="text-lg font-medium">请选择左侧规则查看详情</p>
              <p class="text-sm mt-1">点击规则卡片可查看和编辑规则内容</p>
            </div>
          </div>

          <div v-else class="card bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
            <div class="bg-gradient-to-r from-slate-50 to-white px-6 py-4 border-b border-slate-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span :class="['px-3 py-1 rounded-full text-sm font-medium', selectedRule.isDefault ? 'bg-indigo-100 text-indigo-700' : 'bg-purple-100 text-purple-700']">
                    {{ selectedRule.isDefault ? '默认规则' : '自定义规则' }}
                  </span>
                  <h3 class="text-lg font-semibold text-slate-800">{{ selectedRule.name }}</h3>
                </div>
                <div class="flex gap-2">
                  <button class="btn btn-sm bg-cyan-50 hover:bg-cyan-100 text-cyan-600 border-cyan-200" @click="previewPrompt">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    预览提示词
                  </button>
                  <button v-if="!selectedRule.isDefault" class="btn btn-sm bg-red-50 hover:bg-red-100 text-red-600 border-red-200" @click="deleteRule(selectedRule)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    删除
                  </button>
                  <button class="btn btn-sm bg-indigo-500 hover:bg-indigo-600 text-white border-0" @click="editRule(selectedRule)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    编辑规则
                  </button>
                </div>
              </div>
            </div>

            <div class="p-6 space-y-6 max-h-[calc(100vh-280px)] overflow-y-auto">
              <div class="grid grid-cols-3 gap-4">
                <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
                  <div class="text-sm text-slate-500 mb-1">规则名称</div>
                  <div class="font-medium text-slate-800">{{ selectedRule.name }}</div>
                </div>
                <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
                  <div class="text-sm text-slate-500 mb-1">适用场景</div>
                  <div class="font-medium text-slate-800">{{ selectedRule.scene || '通用场景' }}</div>
                </div>
                <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
                  <div class="text-sm text-slate-500 mb-1">规则状态</div>
                  <div :class="['font-medium', selectedRule.status === '启用' ? 'text-emerald-600' : 'text-slate-500']">{{ selectedRule.status }}</div>
                </div>
              </div>

              <div class="bg-slate-50 rounded-xl p-4 border border-slate-100">
                <div class="text-sm text-slate-500 mb-2">规则描述</div>
                <p class="text-slate-700 leading-relaxed">{{ selectedRule.description }}</p>
              </div>

              <div class="bg-indigo-50 rounded-xl p-4 border border-indigo-100">
                <div class="text-sm font-medium text-indigo-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                  角色设定 (Role)
                </div>
                <div class="bg-white rounded-lg p-4 border border-indigo-100">
                  <p class="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">{{ selectedRule.role }}</p>
                </div>
              </div>

              <div class="bg-amber-50 rounded-xl p-4 border border-amber-100">
                <div class="text-sm font-medium text-amber-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                  </svg>
                  核心原则 (Core Principles)
                </div>
                <div class="space-y-2">
                  <div v-for="(principle, idx) in selectedRule.corePrinciples" :key="idx" class="flex items-start gap-3 p-3 bg-white rounded-lg border border-amber-100">
                    <span class="w-6 h-6 rounded-full bg-amber-500 text-white flex items-center justify-center text-xs font-bold flex-shrink-0">{{ idx + 1 }}</span>
                    <div>
                      <div class="font-medium text-slate-800 text-sm">{{ principle.title }}</div>
                      <div class="text-xs text-slate-500 mt-1">{{ principle.content }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="bg-purple-50 rounded-xl p-4 border border-purple-100">
                <div class="text-sm font-medium text-purple-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  工作流程 (Workflow)
                </div>
                <div class="space-y-2">
                  <div v-for="(step, idx) in selectedRule.workflow" :key="idx" class="flex items-start gap-3 p-3 bg-white rounded-lg border border-purple-100">
                    <span class="w-6 h-6 rounded-full bg-purple-500 text-white flex items-center justify-center text-xs font-bold flex-shrink-0">{{ idx + 1 }}</span>
                    <div>
                      <div class="font-medium text-slate-800 text-sm">{{ step.title }}</div>
                      <div class="text-xs text-slate-500 mt-1">{{ step.content }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.specifications?.length" class="bg-cyan-50 rounded-xl p-4 border border-cyan-100">
                <div class="text-sm font-medium text-cyan-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  命题核心规范 (Specifications)
                </div>
                <div class="space-y-2">
                  <div v-for="(spec, idx) in selectedRule.specifications" :key="idx" class="p-3 bg-white rounded-lg border border-cyan-100">
                    <div class="font-medium text-slate-800 text-sm mb-2">{{ spec.title }}</div>
                    <div class="text-xs text-slate-600 leading-relaxed whitespace-pre-wrap">{{ spec.content }}</div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.distractorMechanics?.length" class="bg-rose-50 rounded-xl p-4 border border-rose-100">
                <div class="text-sm font-medium text-rose-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  干扰项设置 (Distractor Mechanics)
                </div>
                <div class="space-y-2">
                  <div v-for="(item, idx) in selectedRule.distractorMechanics" :key="idx" class="p-3 bg-white rounded-lg border border-rose-100">
                    <div class="font-medium text-slate-800 text-sm mb-1">{{ item.type }}</div>
                    <div class="text-xs text-slate-500">{{ item.description }}</div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.domainSkills?.length" class="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
                <div class="text-sm font-medium text-emerald-600 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                  专项技能 (Domain Skills)
                </div>
                <div class="space-y-2">
                  <div v-for="(skill, idx) in selectedRule.domainSkills" :key="idx" class="p-3 bg-white rounded-lg border border-emerald-100">
                    <div class="font-medium text-slate-800 text-sm mb-1">{{ skill.title }}</div>
                    <div class="text-xs text-slate-500">{{ skill.content }}</div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.outputTemplate" class="bg-slate-100 rounded-xl p-4 border border-slate-200">
                <div class="text-sm font-medium text-slate-600 mb-2 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  输出标准模板 (Output Template)
                </div>
                <div class="bg-white rounded-lg p-4 border border-slate-200">
                  <pre class="text-xs text-slate-700 whitespace-pre-wrap font-mono">{{ selectedRule.outputTemplate }}</pre>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4 text-sm text-slate-500 bg-slate-50 rounded-xl p-4 border border-slate-100">
                <div><span class="font-medium">创建时间：</span>{{ selectedRule.createdAt }}</div>
                <div><span class="font-medium">更新时间：</span>{{ selectedRule.updatedAt }}</div>
                <div><span class="font-medium">创建人：</span>{{ selectedRule.creator }}</div>
                <div><span class="font-medium">使用次数：</span>{{ selectedRule.useCount || 0 }} 次</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <dialog :class="['modal', { 'modal-open': showCreateDialog }]">
      <div class="modal-box w-11/12 max-w-5xl bg-white rounded-2xl shadow-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            {{ isEdit ? '编辑规则' : '新建规则' }}
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showCreateDialog = false">✕</button>
        </div>
        <div class="space-y-4 max-h-[65vh] overflow-y-auto pr-2">
          <div class="grid grid-cols-3 gap-4">
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">规则名称 <span class="text-red-500">*</span></span></label>
              <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.name" placeholder="输入规则名称" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">适用场景</span></label>
              <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.scene" placeholder="如：信号与系统、Python基础" />
            </div>
            <div class="form-control">
              <label class="label"><span class="label-text font-medium text-slate-700">规则状态</span></label>
              <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.status">
                <option value="启用">启用</option>
                <option value="禁用">禁用</option>
              </select>
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-medium text-slate-700">规则描述</span></label>
            <textarea class="textarea textarea-bordered h-16 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.description" placeholder="简要描述规则的适用场景和特点"></textarea>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              角色设定 (Role) <span class="text-red-500">*</span>
            </span></label>
            <textarea class="textarea textarea-bordered h-24 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 text-sm" v-model="ruleForm.role" placeholder="定义AI的角色身份，如：你是一位拥有深厚学术背景的大学教授及教务命题专家..."></textarea>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
              </svg>
              核心原则 (Core Principles)
            </span></label>
            <div class="space-y-2">
              <div v-for="(item, idx) in ruleForm.corePrinciples" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex items-center gap-2 mb-2">
                  <span class="w-6 h-6 rounded-full bg-amber-500 text-white flex items-center justify-center text-xs font-bold">{{ idx + 1 }}</span>
                  <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="原则标题，如：学术标准" />
                  <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.corePrinciples.splice(idx, 1)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
                <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="原则详细内容" rows="2"></textarea>
              </div>
              <button class="btn btn-sm btn-ghost text-amber-600 hover:bg-amber-50 w-full" @click="ruleForm.corePrinciples.push({ title: '', content: '' })">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                添加核心原则
              </button>
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              工作流程 (Workflow)
            </span></label>
            <div class="space-y-2">
              <div v-for="(item, idx) in ruleForm.workflow" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex items-center gap-2 mb-2">
                  <span class="w-6 h-6 rounded-full bg-purple-500 text-white flex items-center justify-center text-xs font-bold">{{ idx + 1 }}</span>
                  <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="步骤标题，如：知识拆解" />
                  <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.workflow.splice(idx, 1)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
                <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="步骤详细内容" rows="2"></textarea>
              </div>
              <button class="btn btn-sm btn-ghost text-purple-600 hover:bg-purple-50 w-full" @click="ruleForm.workflow.push({ title: '', content: '' })">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                添加工作流程
              </button>
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              命题核心规范 (Specifications) - 可选
            </span></label>
            <div class="space-y-2">
              <div v-for="(item, idx) in ruleForm.specifications" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex items-center gap-2 mb-2">
                  <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="规范标题，如：数学与参数鲁棒性" />
                  <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.specifications.splice(idx, 1)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
                <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="规范详细内容" rows="3"></textarea>
              </div>
              <button class="btn btn-sm btn-ghost text-cyan-600 hover:bg-cyan-50 w-full" @click="ruleForm.specifications.push({ title: '', content: '' })">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                添加命题规范
              </button>
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              干扰项设置 (Distractor Mechanics) - 可选
            </span></label>
            <div class="space-y-2">
              <div v-for="(item, idx) in ruleForm.distractorMechanics" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex items-center gap-2 mb-2">
                  <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.type" placeholder="干扰项类型，如：时移陷阱" />
                  <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.distractorMechanics.splice(idx, 1)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
                <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.description" placeholder="干扰项设计原则和注意事项" rows="2"></textarea>
              </div>
              <button class="btn btn-sm btn-ghost text-rose-600 hover:bg-rose-50 w-full" @click="ruleForm.distractorMechanics.push({ type: '', description: '' })">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                添加干扰项设置
              </button>
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
              专项技能 (Domain Skills) - 可选
            </span></label>
            <div class="space-y-2">
              <div v-for="(item, idx) in ruleForm.domainSkills" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <div class="flex items-center gap-2 mb-2">
                  <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="技能标题，如：时域分析" />
                  <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.domainSkills.splice(idx, 1)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
                <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="技能详细内容" rows="2"></textarea>
              </div>
              <button class="btn btn-sm btn-ghost text-emerald-600 hover:bg-emerald-50 w-full" @click="ruleForm.domainSkills.push({ title: '', content: '' })">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                添加专项技能
              </button>
            </div>
          </div>

          <div class="form-control">
            <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              输出标准模板 (Output Template) - 可选
            </span></label>
            <textarea class="textarea textarea-bordered bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 text-sm font-mono" v-model="ruleForm.outputTemplate" placeholder="定义输出的标准格式模板..." rows="6"></textarea>
          </div>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showCreateDialog = false">取消</button>
          <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white shadow-lg" @click="saveRule" :disabled="saving">
            <span v-if="saving" class="loading loading-spinner loading-sm"></span>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showCreateDialog = false">close</button>
      </form>
    </dialog>

    <dialog :class="['modal', { 'modal-open': showPreviewDialog }]">
      <div class="modal-box w-11/12 max-w-4xl bg-white rounded-2xl shadow-2xl">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            AI提示词预览
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="showPreviewDialog = false">✕</button>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 max-h-[60vh] overflow-y-auto">
          <pre class="text-sm text-green-400 whitespace-pre-wrap font-mono">{{ previewPromptText }}</pre>
        </div>
        <div class="modal-action pt-4 border-t border-slate-100">
          <button class="btn btn-ghost" @click="showPreviewDialog = false">关闭</button>
          <button class="btn bg-indigo-500 hover:bg-indigo-600 text-white border-0" @click="copyPrompt">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
            </svg>
            复制提示词
          </button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="showPreviewDialog = false">close</button>
      </form>
    </dialog>

    <dialog :class="['modal', { 'modal-open': showAnalysisDialog }]">
      <div class="modal-box w-11/12 max-w-6xl bg-white rounded-2xl shadow-2xl h-[85vh] flex flex-col">
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
          <h3 class="font-bold text-lg text-slate-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            试题分析生成规则
          </h3>
          <button class="btn btn-sm btn-circle btn-ghost hover:bg-slate-100" @click="closeAnalysisDialog">✕</button>
        </div>

        <!-- 步骤指示器 -->
        <div class="flex flex-col items-center mb-6">
          <div class="flex items-center">
            <div :class="['flex items-center justify-center w-10 h-10 rounded-full font-bold text-sm transition-all', analysisStep >= 0 ? 'bg-indigo-500 text-white' : 'bg-slate-200 text-slate-500']">1</div>
            <div class="w-20 h-1 mx-2" :class="analysisStep >= 1 ? 'bg-indigo-500' : 'bg-slate-200'"></div>
            <div :class="['flex items-center justify-center w-10 h-10 rounded-full font-bold text-sm transition-all', analysisStep >= 1 ? 'bg-indigo-500 text-white' : 'bg-slate-200 text-slate-500']">2</div>
            <div class="w-20 h-1 mx-2" :class="analysisStep >= 2 ? 'bg-indigo-500' : 'bg-slate-200'"></div>
            <div :class="['flex items-center justify-center w-10 h-10 rounded-full font-bold text-sm transition-all', analysisStep >= 2 ? 'bg-indigo-500 text-white' : 'bg-slate-200 text-slate-500']">3</div>
          </div>
          <div class="flex gap-12 text-sm mt-3">
            <span :class="analysisStep === 0 ? 'text-indigo-600 font-medium' : 'text-slate-400'">上传试题</span>
            <span :class="analysisStep === 1 ? 'text-indigo-600 font-medium' : 'text-slate-400'">智能分析</span>
            <span :class="analysisStep === 2 ? 'text-indigo-600 font-medium' : 'text-slate-400'">规则审核</span>
          </div>
        </div>

        <!-- 步骤1：上传试题 -->
        <div v-if="analysisStep === 0" class="flex-1 flex flex-col">
          <div class="bg-indigo-50 rounded-xl p-4 border border-indigo-100 mb-4">
            <div class="text-sm font-medium text-indigo-600 mb-2">功能说明</div>
            <p class="text-slate-700 text-sm leading-relaxed">上传已有试题文件，系统将自动分析试题特征，提取出题原则、质量标准等信息，生成对应的出题规则提示词模板。</p>
          </div>
          
          <div class="flex-1 flex gap-4">
            <div class="flex-1">
              <div class="border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer h-full flex flex-col justify-center" :class="analysisFiles.length > 0 ? 'border-indigo-400 bg-indigo-50/50' : 'border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50/50'" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleFileDrop">
                <input type="file" ref="fileInput" class="hidden" accept=".xlsx,.xls,.docx,.doc,.txt,.pdf" multiple @change="handleFileSelect" />
                <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
                  <svg class="w-8 h-8 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                  </svg>
                </div>
                <p v-if="analysisFiles.length > 0" class="text-slate-600 font-medium mb-2">已选择 {{ analysisFiles.length }} 个文件</p>
                <p v-else class="text-slate-600 font-medium mb-1">点击或拖拽文件到此处上传</p>
                <p class="text-sm text-slate-400">支持 Excel、Word、PDF、TXT 格式，可多选</p>
              </div>
            </div>
            <div class="w-80 bg-slate-50 rounded-xl p-4 border border-slate-100">
              <div class="text-sm font-medium text-slate-700 mb-3">已选文件</div>
              <div class="space-y-2 max-h-[300px] overflow-y-auto">
                <div v-if="analysisFiles.length === 0" class="text-center py-8 text-slate-400">
                  <p class="text-sm">暂未选择文件</p>
                </div>
                <div v-for="(file, idx) in analysisFiles" :key="idx" class="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-100">
                  <svg class="w-5 h-5 text-indigo-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <span class="text-sm text-slate-700 flex-1 truncate">{{ file.name }}</span>
                  <button @click.stop="removeFile(idx)" class="text-slate-400 hover:text-red-500">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="mt-4 pt-4 border-t border-slate-200">
                <div class="form-control">
                  <label class="label"><span class="label-text font-medium text-slate-700">规则名称 <span class="text-red-500">*</span></span></label>
                  <input type="text" class="input input-bordered input-sm focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="analysisRuleName" placeholder="为生成的规则命名" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤2：智能分析 -->
        <div v-if="analysisStep === 1" class="flex-1 flex flex-col items-center justify-center">
          <div class="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center mb-6 animate-pulse">
            <svg class="w-12 h-12 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h4 class="text-xl font-semibold text-slate-700 mb-2">AI正在分析试题特征...</h4>
          <progress class="progress progress-primary w-80 h-3 mb-4" :value="analysisProgress" max="100"></progress>
          <div class="text-sm text-slate-500 space-y-1 text-center">
            <p>正在提取试题知识点...</p>
            <p>分析出题原则与干扰项设计...</p>
            <p>生成结构化规则模板...</p>
          </div>
        </div>

        <!-- 步骤3：规则审核 -->
        <div v-if="analysisStep === 2" class="flex-1 flex flex-col overflow-hidden">
          <div class="bg-emerald-50 rounded-xl p-4 border border-emerald-100 mb-4">
            <div class="flex items-center gap-2 text-emerald-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="font-medium">分析完成！</span>
              <span class="text-sm text-emerald-500">请审核以下生成的规则内容，确认无误后保存</span>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto pr-2">
            <div class="space-y-4">
              <div class="grid grid-cols-3 gap-4">
                <div class="form-control">
                  <label class="label"><span class="label-text font-medium text-slate-700">规则名称</span></label>
                  <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.name" />
                </div>
                <div class="form-control">
                  <label class="label"><span class="label-text font-medium text-slate-700">适用场景</span></label>
                  <input type="text" class="input input-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.scene" />
                </div>
                <div class="form-control">
                  <label class="label"><span class="label-text font-medium text-slate-700">规则状态</span></label>
                  <select class="select select-bordered focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.status">
                    <option value="启用">启用</option>
                    <option value="禁用">禁用</option>
                  </select>
                </div>
              </div>

              <div class="form-control">
                <label class="label"><span class="label-text font-medium text-slate-700">规则描述</span></label>
                <textarea class="textarea textarea-bordered h-16 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100" v-model="ruleForm.description" placeholder="简要描述规则的适用场景和特点"></textarea>
              </div>

              <div class="form-control">
                <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                  角色设定 (Role)
                </span></label>
                <textarea class="textarea textarea-bordered h-20 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 text-sm" v-model="ruleForm.role" placeholder="定义AI的角色身份"></textarea>
              </div>

              <div class="form-control">
                <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                  </svg>
                  核心原则 (Core Principles)
                </span></label>
                <div class="space-y-2">
                  <div v-for="(item, idx) in ruleForm.corePrinciples" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="w-6 h-6 rounded-full bg-amber-500 text-white flex items-center justify-center text-xs font-bold">{{ idx + 1 }}</span>
                      <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="原则标题" />
                      <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.corePrinciples.splice(idx, 1)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="原则详细内容" rows="2"></textarea>
                  </div>
                  <button class="btn btn-sm btn-ghost text-amber-600 hover:bg-amber-50 w-full" @click="ruleForm.corePrinciples.push({ title: '', content: '' })">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    添加核心原则
                  </button>
                </div>
              </div>

              <div class="form-control">
                <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  干扰项设置 (Distractor Mechanics)
                </span></label>
                <div class="space-y-2">
                  <div v-for="(item, idx) in ruleForm.distractorMechanics" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div class="flex items-center gap-2 mb-2">
                      <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.type" placeholder="干扰项类型" />
                      <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.distractorMechanics.splice(idx, 1)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.description" placeholder="干扰项设计原则" rows="2"></textarea>
                  </div>
                  <button class="btn btn-sm btn-ghost text-rose-600 hover:bg-rose-50 w-full" @click="ruleForm.distractorMechanics.push({ type: '', description: '' })">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    添加干扰项设置
                  </button>
                </div>
              </div>

              <div class="form-control">
                <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  数学约束与鲁棒性标准 (Specifications)
                </span></label>
                <div class="space-y-2">
                  <div v-for="(item, idx) in ruleForm.specifications" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div class="flex items-center gap-2 mb-2">
                      <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="规范标题" />
                      <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.specifications.splice(idx, 1)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="规范详细内容" rows="3"></textarea>
                  </div>
                  <button class="btn btn-sm btn-ghost text-cyan-600 hover:bg-cyan-50 w-full" @click="ruleForm.specifications.push({ title: '', content: '' })">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    添加规范
                  </button>
                </div>
              </div>

              <div class="form-control">
                <label class="label"><span class="label-text font-semibold text-slate-700 flex items-center gap-2">
                  <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                  专项命题技能 (Domain Skills)
                </span></label>
                <div class="space-y-2">
                  <div v-for="(item, idx) in ruleForm.domainSkills" :key="idx" class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <div class="flex items-center gap-2 mb-2">
                      <input type="text" class="input input-sm input-bordered flex-1 bg-white" v-model="item.title" placeholder="技能标题" />
                      <button class="btn btn-xs btn-circle btn-ghost text-red-500" @click="ruleForm.domainSkills.splice(idx, 1)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <textarea class="textarea textarea-bordered w-full bg-white text-sm" v-model="item.content" placeholder="技能详细内容" rows="2"></textarea>
                  </div>
                  <button class="btn btn-sm btn-ghost text-emerald-600 hover:bg-emerald-50 w-full" @click="ruleForm.domainSkills.push({ title: '', content: '' })">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    添加专项技能
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部操作栏 -->
        <div class="modal-action pt-4 border-t border-slate-100 mt-auto">
          <div class="flex items-center justify-between w-full">
            <div>
              <button v-if="analysisStep > 0" class="btn btn-ghost" @click="analysisStep--">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
                上一步
              </button>
            </div>
            <div class="flex gap-2">
              <button class="btn btn-ghost" @click="closeAnalysisDialog">取消</button>
              <button v-if="analysisStep === 0" class="btn bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 border-0 text-white" @click="startAnalysis" :disabled="analyzing || analysisFiles.length === 0 || !analysisRuleName">
                <span v-if="analyzing" class="loading loading-spinner loading-sm"></span>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                {{ analyzing ? '分析中...' : '开始分析' }}
              </button>
              <button v-if="analysisStep === 2" class="btn bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 border-0 text-white" @click="saveAnalysisRule" :disabled="saving">
                <span v-if="saving" class="loading loading-spinner loading-sm"></span>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                {{ saving ? '保存中...' : '保存规则' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop bg-slate-900/50">
        <button @click="closeAnalysisDialog">close</button>
      </form>
    </dialog>
  </div>
</template>

<script>
import axios from 'axios'

const API_BASE = 'http://localhost:5001/api/rule'

export default {
  name: 'RuleManagement',
  data() {
    return {
      selectedRule: null,
      showCreateDialog: false,
      showPreviewDialog: false,
      showAnalysisDialog: false,
      isEdit: false,
      saving: false,
      analyzing: false,
      analysisStep: 0,
      analysisProgress: 0,
      previewPromptText: '',
      defaultRule: null,
      customRules: [],
      analysisFiles: [],
      analysisRuleName: '',
      ruleForm: {
        id: null,
        name: '',
        description: '',
        scene: '',
        status: '启用',
        role: '',
        corePrinciples: [],
        workflow: [],
        specifications: [],
        distractorMechanics: [],
        domainSkills: [],
        outputTemplate: ''
      }
    }
  },
  mounted() {
    this.loadRules()
  },
  methods: {
    async loadRules() {
      try {
        await axios.post(`${API_BASE}/rules/init-default`)
        const res = await axios.get(`${API_BASE}/rules`)
        const rules = res.data.rules || []
        this.defaultRule = rules.find(r => r.isDefault) || null
        this.customRules = rules.filter(r => !r.isDefault)
        if (this.defaultRule && !this.selectedRule) {
          this.selectedRule = this.defaultRule
        }
      } catch (e) {
        console.error('加载规则失败:', e)
        this.$message.error('加载规则失败')
      }
    },
    selectRule(rule) {
      this.selectedRule = rule
    },
    getStatusBadgeClass(status) {
      return status === '启用' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'
    },
    openCreateDialog() {
      this.isEdit = false
      this.ruleForm = {
        id: null,
        name: '',
        description: '',
        scene: '',
        status: '启用',
        role: '',
        corePrinciples: [],
        workflow: [],
        specifications: [],
        distractorMechanics: [],
        domainSkills: [],
        outputTemplate: ''
      }
      this.showCreateDialog = true
    },
    openAnalysisDialog() {
      this.analysisFiles = []
      this.analysisRuleName = ''
      this.analysisStep = 0
      this.analysisProgress = 0
      this.showAnalysisDialog = true
    },
    closeAnalysisDialog() {
      this.showAnalysisDialog = false
      this.analysisStep = 0
      this.analysisProgress = 0
    },
    handleFileSelect(e) {
      const files = Array.from(e.target.files)
      if (files.length > 0) {
        this.analysisFiles = [...this.analysisFiles, ...files]
      }
      e.target.value = ''
    },
    handleFileDrop(e) {
      const files = Array.from(e.dataTransfer.files)
      if (files.length > 0) {
        this.analysisFiles = [...this.analysisFiles, ...files]
      }
    },
    removeFile(idx) {
      this.analysisFiles.splice(idx, 1)
    },
    editRule(rule) {
      this.isEdit = true
      this.ruleForm = JSON.parse(JSON.stringify(rule))
      this.showCreateDialog = true
    },
    async deleteRule(rule) {
      if (!confirm(`确定删除规则"${rule.name}"？`)) return
      try {
        await axios.delete(`${API_BASE}/rules/${rule.id}`)
        this.$message.success('删除成功')
        await this.loadRules()
        this.selectedRule = this.defaultRule
      } catch (e) {
        this.$message.error(e.response?.data?.detail || '删除失败')
      }
    },
    async saveRule() {
      if (!this.ruleForm.name) {
        this.$message.error('请输入规则名称')
        return
      }
      if (!this.ruleForm.role) {
        this.$message.error('请填写角色设定')
        return
      }
      
      this.saving = true
      try {
        const payload = {
          name: this.ruleForm.name,
          description: this.ruleForm.description,
          scene: this.ruleForm.scene,
          status: this.ruleForm.status,
          role: this.ruleForm.role,
          corePrinciples: this.ruleForm.corePrinciples,
          workflow: this.ruleForm.workflow,
          specifications: this.ruleForm.specifications,
          distractorMechanics: this.ruleForm.distractorMechanics,
          domainSkills: this.ruleForm.domainSkills,
          outputTemplate: this.ruleForm.outputTemplate
        }
        
        if (this.isEdit && this.ruleForm.id) {
          await axios.put(`${API_BASE}/rules/${this.ruleForm.id}`, payload)
          this.$message.success('更新成功')
        } else {
          await axios.post(`${API_BASE}/rules`, payload)
          this.$message.success('创建成功')
        }
        
        this.showCreateDialog = false
        await this.loadRules()
      } catch (e) {
        this.$message.error(e.response?.data?.detail || '保存失败')
      } finally {
        this.saving = false
      }
    },
    async startAnalysis() {
      if (this.analysisFiles.length === 0 || !this.analysisRuleName) {
        this.$message.error('请上传文件并输入规则名称')
        return
      }
      
      this.analyzing = true
      this.analysisStep = 1
      this.analysisProgress = 0
      
      const progressInterval = setInterval(() => {
        if (this.analysisProgress < 90) {
          this.analysisProgress += Math.random() * 15
        }
      }, 500)
      
      try {
        const formData = new FormData()
        this.analysisFiles.forEach(file => {
          formData.append('files', file)
        })
        formData.append('rule_name', this.analysisRuleName)
        
        const res = await axios.post(`${API_BASE}/rules/analyze`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: 180000
        })
        
        clearInterval(progressInterval)
        this.analysisProgress = 100
        
        if (res.data.success && res.data.rule) {
          setTimeout(() => {
            this.isEdit = false
            this.ruleForm = {
              ...res.data.rule,
              corePrinciples: res.data.rule.corePrinciples || [],
              workflow: res.data.rule.workflow || [],
              specifications: res.data.rule.specifications || [],
              distractorMechanics: res.data.rule.distractorMechanics || [],
              domainSkills: res.data.rule.domainSkills || []
            }
            this.analysisStep = 2
            this.$message.success('分析完成，请审核后保存')
          }, 500)
        }
      } catch (e) {
        clearInterval(progressInterval)
        this.analysisStep = 0
        this.$message.error(e.response?.data?.detail || '分析失败')
      } finally {
        this.analyzing = false
      }
    },
    async saveAnalysisRule() {
      if (!this.ruleForm.name) {
        this.$message.error('请输入规则名称')
        return
      }
      if (!this.ruleForm.role) {
        this.$message.error('请填写角色设定')
        return
      }
      
      this.saving = true
      try {
        const payload = {
          name: this.ruleForm.name,
          description: this.ruleForm.description,
          scene: this.ruleForm.scene,
          status: this.ruleForm.status,
          role: this.ruleForm.role,
          corePrinciples: this.ruleForm.corePrinciples,
          workflow: this.ruleForm.workflow,
          specifications: this.ruleForm.specifications,
          distractorMechanics: this.ruleForm.distractorMechanics,
          domainSkills: this.ruleForm.domainSkills,
          outputTemplate: this.ruleForm.outputTemplate
        }
        
        await axios.post(`${API_BASE}/rules`, payload)
        this.$message.success('规则保存成功')
        this.closeAnalysisDialog()
        await this.loadRules()
      } catch (e) {
        this.$message.error(e.response?.data?.detail || '保存失败')
      } finally {
        this.saving = false
      }
    },
    previewPrompt() {
      if (!this.selectedRule) return
      
      const rule = this.selectedRule
      let prompt = `# Role\n${rule.role}\n\n`
      
      prompt += `# Core Principles\n`
      rule.corePrinciples.forEach((p, idx) => {
        prompt += `${idx + 1}. ${p.title}：${p.content}\n`
      })
      
      prompt += `\n# Workflow\n`
      rule.workflow.forEach((w, idx) => {
        prompt += `${idx + 1}. ${w.title}：${w.content}\n`
      })
      
      if (rule.specifications?.length) {
        prompt += `\n# Specifications\n`
        rule.specifications.forEach(s => {
          prompt += `\n## ${s.title}\n${s.content}\n`
        })
      }
      
      if (rule.distractorMechanics?.length) {
        prompt += `\n# Distractor Mechanics\n`
        rule.distractorMechanics.forEach(d => {
          prompt += `- ${d.type}：${d.description}\n`
        })
      }
      
      if (rule.domainSkills?.length) {
        prompt += `\n# Domain Skills\n`
        rule.domainSkills.forEach(s => {
          prompt += `- ${s.title}：${s.content}\n`
        })
      }
      
      if (rule.outputTemplate) {
        prompt += `\n# Output Template\n${rule.outputTemplate}\n`
      }
      
      this.previewPromptText = prompt
      this.showPreviewDialog = true
    },
    copyPrompt() {
      navigator.clipboard.writeText(this.previewPromptText).then(() => {
        this.$message.success('已复制到剪贴板')
      }).catch(() => {
        this.$message.error('复制失败')
      })
    }
  }
}
</script>

<style lang="less" scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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
