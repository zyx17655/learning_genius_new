<template>
  <div class="p-8">
    <main>
      <section class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-800 mb-1">规则管理</h1>
            <p class="text-sm text-slate-500">定义AI出题提示词模板，精准控制生题质量</p>
          </div>
          <div class="flex gap-3">
            <button class="btn bg-slate-800 hover:bg-slate-700 border-0 text-white shadow-md" @click="openAnalysisDialog">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              试题分析生成规则
            </button>
            <button class="btn bg-slate-700 hover:bg-slate-600 border-0 text-white shadow-md" @click="openCreateDialog">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              新建规则
            </button>
          </div>
        </div>
      </section>

      <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="space-y-4">
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100 bg-slate-50">
              <div class="flex items-center gap-2 text-slate-700 font-semibold">
                <svg class="w-5 h-5 text-slate-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                默认规则
                <span class="ml-auto text-xs text-slate-400 font-normal">通用模板</span>
              </div>
            </div>
            <div class="card-body" style="padding: 12px;">
              <div v-if="defaultRule" :class="['rule-item', selectedRule?.id === defaultRule.id ? 'rule-item-active' : '']" @click="selectRule(defaultRule)">
                <div class="rule-item-header">
                  <span class="tag-new tag-primary">系统默认</span>
                  <span class="rule-item-meta">不可删除</span>
                </div>
                <h4 class="rule-item-title">{{ defaultRule.name }}</h4>
                <p class="rule-item-desc">{{ defaultRule.description }}</p>
                <div class="rule-item-footer">
                  <span class="rule-item-stat">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    使用 {{ defaultRule.useCount }} 次
                  </span>
                </div>
              </div>
              <div v-else class="loading-new">
                <div class="spinner"></div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100 bg-slate-50">
              <div class="flex items-center gap-2 text-slate-700 font-semibold">
                <svg class="w-5 h-5 text-slate-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
                自定义规则
                <span class="ml-auto text-xs text-slate-400 font-normal">{{ customRules.length }} 条</span>
              </div>
            </div>
            <div class="card-body" style="padding: 12px; max-height: 500px; overflow-y: auto;">
              <div v-if="customRules.length === 0" class="empty-state-new" style="padding: 32px;">
                <svg class="empty-icon" style="width: 48px; height: 48px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                <p class="empty-title">暂无自定义规则</p>
                <p class="empty-desc">点击右上角"新建规则"创建</p>
              </div>
              <div v-for="rule in customRules" :key="rule.id" :class="['rule-item', selectedRule?.id === rule.id ? 'rule-item-active-custom' : '']" @click="selectRule(rule)">
                <div class="rule-item-header">
                  <span :class="['tag-new', rule.status === '启用' ? 'tag-success' : 'tag-error']">{{ rule.status }}</span>
                  <span class="rule-item-meta">{{ rule.createdAt }}</span>
                </div>
                <h4 class="rule-item-title">{{ rule.name }}</h4>
                <p class="rule-item-desc">{{ rule.description }}</p>
                <div class="rule-item-footer">
                  <span class="rule-item-stat">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                    </svg>
                    {{ rule.scene || '通用场景' }}
                  </span>
                  <span class="rule-item-stat">
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

        <div class="lg:col-span-2">
          <div v-if="!selectedRule" class="bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 h-96 flex items-center justify-center">
            <div class="text-center">
              <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              <p class="text-slate-500 font-medium">请选择左侧规则查看详情</p>
              <p class="text-slate-400 text-sm mt-1">点击规则卡片可查看和编辑规则内容</p>
            </div>
          </div>

          <div v-else class="bg-white rounded-2xl shadow-lg shadow-slate-200/50 border border-slate-100 overflow-hidden">
            <div class="card-header bg-gradient-to-r from-slate-50 to-slate-100 px-4 py-3 border-b border-slate-100">
              <div class="rule-detail-header">
                <div class="rule-detail-title">
                  <span :class="['tag-new', selectedRule.isDefault ? 'tag-primary' : 'tag-success']">
                    {{ selectedRule.isDefault ? '默认规则' : '自定义规则' }}
                  </span>
                  <h3>{{ selectedRule.name }}</h3>
                </div>
                <div class="rule-detail-actions">
                  <button class="btn-new btn-sm-new btn-ghost-new" @click="previewPrompt">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    预览提示词
                  </button>
                  <button v-if="!selectedRule.isDefault" class="btn-new btn-sm-new" style="color: #dc2626; border-color: #fecaca; background: #fef2f2;" @click="deleteRule(selectedRule)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    删除
                  </button>
                  <button class="btn-new btn-sm-new btn-primary-new" @click="editRule(selectedRule)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    编辑规则
                  </button>
                </div>
              </div>
            </div>

            <div class="card-body" style="max-height: calc(100vh - 280px); overflow-y: auto;">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-label">规则名称</div>
                  <div class="detail-value">{{ selectedRule.name }}</div>
                </div>
                <div class="detail-item">
                  <div class="detail-label">适用场景</div>
                  <div class="detail-value">{{ selectedRule.scene || '通用场景' }}</div>
                </div>
                <div class="detail-item">
                  <div class="detail-label">规则状态</div>
                  <div :class="['detail-value', selectedRule.status === '启用' ? 'text-success' : 'text-muted']">{{ selectedRule.status }}</div>
                </div>
              </div>

              <div class="detail-section">
                <div class="detail-label">规则描述</div>
                <p class="detail-text">{{ selectedRule.description }}</p>
              </div>

              <div class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                  角色设定 (Role)
                </div>
                <div class="detail-block-content">
                  <p class="detail-text-pre">{{ selectedRule.role }}</p>
                </div>
              </div>

              <div v-if="selectedRule.isDefault && selectedRule.corePrinciples?.length" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                  </svg>
                  核心原则 (Core Principles)
                </div>
                <div class="detail-list">
                  <div v-for="(principle, idx) in selectedRule.corePrinciples" :key="idx" class="detail-list-item">
                    <span class="detail-list-number">{{ idx + 1 }}</span>
                    <div>
                      <div class="detail-list-title">{{ principle.title }}</div>
                      <div class="detail-list-desc">{{ principle.content }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.isDefault && selectedRule.workflow?.length" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  工作流程 (Workflow)
                </div>
                <div class="detail-list">
                  <div v-for="(step, idx) in selectedRule.workflow" :key="idx" class="detail-list-item">
                    <span class="detail-list-number">{{ idx + 1 }}</span>
                    <div>
                      <div class="detail-list-title">{{ step.title }}</div>
                      <div class="detail-list-desc">{{ step.content }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.isDefault && selectedRule.specifications?.length" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  命题核心规范 (Specifications)
                </div>
                <div class="detail-list">
                  <div v-for="(spec, idx) in selectedRule.specifications" :key="idx" class="detail-list-item-simple">
                    <div class="detail-list-title">{{ spec.title }}</div>
                    <div class="detail-list-desc-pre">{{ spec.content }}</div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.isDefault && selectedRule.distractorMechanics?.length" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  干扰项设置 (Distractor Mechanics)
                </div>
                <div class="detail-list">
                  <div v-for="(item, idx) in selectedRule.distractorMechanics" :key="idx" class="detail-list-item-simple">
                    <div class="detail-list-title">{{ item.type }}</div>
                    <div class="detail-list-desc">{{ item.description }}</div>
                  </div>
                </div>
              </div>

              <div v-if="selectedRule.isDefault && selectedRule.domainSkills?.length" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                  </svg>
                  专项技能 (Domain Skills)
                </div>
                <div class="detail-list">
                  <div v-for="(skill, idx) in selectedRule.domainSkills" :key="idx" class="detail-list-item-simple">
                    <div class="detail-list-title">{{ skill.title }}</div>
                    <div class="detail-list-desc">{{ skill.content }}</div>
                  </div>
                </div>
              </div>

              <div v-if="!selectedRule.isDefault && selectedRule.notationConvention" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                  </svg>
                  学科表达与符号习惯 (Notation & Convention)
                </div>
                <div class="detail-block-content">
                  <p class="detail-text-pre"><latex-renderer :content="selectedRule.notationConvention" /></p>
                </div>
              </div>

              <div v-if="!selectedRule.isDefault && selectedRule.assessmentFocus" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                  </svg>
                  考察偏好与方法论 (Assessment Focus)
                </div>
                <div class="detail-block-content">
                  <p class="detail-text-pre"><latex-renderer :content="selectedRule.assessmentFocus" /></p>
                </div>
              </div>

              <div v-if="!selectedRule.isDefault && selectedRule.subjectTraps" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                  </svg>
                  干扰项逻辑陷阱 (Subject-Specific Traps)
                </div>
                <div class="detail-block-content">
                  <p class="detail-text-pre"><latex-renderer :content="selectedRule.subjectTraps" /></p>
                </div>
              </div>

              <div v-if="!selectedRule.isDefault && selectedRule.stemStyle" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                  </svg>
                  语言风格与题干结构 (Stem Style)
                </div>
                <div class="detail-block-content">
                  <p class="detail-text-pre"><latex-renderer :content="selectedRule.stemStyle" /></p>
                </div>
              </div>

              <div v-if="!selectedRule.isDefault && selectedRule.solutionBlueprint" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  解析深度与标准 (Solution Blueprint)
                </div>
                <div class="detail-block-content">
                  <p class="detail-text-pre"><latex-renderer :content="selectedRule.solutionBlueprint" /></p>
                </div>
              </div>

              <div v-if="selectedRule.isDefault && selectedRule.outputTemplate" class="detail-block detail-block-slate">
                <div class="detail-block-title">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  输出标准模板 (Output Template)
                </div>
                <div class="detail-block-content">
                  <pre class="detail-code">{{ selectedRule.outputTemplate }}</pre>
                </div>
              </div>

              <div class="detail-meta">
                <div><span>创建时间：</span>{{ selectedRule.createdAt }}</div>
                <div><span>更新时间：</span>{{ selectedRule.updatedAt }}</div>
                <div><span>创建人：</span>{{ selectedRule.creator }}</div>
                <div><span>使用次数：</span>{{ selectedRule.useCount || 0 }} 次</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 创建/编辑规则对话框 -->
    <div v-if="showCreateDialog" class="modal-overlay" @click.self="showCreateDialog = false">
      <div class="modal-content" style="max-width: 900px; width: 95%;">
        <div class="modal-header">
          <h3 class="modal-title" style="display: flex; align-items: center; gap: 8px;">
            <svg class="w-5 h-5" style="color: #1a1a2e; flex-shrink: 0;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            {{ isEdit ? '编辑规则' : '新建规则' }}
          </h3>
          <button class="modal-close" @click="showCreateDialog = false">✕</button>
        </div>
        <div class="modal-body" style="max-height: 65vh; overflow-y: auto;">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">规则名称 <span class="text-error">*</span></label>
              <input type="text" class="form-input" v-model="ruleForm.name" placeholder="输入规则名称" />
            </div>
            <div class="form-group">
              <label class="form-label">适用场景</label>
              <input type="text" class="form-input" v-model="ruleForm.scene" placeholder="如：信号与系统、Python基础" />
            </div>
            <div class="form-group">
              <label class="form-label">规则状态</label>
              <select class="form-select" v-model="ruleForm.status">
                <option value="启用">启用</option>
                <option value="禁用">禁用</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">规则描述</label>
            <textarea class="form-textarea" v-model="ruleForm.description" placeholder="简要描述规则的适用场景和特点" rows="2"></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">
              <svg class="w-4 h-4" style="color: #1a1a2e; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              角色设定 (Role) <span class="text-error">*</span>
            </label>
            <textarea class="form-textarea" v-model="ruleForm.role" placeholder="定义AI的角色身份，如：你是一位拥有深厚学术背景的大学教授及教务命题专家..." rows="4"></textarea>
          </div>

          <template v-if="ruleForm.isDefault">
            <div class="form-divider">默认规则维度</div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #f59e0b; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                </svg>
                核心原则 (Core Principles)
              </label>
              <div class="form-list">
                <div v-for="(item, idx) in ruleForm.corePrinciples" :key="idx" class="form-list-item">
                  <div class="form-list-header">
                    <span class="detail-list-number" style="background: #f59e0b;">{{ idx + 1 }}</span>
                    <input type="text" class="form-input form-input-sm" v-model="item.title" placeholder="原则标题，如：学术标准" />
                    <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="ruleForm.corePrinciples.splice(idx, 1)">✕</button>
                  </div>
                  <textarea class="form-textarea" v-model="item.content" placeholder="原则详细内容" rows="2"></textarea>
                </div>
                <button class="btn-new btn-ghost-new" style="width: 100%;" @click="ruleForm.corePrinciples.push({ title: '', content: '' })">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  添加核心原则
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #9333ea; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                工作流程 (Workflow)
              </label>
              <div class="form-list">
                <div v-for="(item, idx) in ruleForm.workflow" :key="idx" class="form-list-item">
                  <div class="form-list-header">
                    <span class="detail-list-number" style="background: #9333ea;">{{ idx + 1 }}</span>
                    <input type="text" class="form-input form-input-sm" v-model="item.title" placeholder="步骤标题，如：知识拆解" />
                    <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="ruleForm.workflow.splice(idx, 1)">✕</button>
                  </div>
                  <textarea class="form-textarea" v-model="item.content" placeholder="步骤详细内容" rows="2"></textarea>
                </div>
                <button class="btn-new btn-ghost-new" style="width: 100%;" @click="ruleForm.workflow.push({ title: '', content: '' })">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  添加工作流程
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #06b6d4; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                命题核心规范 (Specifications)
              </label>
              <div class="form-list">
                <div v-for="(item, idx) in ruleForm.specifications" :key="idx" class="form-list-item">
                  <div class="form-list-header">
                    <input type="text" class="form-input form-input-sm" v-model="item.title" placeholder="规范标题，如：数学与参数鲁棒性" />
                    <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="ruleForm.specifications.splice(idx, 1)">✕</button>
                  </div>
                  <textarea class="form-textarea" v-model="item.content" placeholder="规范详细内容" rows="3"></textarea>
                </div>
                <button class="btn-new btn-ghost-new" style="width: 100%;" @click="ruleForm.specifications.push({ title: '', content: '' })">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  添加命题规范
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #e11d48; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                干扰项设置 (Distractor Mechanics)
              </label>
              <div class="form-list">
                <div v-for="(item, idx) in ruleForm.distractorMechanics" :key="idx" class="form-list-item">
                  <div class="form-list-header">
                    <input type="text" class="form-input form-input-sm" v-model="item.type" placeholder="干扰项类型，如：时移陷阱" />
                    <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="ruleForm.distractorMechanics.splice(idx, 1)">✕</button>
                  </div>
                  <textarea class="form-textarea" v-model="item.description" placeholder="干扰项设计原则和注意事项" rows="2"></textarea>
                </div>
                <button class="btn-new btn-ghost-new" style="width: 100%;" @click="ruleForm.distractorMechanics.push({ type: '', description: '' })">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  添加干扰项设置
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #10b981; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
                专项技能 (Domain Skills)
              </label>
              <div class="form-list">
                <div v-for="(item, idx) in ruleForm.domainSkills" :key="idx" class="form-list-item">
                  <div class="form-list-header">
                    <input type="text" class="form-input form-input-sm" v-model="item.title" placeholder="技能标题，如：时域分析" />
                    <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="ruleForm.domainSkills.splice(idx, 1)">✕</button>
                  </div>
                  <textarea class="form-textarea" v-model="item.content" placeholder="技能详细内容" rows="2"></textarea>
                </div>
                <button class="btn-new btn-ghost-new" style="width: 100%;" @click="ruleForm.domainSkills.push({ title: '', content: '' })">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  添加专项技能
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #64748b; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                输出标准模板 (Output Template)
              </label>
              <textarea class="form-textarea" v-model="ruleForm.outputTemplate" placeholder="定义输出的标准格式模板..." rows="6" style="font-family: monospace;"></textarea>
            </div>
          </template>

          <template v-else>
            <div class="form-divider">自定义规则专属维度</div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #3b82f6; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                </svg>
                学科表达与符号习惯 (Notation & Convention) - 可选
              </label>
              <textarea class="form-textarea" v-model="ruleForm.notationConvention" placeholder="特定的物理量符号（如信号处理中的 $j$ vs $i$）、公式表示法（算子法 vs 变换法）、计算结果的精度要求（保留根号、π还是四舍五入）..." rows="4"></textarea>
              <div class="form-hint">保证生成的题目在视觉和表达上与用户习惯的教材高度统一</div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #8b5cf6; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                </svg>
                考察偏好与方法论 (Assessment Focus) - 可选
              </label>
              <textarea class="form-textarea" v-model="ruleForm.assessmentFocus" placeholder="该卷子侧重于数学推导、图形解析还是数值计算？是否有特定定理的出题执念（如必考收敛域判别）..." rows="4"></textarea>
              <div class="form-hint">确保 AI 能够从知识素材中挖掘出用户真正感兴趣的命题切入点</div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #f97316; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
                干扰项逻辑陷阱 (Subject-Specific Traps) - 可选
              </label>
              <textarea class="form-textarea" v-model="ruleForm.subjectTraps" placeholder="提取该学科、该水平段学生最容易掉进去的坑（如信号时移方向弄反、积分限写错）..." rows="4"></textarea>
              <div class="form-hint">让 AI 生成的"功能性干扰项"不再是凑数，而是精准打击知识盲区</div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #14b8a6; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/>
                </svg>
                语言风格与题干结构 (Stem Style) - 可选
              </label>
              <textarea class="form-textarea" v-model="ruleForm.stemStyle" placeholder="是简洁的指令式（已知...求...）还是复杂的情境式（某系统在...环境下...）..." rows="4"></textarea>
              <div class="form-hint">保持与原卷一致的语感</div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <svg class="w-4 h-4" style="color: #ec4899; display: inline;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                解析深度与标准 (Solution Blueprint) - 可选
              </label>
              <textarea class="form-textarea" v-model="ruleForm.solutionBlueprint" placeholder="解析中是否需要列出所有中间公式？是否需要说明物理意义？是否需要总结解题技巧？..." rows="4"></textarea>
              <div class="form-hint">确保生成的答案解析符合用户的教学要求</div>
            </div>
          </template>
        </div>
        <div class="modal-footer">
          <button class="btn-new btn-ghost-new" @click="showCreateDialog = false">取消</button>
          <button class="btn-new btn-primary-new" @click="saveRule" :disabled="saving">
            <span v-if="saving" class="spinner" style="width: 16px; height: 16px; border-width: 2px;"></span>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 预览提示词对话框 -->
    <div v-if="showPreviewDialog" class="modal-overlay" @click.self="showPreviewDialog = false">
      <div class="modal-content" style="max-width: 800px;">
        <div class="modal-header">
          <h3 class="modal-title">
            <svg class="w-5 h-5" style="color: #06b6d4;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            AI提示词预览
          </h3>
          <button class="modal-close" @click="showPreviewDialog = false">✕</button>
        </div>
        <div class="modal-body">
          <div style="background: #1a1a2e; border-radius: 8px; padding: 16px; max-height: 60vh; overflow-y: auto;">
            <pre style="color: #4ade80; font-size: 13px; white-space: pre-wrap; font-family: monospace; margin: 0;">{{ previewPromptText }}</pre>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-new btn-ghost-new" @click="showPreviewDialog = false">关闭</button>
          <button class="btn-new btn-primary-new" @click="copyPrompt">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
            </svg>
            复制提示词
          </button>
        </div>
      </div>
    </div>

    <!-- 试题分析生成规则对话框 -->
    <div v-if="showAnalysisDialog" class="modal-overlay" @click.self="closeAnalysisDialog">
      <div class="modal-content" style="max-width: 1000px; height: 85vh; display: flex; flex-direction: column;">
        <div class="modal-header">
          <h3 class="modal-title">
            <svg class="w-5 h-5" style="color: #1a1a2e;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            试题分析生成规则
          </h3>
          <button class="modal-close" @click="closeAnalysisDialog">✕</button>
        </div>

        <!-- 步骤指示器 -->
        <div style="display: flex; flex-direction: column; align-items: center; padding: 20px;">
          <div style="display: flex; align-items: center;">
            <div :style="{ width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', background: analysisStep >= 0 ? '#1a1a2e' : '#e2e8f0', color: analysisStep >= 0 ? 'white' : '#64748b' }">1</div>
            <div :style="{ width: '80px', height: '4px', background: analysisStep >= 1 ? '#1a1a2e' : '#e2e8f0', margin: '0 8px' }"></div>
            <div :style="{ width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', background: analysisStep >= 1 ? '#1a1a2e' : '#e2e8f0', color: analysisStep >= 1 ? 'white' : '#64748b' }">2</div>
            <div :style="{ width: '80px', height: '4px', background: analysisStep >= 2 ? '#1a1a2e' : '#e2e8f0', margin: '0 8px' }"></div>
            <div :style="{ width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', background: analysisStep >= 2 ? '#1a1a2e' : '#e2e8f0', color: analysisStep >= 2 ? 'white' : '#64748b' }">3</div>
          </div>
          <div style="display: flex; gap: 48px; margin-top: 12px; font-size: 14px;">
            <span :style="{ color: analysisStep === 0 ? '#1a1a2e' : '#94a3b8', fontWeight: analysisStep === 0 ? '600' : 'normal' }">上传试题</span>
            <span :style="{ color: analysisStep === 1 ? '#1a1a2e' : '#94a3b8', fontWeight: analysisStep === 1 ? '600' : 'normal' }">智能分析</span>
            <span :style="{ color: analysisStep === 2 ? '#1a1a2e' : '#94a3b8', fontWeight: analysisStep === 2 ? '600' : 'normal' }">规则审核</span>
          </div>
        </div>

        <!-- 步骤1：上传试题 -->
        <div v-if="analysisStep === 0" style="flex: 1; display: flex; flex-direction: column; padding: 0 20px 20px;">
          <div class="detail-block detail-block-slate" style="margin-bottom: 16px;">
            <div class="detail-block-title">功能说明</div>
            <p class="detail-text">上传已有试题文件，系统将自动分析试题特征，提取出题原则、质量标准等信息，生成对应的出题规则提示词模板。</p>
          </div>
          
          <div style="flex: 1; display: flex; gap: 16px;">
            <div style="flex: 1;">
              <div :style="{ border: '2px dashed', borderRadius: '16px', padding: '32px', textAlign: 'center', cursor: 'pointer', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', borderColor: analysisFiles.length > 0 ? '#1a1a2e' : '#cbd5e1', background: analysisFiles.length > 0 ? 'rgba(26, 26, 46, 0.05)' : 'transparent' }" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleFileDrop">
                <input type="file" ref="fileInput" class="hidden" accept=".xlsx,.xls,.docx,.doc,.txt,.pdf" multiple @change="handleFileSelect" />
                <div style="width: 64px; height: 64px; margin: '0 auto 16px', borderRadius: '16px', background: 'linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }">
                  <svg class="w-8 h-8" style="color: #1a1a2e;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                  </svg>
                </div>
                <p v-if="analysisFiles.length > 0" style="fontWeight: 500; color: '#1e293b'; marginBottom: '8px'">已选择 {{ analysisFiles.length }} 个文件</p>
                <p v-else style="fontWeight: 500; color: '#1e293b'; marginBottom: '4px'">点击或拖拽文件到此处上传</p>
                <p style="fontSize: '14px', color: '#64748b'">支持 Excel、Word、PDF、TXT 格式，可多选</p>
              </div>
            </div>
            <div style="width: 320px; background: '#f8fafc', borderRadius: '12px', padding: '16px', border: '1px solid #e2e8f0' }">
              <div style="fontWeight: 500; color: '#1e293b', marginBottom: '12px'">已选文件</div>
              <div style="maxHeight: '300px', overflowY: 'auto' }">
                <div v-if="analysisFiles.length === 0" style="textAlign: 'center', padding: '32px', color: '#94a3b8'">
                  <p style="fontSize: '14px'">暂未选择文件</p>
                </div>
                <div v-for="(file, idx) in analysisFiles" :key="idx" style="display: 'flex', alignItems: 'center', gap: '8px', padding: '8px', background: 'white', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '8px' }">
                  <svg class="w-5 h-5" style="color: #1a1a2e; flex-shrink: 0;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <span style="fontSize: '14px', color: '#1e293b', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'">{{ file.name }}</span>
                  <button @click.stop="removeFile(idx)" style="color: '#94a3b8', cursor: 'pointer'">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div style="marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #e2e8f0' }">
                <div class="form-group">
                  <label class="form-label">规则名称 <span class="text-error">*</span></label>
                  <input type="text" class="form-input form-input-sm" v-model="analysisRuleName" placeholder="为生成的规则命名" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤2：智能分析 -->
        <div v-if="analysisStep === 1" style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px;">
          <div style="width: 96px; height: 96px; borderRadius: '50%', background: 'linear-gradient(135deg, #1a1a2e 0%, #3b3b5c 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '24px', animation: 'pulse 2s infinite' }">
            <svg class="w-12 h-12" style="color: white; animation: spin 1s linear infinite;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
          <h4 style="fontSize: '20px', fontWeight: 600, color: '#1e293b', marginBottom: '8px'">AI正在分析试题特征...</h4>
          <div style="width: 320px; height: 12px; background: '#e2e8f0', borderRadius: '6px', overflow: 'hidden', marginBottom: '16px' }">
            <div :style="{ height: '100%', background: 'linear-gradient(90deg, #1a1a2e 0%, #3b3b5c 100%)', borderRadius: '6px', transition: 'width 0.3s', width: analysisProgress + '%' }"></div>
          </div>
          <div style="textAlign: 'center', color: '#64748b', fontSize: '14px' }">
            <p>正在提取试题知识点...</p>
            <p>分析出题原则与干扰项设计...</p>
            <p>生成结构化规则模板...</p>
          </div>
        </div>

        <!-- 步骤3：规则审核 -->
        <div v-if="analysisStep === 2" style="flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 0 20px 20px;">
          <div class="detail-block detail-block-success" style="margin-bottom: 16px;">
            <div style="display: 'flex', alignItems: 'center', gap: '8px', color: '#10b981' }">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span style="fontWeight: 500;">分析完成！</span>
              <span style="fontSize: '14px'">请审核以下生成的规则内容，确认无误后保存</span>
            </div>
          </div>
          <div style="flex: 1; overflow-y: auto;">
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">规则名称</label>
                <input type="text" class="form-input" v-model="ruleForm.name" />
              </div>
              <div class="form-group">
                <label class="form-label">适用场景</label>
                <input type="text" class="form-input" v-model="ruleForm.scene" />
              </div>
              <div class="form-group">
                <label class="form-label">规则状态</label>
                <select class="form-select" v-model="ruleForm.status">
                  <option value="启用">启用</option>
                  <option value="禁用">禁用</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">规则描述</label>
              <textarea class="form-textarea" v-model="ruleForm.description" placeholder="简要描述规则的适用场景和特点" rows="2"></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">角色设定 (Role)</label>
              <textarea class="form-textarea" v-model="ruleForm.role" placeholder="定义AI的角色身份" rows="3"></textarea>
            </div>

            <div class="form-divider">自定义规则专属维度</div>

            <div class="form-group">
              <label class="form-label">学科表达与符号习惯 (Notation & Convention)</label>
              <textarea class="form-textarea" v-model="ruleForm.notationConvention" placeholder="特定的物理量符号、公式表示法、计算结果的精度要求..." rows="3"></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">考察偏好与方法论 (Assessment Focus)</label>
              <textarea class="form-textarea" v-model="ruleForm.assessmentFocus" placeholder="侧重于数学推导、图形解析还是数值计算..." rows="3"></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">干扰项逻辑陷阱 (Subject-Specific Traps)</label>
              <textarea class="form-textarea" v-model="ruleForm.subjectTraps" placeholder="提取该学科学生最容易掉进去的坑..." rows="3"></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">语言风格与题干结构 (Stem Style)</label>
              <textarea class="form-textarea" v-model="ruleForm.stemStyle" placeholder="是简洁的指令式还是复杂的情境式..." rows="3"></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">解析深度与标准 (Solution Blueprint)</label>
              <textarea class="form-textarea" v-model="ruleForm.solutionBlueprint" placeholder="解析中是否需要列出所有中间公式？是否需要说明物理意义..." rows="3"></textarea>
            </div>
          </div>
        </div>

        <!-- 底部操作栏 -->
        <div class="modal-footer" style="border-top: '1px solid #e2e8f0', marginTop: 'auto' }">
          <div style="display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }">
            <div>
              <button v-if="analysisStep > 0" class="btn-new btn-ghost-new" @click="analysisStep--">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
                上一步
              </button>
            </div>
            <div style="display: 'flex', gap: '8px' }">
              <button class="btn-new btn-ghost-new" @click="closeAnalysisDialog">取消</button>
              <button v-if="analysisStep === 0" class="btn-new btn-primary-new" @click="startAnalysis" :disabled="analyzing || analysisFiles.length === 0 || !analysisRuleName">
                <span v-if="analyzing" class="spinner" style="width: 16px; height: 16px; border-width: 2px;"></span>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                {{ analyzing ? '分析中...' : '开始分析' }}
              </button>
              <button v-if="analysisStep === 2" class="btn-new btn-primary-new" style="background: '#10b981'; border-color: '#10b981';" @click="saveAnalysisRule" :disabled="saving">
                <span v-if="saving" class="spinner" style="width: 16px; height: 16px; border-width: 2px;"></span>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                {{ saving ? '保存中...' : '保存规则' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
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
        outputTemplate: '',
        notationConvention: '',
        assessmentFocus: '',
        subjectTraps: '',
        stemStyle: '',
        solutionBlueprint: ''
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
        console.log('加载的规则数据:', rules)
        this.defaultRule = rules.find(r => r.isDefault) || null
        this.customRules = rules.filter(r => !r.isDefault)
        // 确保自定义规则字段正确映射
        this.customRules = this.customRules.map(rule => ({
          ...rule,
          assessmentFocus: rule.assessment_focus || rule.assessmentFocus || '',
          subjectTraps: rule.subject_traps || rule.subjectTraps || '',
          stemStyle: rule.stem_style || rule.stemStyle || '',
          solutionBlueprint: rule.solution_blueprint || rule.solutionBlueprint || '',
          notationConvention: rule.notation_convention || rule.notationConvention || ''
        }))
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
        isDefault: false,
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
        outputTemplate: '',
        notationConvention: '',
        assessmentFocus: '',
        subjectTraps: '',
        stemStyle: '',
        solutionBlueprint: ''
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
      this.ruleForm = {
        ...JSON.parse(JSON.stringify(rule)),
        isDefault: rule.isDefault || false,
        corePrinciples: rule.corePrinciples || [],
        workflow: rule.workflow || [],
        specifications: rule.specifications || [],
        distractorMechanics: rule.distractorMechanics || [],
        domainSkills: rule.domainSkills || [],
        // 自定义规则字段映射（支持下划线和驼峰两种格式）
        notationConvention: rule.notation_convention || rule.notationConvention || '',
        assessmentFocus: rule.assessment_focus || rule.assessmentFocus || '',
        subjectTraps: rule.subject_traps || rule.subjectTraps || '',
        stemStyle: rule.stem_style || rule.stemStyle || '',
        solutionBlueprint: rule.solution_blueprint || rule.solutionBlueprint || ''
      }
      console.log('编辑规则表单数据:', this.ruleForm)
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
        let payload
        if (this.ruleForm.isDefault) {
          payload = {
            name: this.ruleForm.name,
            description: this.ruleForm.description,
            scene: this.ruleForm.scene,
            status: this.ruleForm.status,
            role: this.ruleForm.role,
            corePrinciples: this.ruleForm.corePrinciples || [],
            workflow: this.ruleForm.workflow || [],
            specifications: this.ruleForm.specifications || [],
            distractorMechanics: this.ruleForm.distractorMechanics || [],
            domainSkills: this.ruleForm.domainSkills || [],
            outputTemplate: this.ruleForm.outputTemplate || ''
          }
        } else {
          // 自定义规则：同时发送驼峰和下划线格式，确保后端能正确接收
          payload = {
            name: this.ruleForm.name,
            description: this.ruleForm.description,
            scene: this.ruleForm.scene,
            status: this.ruleForm.status,
            role: this.ruleForm.role,
            // 驼峰格式
            notationConvention: this.ruleForm.notationConvention || '',
            assessmentFocus: this.ruleForm.assessmentFocus || '',
            subjectTraps: this.ruleForm.subjectTraps || '',
            stemStyle: this.ruleForm.stemStyle || '',
            solutionBlueprint: this.ruleForm.solutionBlueprint || ''
          }
        }
        
        console.log('保存规则 payload:', payload)
        
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
              scene: res.data.rule.scene || '',
              status: res.data.rule.status || '启用',
              corePrinciples: res.data.rule.corePrinciples || [],
              workflow: res.data.rule.workflow || [],
              specifications: res.data.rule.specifications || [],
              distractorMechanics: res.data.rule.distractorMechanics || [],
              domainSkills: res.data.rule.domainSkills || [],
              // 支持下划线和驼峰两种格式
              notationConvention: res.data.rule.notation_convention || res.data.rule.notationConvention || '',
              assessmentFocus: res.data.rule.assessment_focus || res.data.rule.assessmentFocus || '',
              subjectTraps: res.data.rule.subject_traps || res.data.rule.subjectTraps || '',
              stemStyle: res.data.rule.stem_style || res.data.rule.stemStyle || '',
              solutionBlueprint: res.data.rule.solution_blueprint || res.data.rule.solutionBlueprint || ''
            }
            console.log('分析完成的规则表单:', this.ruleForm)
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
          // 同时发送驼峰和下划线格式，确保后端能正确接收
          notationConvention: this.ruleForm.notationConvention || '',
          assessmentFocus: this.ruleForm.assessmentFocus || '',
          subjectTraps: this.ruleForm.subjectTraps || '',
          stemStyle: this.ruleForm.stemStyle || '',
          solutionBlueprint: this.ruleForm.solutionBlueprint || ''
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
      
      if (!rule.isDefault) {
        if (rule.notationConvention) {
          prompt += `\n# Notation & Convention\n${rule.notationConvention}\n`
        }
        if (rule.assessmentFocus) {
          prompt += `\n# Assessment Focus\n${rule.assessmentFocus}\n`
        }
        if (rule.subjectTraps) {
          prompt += `\n# Subject-Specific Traps\n${rule.subjectTraps}\n`
        }
        if (rule.stemStyle) {
          prompt += `\n# Stem Style\n${rule.stemStyle}\n`
        }
        if (rule.solutionBlueprint) {
          prompt += `\n# Solution Blueprint\n${rule.solutionBlueprint}\n`
        }
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
@import '../assets/styles/variables.less';

.main-content {
  padding: @spacing-xl;
}

.welcome-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.welcome-actions {
  display: flex;
  gap: @spacing-md;
}

// 规则布局
.rules-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: @spacing-xl;
}

.rules-sidebar {
  display: flex;
  flex-direction: column;
  gap: @spacing-lg;
}

.rules-main {
  min-height: 600px;
}

// 规则项
.rule-item {
  padding: @spacing-md;
  border-radius: @radius-lg;
  cursor: pointer;
  transition: all @transition-fast;
  border: 2px solid transparent;
  background: @bg-card;
  margin-bottom: @spacing-sm;

  &:hover {
    border-color: @border-color;
    background: @bg-hover;
  }

  &.rule-item-active {
    border-color: @primary-color;
    background: fade(@primary-color, 5%);
    box-shadow: @shadow-sm;
  }

  &.rule-item-active-custom {
    border-color: @primary-color;
    background: fade(@primary-color, 5%);
    box-shadow: @shadow-sm;
  }
}

.rule-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: @spacing-sm;
}

.rule-item-meta {
  font-size: @font-size-xs;
  color: @text-muted;
}

.rule-item-title {
  font-weight: 600;
  color: @text-primary;
  margin-bottom: @spacing-xs;
  font-size: @font-size-md;
}

.rule-item-desc {
  font-size: @font-size-sm;
  color: @text-secondary;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.rule-item-footer {
  display: flex;
  gap: @spacing-md;
  margin-top: @spacing-sm;
}

.rule-item-stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: @font-size-xs;
  color: @text-muted;
}

// 规则详情
.rule-detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.rule-detail-title {
  display: flex;
  align-items: center;
  gap: @spacing-md;

  h3 {
    font-size: @font-size-lg;
    font-weight: 600;
    color: @text-primary;
    margin: 0;
  }
}

.rule-detail-actions {
  display: flex;
  gap: @spacing-sm;
}

// 详情网格
.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: @spacing-md;
  margin-bottom: @spacing-lg;
}

.detail-item {
  background: @bg-hover;
  border-radius: @radius-md;
  padding: @spacing-md;
  border: 1px solid @border-light;
}

.detail-label {
  font-size: @font-size-sm;
  color: @text-secondary;
  margin-bottom: @spacing-xs;
}

.detail-value {
  font-weight: 600;
  color: @text-primary;

  &.text-success {
    color: @success-color;
  }

  &.text-muted {
    color: @text-muted;
  }
}

.detail-text {
  color: @text-primary;
  line-height: 1.6;
  margin: 0;
}

.detail-text-pre {
  color: @text-primary;
  line-height: 1.6;
  white-space: pre-wrap;
  margin: 0;
}

.detail-section {
  background: @bg-hover;
  border-radius: @radius-md;
  padding: @spacing-md;
  border: 1px solid @border-light;
  margin-bottom: @spacing-lg;
}

// 详情块
.detail-block {
  border-radius: @radius-lg;
  padding: @spacing-md;
  margin-bottom: @spacing-lg;
  background: white;

  &.detail-block-slate {
    background: linear-gradient(135deg, #f1f5f9 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;

    .detail-block-title {
      color: #475569;
    }
  }

  &.detail-block-amber {
    background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%);
    border: 1px solid #fde68a;

    .detail-block-title {
      color: #b45309;
    }
  }

  &.detail-block-slate-secondary {
    background: linear-gradient(135deg, #f1f5f9 0%, #f8fafc 100%);
    border: 1px solid #e2e8f0;

    .detail-block-title {
      color: #64748b;
    }
  }

  &.detail-block-cyan {
    background: linear-gradient(135deg, #cffafe 0%, #f0fdfa 100%);
    border: 1px solid #a5f3fc;

    .detail-block-title {
      color: #0e7490;
    }
  }

  &.detail-block-rose {
    background: linear-gradient(135deg, #ffe4e6 0%, #fff1f2 100%);
    border: 1px solid #fecdd3;

    .detail-block-title {
      color: #be123c;
    }
  }

  &.detail-block-emerald {
    background: linear-gradient(135deg, #d1fae5 0%, #ecfdf5 100%);
    border: 1px solid #a7f3d0;

    .detail-block-title {
      color: #047857;
    }
  }

  &.detail-block-blue {
    background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
    border: 1px solid #bfdbfe;

    .detail-block-title {
      color: #1d4ed8;
    }
  }

  &.detail-block-violet {
    background: linear-gradient(135deg, #ede9fe 0%, #f5f3ff 100%);
    border: 1px solid #ddd6fe;

    .detail-block-title {
      color: #6d28d9;
    }
  }

  &.detail-block-orange {
    background: linear-gradient(135deg, #ffedd5 0%, #fff7ed 100%);
    border: 1px solid #fed7aa;

    .detail-block-title {
      color: #c2410c;
    }
  }

  &.detail-block-teal {
    background: linear-gradient(135deg, #99f6e4 0%, #f0fdfa 100%);
    border: 1px solid #5eead4;

    .detail-block-title {
      color: #115e59;
    }
  }

  &.detail-block-pink {
    background: linear-gradient(135deg, #fce7f3 0%, #fdf2f8 100%);
    border: 1px solid #fbcfe8;

    .detail-block-title {
      color: #be185d;
    }
  }

  &.detail-block-slate {
    background: linear-gradient(135deg, #e2e8f0 0%, #f8fafc 100%);
    border: 1px solid #cbd5e1;

    .detail-block-title {
      color: #475569;
    }
  }

  &.detail-block-success {
    background: fade(#10b981, 5%);
    border: 1px solid fade(#10b981, 10%);
  }
}

.detail-block-title {
  font-size: @font-size-sm;
  font-weight: 600;
  margin-bottom: @spacing-md;
  display: flex;
  align-items: center;
  gap: @spacing-sm;
}

.detail-block-content {
  background: @bg-card;
  border-radius: @radius-md;
  padding: @spacing-md;
  border: 1px solid @border-light;
}

.detail-code {
  font-family: monospace;
  font-size: @font-size-xs;
  color: @text-primary;
  white-space: pre-wrap;
  margin: 0;
}

// 详情列表
.detail-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
}

.detail-list-item {
  display: flex;
  align-items: flex-start;
  gap: @spacing-md;
  padding: @spacing-md;
  background: @bg-card;
  border-radius: @radius-md;
  border: 1px solid @border-light;
}

.detail-list-item-simple {
  padding: @spacing-md;
  background: @bg-card;
  border-radius: @radius-md;
  border: 1px solid @border-light;
}

.detail-list-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: @font-size-xs;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.detail-list-title {
  font-weight: 600;
  color: @text-primary;
  font-size: @font-size-sm;
  margin-bottom: @spacing-xs;
}

.detail-list-desc {
  font-size: @font-size-xs;
  color: @text-secondary;
}

.detail-list-desc-pre {
  font-size: @font-size-xs;
  color: @text-secondary;
  white-space: pre-wrap;
  line-height: 1.5;
}

// 元信息
.detail-meta {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: @spacing-md;
  font-size: @font-size-sm;
  color: @text-secondary;
  background: @bg-hover;
  border-radius: @radius-md;
  padding: @spacing-md;
  border: 1px solid @border-light;

  span {
    font-weight: 600;
    color: @text-primary;
  }
}

// 表单样式
.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: @spacing-md;
  margin-bottom: @spacing-md;
}

.form-group {
  margin-bottom: @spacing-md;
}

.form-label {
  display: block;
  font-size: @font-size-sm;
  font-weight: 500;
  color: @text-primary;
  margin-bottom: @spacing-xs;

  svg {
    display: inline;
    vertical-align: middle;
    margin-right: 4px;
  }
}

.form-input {
  width: 100%;
  padding: @spacing-sm @spacing-md;
  border: 1px solid @border-color;
  border-radius: @radius-md;
  font-size: @font-size-md;
  color: @text-primary;
  background: @bg-card;
  transition: all @transition-fast;

  &:focus {
    outline: none;
    border-color: @primary-color;
    box-shadow: 0 0 0 3px fade(@primary-color, 10%);
  }

  &::placeholder {
    color: @text-light;
  }

  &.form-input-sm {
    padding: @spacing-xs @spacing-sm;
    font-size: @font-size-sm;
  }
}

.form-select {
  width: 100%;
  padding: @spacing-sm @spacing-md;
  border: 1px solid @border-color;
  border-radius: @radius-md;
  font-size: @font-size-md;
  color: @text-primary;
  background: @bg-card;
  transition: all @transition-fast;

  &:focus {
    outline: none;
    border-color: @primary-color;
    box-shadow: 0 0 0 3px fade(@primary-color, 10%);
  }
}

.form-textarea {
  width: 100%;
  padding: @spacing-sm @spacing-md;
  border: 1px solid @border-color;
  border-radius: @radius-md;
  font-size: @font-size-sm;
  color: @text-primary;
  background: @bg-card;
  transition: all @transition-fast;
  resize: vertical;

  &:focus {
    outline: none;
    border-color: @primary-color;
    box-shadow: 0 0 0 3px fade(@primary-color, 10%);
  }

  &::placeholder {
    color: @text-light;
  }
}

.form-hint {
  font-size: @font-size-xs;
  color: @text-muted;
  margin-top: @spacing-xs;
}

.form-divider {
  text-align: center;
  color: @text-muted;
  font-size: @font-size-sm;
  margin: @spacing-xl 0;
  position: relative;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    width: calc(50% - 60px);
    height: 1px;
    background: @border-light;
  }

  &::before {
    left: 0;
  }

  &::after {
    right: 0;
  }
}

// 表单列表
.form-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
}

.form-list-item {
  padding: @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
  border: 1px solid @border-light;
}

.form-list-header {
  display: flex;
  align-items: center;
  gap: @spacing-sm;
  margin-bottom: @spacing-sm;
}

// 文本颜色
.text-error {
  color: @error-color;
}

// 隐藏文件输入
.hidden {
  display: none;
}

// 动画
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

// 响应式
@media (max-width: @breakpoint-lg) {
  .rules-layout {
    grid-template-columns: 1fr;
  }

  .rules-sidebar {
    flex-direction: row;
    overflow-x: auto;

    .content-card {
      min-width: 320px;
    }
  }

  .detail-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }

  .welcome-header {
    flex-direction: column;
    gap: @spacing-md;
    align-items: flex-start;
  }
}
</style>
