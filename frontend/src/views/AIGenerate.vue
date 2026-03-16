<template>
  <div class="page-wrapper">
    <section class="welcome-section">
      <div class="welcome-header">
        <div>
          <h1 class="welcome-title">AI智能生题 🤖</h1>
          <p class="welcome-subtitle">基于知识图谱和AI算法，智能生成高质量题目</p>
        </div>
      </div>
    </section>

    <div class="generate-layout">
      <div class="generate-sidebar">
        <div class="content-card">
          <div class="card-header">
            <div class="card-title">
              <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
              </svg>
              生成配置
            </div>
          </div>
          <div class="card-body">
            <div class="form-group">
              <label class="form-label">知识范围 <span class="text-error">*</span></label>
              <div class="knowledge-tree">
                <div v-for="node in knowledgeTree" :key="node.id" class="tree-node">
                  <div class="tree-node-header" @click="node.expanded = !node.expanded">
                    <svg class="tree-icon" :class="{ 'expanded': node.expanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                    <label class="checkbox-label">
                      <input type="checkbox" :value="node.id" v-model="selectedKnowledgeIds" @click.stop />
                      <span>{{ node.label }}</span>
                    </label>
                  </div>
                  <div v-if="node.expanded && node.children" class="tree-children">
                    <div v-for="child in node.children" :key="child.id" class="tree-child">
                      <div class="tree-node-header" @click="child.expanded = !child.expanded">
                        <svg v-if="child.children" class="tree-icon" :class="{ 'expanded': child.expanded }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                        <label class="checkbox-label">
                          <input type="checkbox" :value="child.id" v-model="selectedKnowledgeIds" @click.stop />
                          <span>{{ child.label }}</span>
                        </label>
                      </div>
                      <div v-if="child.expanded && child.children" class="tree-grandchildren">
                        <label v-for="grandchild in child.children" :key="grandchild.id" class="checkbox-label tree-leaf">
                          <input type="checkbox" :value="grandchild.id" v-model="selectedKnowledgeIds" />
                          <span>{{ grandchild.label }}</span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">题型 <span class="text-error">*</span></label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" value="单选" v-model="form.question_types" />
                  <span>单选</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" value="多选" v-model="form.question_types" />
                  <span>多选</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" value="判断" v-model="form.question_types" />
                  <span>判断</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" value="填空" v-model="form.question_types" />
                  <span>填空</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" value="主观" v-model="form.question_types" />
                  <span>主观</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">难度 <span class="text-error">*</span></label>
              <div class="radio-group">
                <label class="radio-label">
                  <input type="radio" value="L1" v-model="form.difficulty" />
                  <span>L1 记忆</span>
                </label>
                <label class="radio-label">
                  <input type="radio" value="L2" v-model="form.difficulty" />
                  <span>L2 理解</span>
                </label>
                <label class="radio-label">
                  <input type="radio" value="L3" v-model="form.difficulty" />
                  <span>L3 应用</span>
                </label>
                <label class="radio-label">
                  <input type="radio" value="L4" v-model="form.difficulty" />
                  <span>L4 分析</span>
                </label>
                <label class="radio-label">
                  <input type="radio" value="L5" v-model="form.difficulty" />
                  <span>L5 创造</span>
                </label>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">题目数量 <span class="text-error">*</span></label>
              <div class="slider-wrapper">
                <input type="range" min="1" max="20" v-model="form.question_count" class="form-slider" />
                <span class="slider-value">{{ form.question_count }} 题</span>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">高级设置</label>
              <div class="advanced-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="form.advanced.distractors_based_on_misconceptions" />
                  <span>干扰项基于常见误区</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="form.advanced.combine_with_fault_cases" />
                  <span>结合实际故障案例</span>
                </label>
                <textarea class="form-textarea" v-model="form.advanced.custom_requirements" placeholder="自定义文本要求..." rows="3"></textarea>
              </div>
            </div>

            <div class="form-actions">
              <button class="btn-new btn-primary-new" @click="generateQuestions" :disabled="isGenerating" style="width: 100%;">
                <span v-if="isGenerating" class="spinner" style="width: 16px; height: 16px; border-width: 2px;"></span>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                {{ isGenerating ? '生成中...' : '开始生成' }}
              </button>
              <button v-if="isGenerating" class="btn-new btn-ghost-new" @click="cancelGeneration" style="width: 100%; margin-top: 8px;">
                取消生成
              </button>
            </div>
          </div>
        </div>

        <!-- 生成进度 -->
        <div v-if="isGenerating" class="content-card" style="margin-top: 16px;">
          <div class="card-header">
            <div class="card-title">
              <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              生成进度
            </div>
          </div>
          <div class="card-body">
            <div class="progress-wrapper">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: generationProgress + '%' }"></div>
              </div>
              <div class="progress-info">
                <span>{{ generationProgress }}%</span>
                <span>已生成: {{ generatedCount }}/{{ form.question_count }} 题</span>
              </div>
              <div v-if="generationMessage" class="progress-message" style="margin-top: 8px; font-size: 12px; color: #666;">
                {{ generationMessage }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="generate-main">
        <div v-if="generatedQuestions.length === 0" class="content-card" style="height: 100%; display: flex; align-items: center; justify-content: center;">
          <div class="empty-state-new">
            <svg class="empty-icon" style="width: 80px; height: 80px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
            <p class="empty-title">开始生成题目</p>
            <p class="empty-desc">在左侧配置生成参数，点击"开始生成"按钮</p>
          </div>
        </div>

        <div v-else class="content-card">
          <div class="card-header">
            <div class="card-title">
              <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              生成结果
              <span class="card-subtitle">共 {{ generatedQuestions.length }} 道题目</span>
            </div>
            <div class="batch-actions">
              <button class="btn-new btn-sm-new" style="color: #10b981; border-color: #a7f3d0; background: #ecfdf5;" @click="batchAdopt" :disabled="selectedQuestions.length === 0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                批量采纳
              </button>
              <button class="btn-new btn-sm-new" style="color: #dc2626; border-color: #fecaca; background: #fef2f2;" @click="batchDiscard" :disabled="selectedQuestions.length === 0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                批量丢弃
              </button>
            </div>
          </div>
          <div class="card-body" style="padding: 0;">
            <div v-for="(question, index) in generatedQuestions" :key="index" class="question-item">
              <div class="question-header">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="question.selected" @change="handleQuestionSelect" />
                  <span class="question-number">第 {{ index + 1 }} 题</span>
                </label>
                <div class="question-tags">
                  <span class="tag-new" :class="getQuestionTypeClass(question.question_type)">{{ question.question_type }}</span>
                  <span class="tag-new" :class="getDifficultyClass(question.difficulty)">{{ question.difficulty }}</span>
                </div>
              </div>
              <div class="question-body">
                <div class="question-content">
                  <latex-renderer :content="question.content" />
                </div>
                <div v-if="['单选', '多选', '判断'].includes(question.question_type)" class="question-options">
                  <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option-item" :class="{ 'correct': option.is_correct }">
                    <span class="option-label">{{ String.fromCharCode(65 + optIndex) }}.</span>
                    <latex-renderer :content="option.content" />
                  </div>
                </div>
                <div v-if="question.explanation" class="question-explanation">
                  <div class="explanation-title">解析：</div>
                  <latex-renderer :content="question.explanation" />
                </div>
                <div v-if="question.design_reason || question.difficulty_reason" class="question-interpretability">
                  <div class="interpretability-header" @click="question.showInterpretability = !question.showInterpretability">
                    <svg class="w-4 h-4" :class="{ 'expanded': question.showInterpretability }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                    <span>可解释性信息</span>
                  </div>
                  <div v-if="question.showInterpretability" class="interpretability-content">
                    <p v-if="question.design_reason"><strong>题目设计依据：</strong><latex-renderer :content="question.design_reason" /></p>
                    <p v-if="question.difficulty_reason"><strong>难度设定理由：</strong><latex-renderer :content="question.difficulty_reason" /></p>
                    <div v-if="question.distractor_reasons && question.distractor_reasons.length > 0">
                      <strong>干扰项设计理由：</strong>
                      <div v-for="(dr, drIdx) in question.distractor_reasons" :key="drIdx" class="distractor-item">
                        <span class="tag-new tag-primary">{{ dr.option }}</span>
                        <span class="tag-new tag-warning">{{ dr.type }}</span>
                        <latex-renderer :content="dr.reason" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="question-footer">
                <button class="btn-new btn-sm-new" style="color: #10b981; border-color: #a7f3d0; background: #ecfdf5;" @click="adoptQuestion(index)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  采纳
                </button>
                <button class="btn-new btn-sm-new btn-ghost-new" @click="editQuestion(index)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                  编辑
                </button>
                <button class="btn-new btn-sm-new btn-ghost-new" @click="regenerateQuestion(index)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                  重新生成
                </button>
                <button class="btn-new btn-sm-new" style="color: #dc2626; border-color: #fecaca; background: #fef2f2;" @click="discardQuestion(index)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                  丢弃
                </button>
              </div>
            </div>
          </div>
          <div class="card-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-top: 1px solid #e2e8f0;">
            <div style="font-size: 14px; color: #64748b;">
              已选择 <strong style="color: #1a1a2e;">{{ selectedQuestions.length }}</strong> 道题目
            </div>
            <button class="btn-new btn-primary-new" @click="confirmAdoption" :disabled="selectedQuestions.length === 0">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              确认入库
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑题目对话框 -->
    <div v-if="editDialogVisible" class="modal-overlay" @click.self="editDialogVisible = false">
      <div class="modal-content" style="max-width: 900px; width: 95%;">
        <div class="modal-header">
          <h3 class="modal-title">
            <svg class="w-5 h-5" style="color: #1a1a2e;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            编辑题目
          </h3>
          <button class="modal-close" @click="editDialogVisible = false">✕</button>
        </div>
        <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">
          <div class="form-group">
            <label class="form-label">题目内容</label>
            <textarea class="form-textarea" v-model="editForm.content" rows="4"></textarea>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">题型</label>
              <select class="form-select" v-model="editForm.question_type">
                <option value="单选">单选</option>
                <option value="多选">多选</option>
                <option value="判断">判断</option>
                <option value="填空">填空</option>
                <option value="主观">主观</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">难度</label>
              <select class="form-select" v-model="editForm.difficulty">
                <option value="L1">L1 记忆</option>
                <option value="L2">L2 理解</option>
                <option value="L3">L3 应用</option>
                <option value="L4">L4 分析</option>
                <option value="L5">L5 创造</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">解析</label>
            <textarea class="form-textarea" v-model="editForm.explanation" rows="3"></textarea>
          </div>
          <div class="form-group" v-if="['单选', '多选', '判断'].includes(editForm.question_type)">
            <label class="form-label">选项</label>
            <div class="options-list">
              <div v-for="(option, index) in editForm.options" :key="index" class="option-item">
                <input type="text" class="form-input" v-model="option.content" placeholder="选项内容" />
                <label class="checkbox-label">
                  <input type="checkbox" v-model="option.is_correct" />
                  <span>正确</span>
                </label>
                <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="removeOption(index)">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
              <button class="btn-new btn-ghost-new" style="width: 100%;" @click="addOption">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                添加选项
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-new btn-ghost-new" @click="editDialogVisible = false">取消</button>
          <button class="btn-new btn-primary-new" @click="saveEditedQuestion">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIGenerate',
  data() {
    return {
      form: {
        knowledge_point_ids: [],
        question_types: ['单选', '多选', '判断'],
        difficulty: 'L2',
        question_count: 5,
        advanced: {
          distractors_based_on_misconceptions: true,
          combine_with_fault_cases: false,
          custom_requirements: ''
        }
      },
      selectedKnowledgeIds: [],
      knowledgeTree: [
        {
          id: 1,
          label: '课程总览',
          expanded: true,
          children: [
            {
              id: 2,
              label: '基础知识',
              expanded: false,
              children: [
                { id: 5, label: '基本定义' },
                { id: 6, label: '发展历史' }
              ]
            },
            {
              id: 3,
              label: '核心概念',
              expanded: false,
              children: [
                { id: 7, label: '核心原理' },
                { id: 8, label: '关键技术' }
              ]
            },
            {
              id: 4,
              label: '实践应用',
              expanded: false,
              children: [
                { id: 9, label: '实际操作' },
                { id: 10, label: '故障处理' }
              ]
            }
          ]
        }
      ],
      isGenerating: false,
      generationProgress: 0,
      generationStatus: 'success',
      generatedCount: 0,
      generatedQuestions: [],
      selectedQuestions: [],
      editDialogVisible: false,
      editForm: {
        content: '',
        question_type: '单选',
        difficulty: 'L2',
        explanation: '',
        options: []
      },
      editIndex: -1,
      // 异步任务相关
      currentTaskId: null,
      statusPollingInterval: null,
      generationMessage: '',
      enableVerification: true,  // 是否启用验证
      maxRetries: 3  // 最大重试次数
    }
  },
  mounted() {
    this.loadKnowledgeTree()
  },

  beforeDestroy() {
    // 组件销毁时停止轮询
    this.stopStatusPolling()
  },
  methods: {
    loadKnowledgeTree() {
      // 这里应该调用API获取知识点树
    },
    async generateQuestions() {
      if (this.selectedKnowledgeIds.length === 0) {
        this.$message.error('请选择知识范围')
        return
      }
      if (this.form.question_types.length === 0) {
        this.$message.error('请选择题型')
        return
      }

      this.isGenerating = true
      this.generationProgress = 0
      this.generatedCount = 0
      this.generatedQuestions = []
      this.generationMessage = '正在创建生成任务...'

      try {
        // 构建请求参数
        const typeCounts = {}
        this.form.question_types.forEach(type => {
          typeCounts[type] = Math.ceil(this.form.question_count / this.form.question_types.length)
        })

        // 难度配置
        const difficultyConfig = {}
        difficultyConfig[this.form.difficulty] = { count: this.form.question_count }

        const requestData = {
          knowledge_categories: this.selectedKnowledgeIds.map(id => {
            // 根据ID获取知识点名称
            const node = this.findKnowledgeNodeById(id)
            return node ? node.label : ''
          }).filter(name => name),
          question_types: this.form.question_types,
          type_counts: typeCounts,
          difficulty_config: difficultyConfig,
          total_count: this.form.question_count,
          enable_verification: this.enableVerification,
          max_generation_retries: this.maxRetries,
          distractor_list: [],
          preference_list: [],
          custom_requirement: this.form.advanced.custom_requirements || ''
        }

        this.generationMessage = '正在发送生成请求...'

        // 调用新的异步生成接口
        const response = await api.generateQuestionsWithVerification(requestData)

        if (response.data.code === 0) {
          this.currentTaskId = response.data.data.task_id
          this.generationMessage = `任务已创建 (ID: ${this.currentTaskId})，开始生成...`
          this.$message.success('生成任务已创建，开始生成题目...')

          // 开始轮询任务状态
          this.startStatusPolling()
        } else {
          this.$message.error(response.data.message || '创建生成任务失败')
          this.isGenerating = false
        }
      } catch (error) {
        console.error('生成题目失败:', error)
        this.$message.error('生成题目失败: ' + (error.response?.data?.message || error.message))
        this.isGenerating = false
      }
    },

    // 开始轮询任务状态
    startStatusPolling() {
      // 清除之前的轮询
      if (this.statusPollingInterval) {
        clearInterval(this.statusPollingInterval)
      }

      // 每2秒查询一次状态
      this.statusPollingInterval = setInterval(async () => {
        await this.checkTaskStatus()
      }, 2000)
    },

    // 查询任务状态
    async checkTaskStatus() {
      if (!this.currentTaskId) return

      try {
        const response = await api.getTaskStatus(this.currentTaskId)

        if (response.data.code === 0) {
          const data = response.data.data

          // 更新进度
          this.generationProgress = Math.round((data.current_question / data.total_count) * 100)
          this.generatedCount = data.generated_count
          this.generationMessage = data.message || `正在生成第 ${data.current_question}/${data.total_count} 题...`

          // 如果任务完成
          if (data.status === 'completed') {
            this.stopStatusPolling()
            this.generationStatus = 'success'
            this.generationMessage = `生成完成！成功 ${data.completed_count} 题，失败 ${data.failed_count} 题`
            this.$message.success(`题目生成完成！成功 ${data.completed_count} 题`)

            // 获取生成的题目
            await this.loadGeneratedQuestions()
            this.isGenerating = false
          }

          // 如果任务失败
          if (data.status === 'failed') {
            this.stopStatusPolling()
            this.generationStatus = 'error'
            this.generationMessage = '生成任务失败: ' + (data.message || '未知错误')
            this.$message.error('生成任务失败')
            this.isGenerating = false
          }
        }
      } catch (error) {
        console.error('查询任务状态失败:', error)
      }
    },

    // 停止轮询
    stopStatusPolling() {
      if (this.statusPollingInterval) {
        clearInterval(this.statusPollingInterval)
        this.statusPollingInterval = null
      }
    },

    // 加载生成的题目
    async loadGeneratedQuestions() {
      if (!this.currentTaskId) return

      try {
        const response = await api.getGeneratedQuestions(this.currentTaskId)

        if (response.data.code === 0) {
          // 转换后端数据格式为前端格式
          this.generatedQuestions = response.data.data.map(q => ({
            id: q.id,
            selected: false,
            content: q.content,
            question_type: q.question_type,
            difficulty: q.difficulty,
            answer: q.answer,
            explanation: q.explanation,
            options: q.options || [],
            design_reason: q.design_reason || '',
            difficulty_reason: q.difficulty_reason || '',
            distractor_reasons: q.distractor_reasons || [],
            knowledge_points: Array.isArray(q.knowledge_points) ? q.knowledge_points :
              (typeof q.knowledge_points === 'string' && q.knowledge_points.includes(',')) ?
                q.knowledge_points.split(',').map(k => k.trim()).filter(Boolean) :
                (q.knowledge_points ? [q.knowledge_points] : []),
            showInterpretability: false,
            is_draft: q.is_draft,
            is_discarded: q.is_discarded
          }))
        }
      } catch (error) {
        console.error('加载生成的题目失败:', error)
        this.$message.error('加载生成的题目失败')
      }
    },

    // 根据ID查找知识点节点
    findKnowledgeNodeById(id) {
      for (const node of this.knowledgeTree) {
        if (node.id === id) return node
        if (node.children) {
          for (const child of node.children) {
            if (child.id === id) return child
            if (child.children) {
              for (const grandchild of child.children) {
                if (grandchild.id === id) return grandchild
              }
            }
          }
        }
      }
      return null
    },

    cancelGeneration() {
      this.stopStatusPolling()
      this.isGenerating = false
      this.generationProgress = 0
      this.generatedCount = 0
      this.currentTaskId = null
      this.generationMessage = ''
      this.$message.info('生成已取消')
    },
    handleQuestionSelect() {
      this.selectedQuestions = this.generatedQuestions.filter(q => q.selected)
    },
    adoptQuestion(index) {
      this.generatedQuestions[index].status = '已采纳'
      this.generatedQuestions[index].selected = true
      this.handleQuestionSelect()
      this.$message.success('题目已采纳')
    },
    discardQuestion(index) {
      this.generatedQuestions.splice(index, 1)
      this.handleQuestionSelect()
      this.$message.success('题目已丢弃')
    },
    editQuestion(index) {
      this.editIndex = index
      const question = this.generatedQuestions[index]
      this.editForm = {
        content: question.content,
        question_type: question.question_type,
        difficulty: question.difficulty,
        explanation: question.explanation,
        options: JSON.parse(JSON.stringify(question.options))
      }
      this.editDialogVisible = true
    },
    saveEditedQuestion() {
      if (this.editIndex >= 0) {
        const question = this.generatedQuestions[this.editIndex]
        question.content = this.editForm.content
        question.question_type = this.editForm.question_type
        question.difficulty = this.editForm.difficulty
        question.explanation = this.editForm.explanation
        question.options = this.editForm.options
        this.editDialogVisible = false
        this.$message.success('题目编辑成功')
      }
    },
    regenerateQuestion(index) {
      this.$message.info('正在重新生成题目...')
      setTimeout(() => {
        this.generatedQuestions[index].content = `这是重新生成的${this.form.difficulty}难度题目，包含公式 $E=mc^2$`
        this.$message.success('题目重新生成成功')
      }, 1000)
    },
    batchAdopt() {
      let count = 0
      this.generatedQuestions.forEach(q => {
        if (q.selected) {
          q.status = '已采纳'
          count++
        }
      })
      this.$message.success(`成功采纳${count}道题目`)
    },
    batchDiscard() {
      const count = this.selectedQuestions.length
      this.generatedQuestions = this.generatedQuestions.filter(q => !q.selected)
      this.selectedQuestions = []
      this.$message.success(`成功丢弃${count}道题目`)
    },
    confirmAdoption() {
      const selectedQuestions = this.generatedQuestions.filter(q => q.selected)
      if (selectedQuestions.length === 0) {
        this.$message.error('请选择要入库的题目')
        return
      }
      
      this.$message.success(`成功将${selectedQuestions.length}道题目入库`)
      this.generatedQuestions = []
      this.selectedQuestions = []
    },
    addOption() {
      this.editForm.options.push({ content: '', is_correct: false })
    },
    removeOption(index) {
      if (this.editForm.options.length <= 2) {
        this.$message.warning('至少需要保留两个选项')
        return
      }
      this.editForm.options.splice(index, 1)
    },
    getQuestionTypeClass(type) {
      switch (type) {
        case '单选': return 'tag-primary'
        case '多选': return 'tag-success'
        case '判断': return 'tag-warning'
        case '填空': return 'tag-error'
        case '主观': return 'tag-purple'
        default: return 'tag-primary'
      }
    },
    getDifficultyClass(difficulty) {
      switch (difficulty) {
        case 'L1': return 'tag-success'
        case 'L2': return 'tag-primary'
        case 'L3': return 'tag-warning'
        case 'L4': return 'tag-error'
        case 'L5': return 'tag-purple'
        default: return 'tag-primary'
      }
    }
  }
}
</script>

<style lang="less" scoped>
@import '../assets/styles/variables.less';

.welcome-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

// 生成布局
.generate-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: @spacing-xl;
}

.generate-sidebar {
  display: flex;
  flex-direction: column;
}

.generate-main {
  min-height: 600px;
}

// 知识树
.knowledge-tree {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid @border-light;
  border-radius: @radius-md;
  padding: @spacing-md;
  background: @bg-card;
}

.tree-node {
  margin-bottom: @spacing-sm;
}

.tree-node-header {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  cursor: pointer;
  padding: @spacing-xs 0;
}

.tree-icon {
  width: 16px;
  height: 16px;
  transition: transform @transition-fast;
  color: @text-muted;

  &.expanded {
    transform: rotate(90deg);
  }
}

.tree-children {
  margin-left: @spacing-lg;
  margin-top: @spacing-xs;
}

.tree-child {
  margin-bottom: @spacing-xs;
}

.tree-grandchildren {
  margin-left: @spacing-lg;
  margin-top: @spacing-xs;
}

.tree-leaf {
  display: block;
  padding: @spacing-xs 0;
}

// 复选框组
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: @spacing-md;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  font-size: @font-size-sm;
  color: @text-primary;
  cursor: pointer;

  input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
}

// 单选组
.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: @spacing-md;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  font-size: @font-size-sm;
  color: @text-primary;
  cursor: pointer;

  input[type="radio"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
}

// 滑块
.slider-wrapper {
  display: flex;
  align-items: center;
  gap: @spacing-md;
}

.form-slider {
  flex: 1;
  -webkit-appearance: none;
  height: 6px;
  border-radius: 3px;
  background: @border-light;
  outline: none;

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: @primary-color;
    cursor: pointer;
  }

  &::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: @primary-color;
    cursor: pointer;
    border: none;
  }
}

.slider-value {
  font-size: @font-size-sm;
  color: @text-primary;
  font-weight: 500;
  min-width: 50px;
}

// 高级选项
.advanced-options {
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
}

// 表单操作
.form-actions {
  margin-top: @spacing-lg;
}

// 进度条
.progress-wrapper {
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
}

.progress-bar {
  height: 8px;
  background: @border-light;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, @primary-color 0%, lighten(@primary-color, 20%) 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: @font-size-sm;
  color: @text-secondary;
}

// 批量操作
.batch-actions {
  display: flex;
  gap: @spacing-sm;
}

// 题目项
.question-item {
  border-bottom: 1px solid @border-light;
  padding: @spacing-lg;

  &:last-child {
    border-bottom: none;
  }
}

.question-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: @spacing-md;
}

.question-number {
  font-weight: 600;
  color: @text-primary;
}

.question-tags {
  display: flex;
  gap: @spacing-xs;
}

.question-body {
  margin-bottom: @spacing-md;
}

.question-content {
  font-size: @font-size-md;
  color: @text-primary;
  line-height: 1.6;
  margin-bottom: @spacing-md;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
  margin-bottom: @spacing-md;
}

.option-item {
  display: flex;
  align-items: center;
  gap: @spacing-sm;
  padding: @spacing-sm @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
  border: 1px solid @border-light;

  &.correct {
    background: fade(@success-color, 10%);
    border-color: fade(@success-color, 30%);
  }
}

.option-label {
  font-weight: 600;
  color: @text-secondary;
  min-width: 24px;
}

.question-explanation {
  margin-bottom: @spacing-md;
  padding: @spacing-md;
  background: fade(@primary-color, 5%);
  border-radius: @radius-md;
  border: 1px solid fade(@primary-color, 10%);
}

.explanation-title {
  font-weight: 600;
  color: @primary-color;
  margin-bottom: @spacing-xs;
}

.question-interpretability {
  margin-bottom: @spacing-md;
}

.interpretability-header {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  font-size: @font-size-sm;
  color: @text-secondary;
  cursor: pointer;
  padding: @spacing-sm 0;

  svg {
    transition: transform @transition-fast;

    &.expanded {
      transform: rotate(90deg);
    }
  }
}

.interpretability-content {
  padding: @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
  font-size: @font-size-sm;

  p {
    margin-bottom: @spacing-sm;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.distractor-item {
  display: flex;
  align-items: center;
  gap: @spacing-sm;
  margin-top: @spacing-xs;
  padding: @spacing-xs @spacing-sm;
  background: @bg-card;
  border-radius: @radius-sm;
}

.question-footer {
  display: flex;
  gap: @spacing-sm;
}

// 选项列表
.options-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
}

// 紫色标签
.tag-purple {
  background: fade(#9333ea, 10%);
  color: #9333ea;
}

// 文本颜色
.text-error {
  color: @error-color;
}

// 响应式
@media (max-width: @breakpoint-lg) {
  .generate-layout {
    grid-template-columns: 1fr;
  }

  .generate-sidebar {
    order: 2;
  }

  .generate-main {
    order: 1;
  }

  .welcome-header {
    flex-direction: column;
    gap: @spacing-md;
    align-items: flex-start;
  }
}
</style>
