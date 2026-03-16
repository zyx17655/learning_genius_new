<template>
  <div class="page-wrapper">
    <section class="welcome-section">
      <div class="welcome-header">
        <div>
          <h1 class="welcome-title">题库管理 📚</h1>
          <p class="welcome-subtitle">管理所有题目，支持LaTeX公式编辑与预览</p>
        </div>
        <div class="welcome-actions">
          <button class="btn-new btn-primary-new" @click="addQuestion">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            新增题目
          </button>
        </div>
      </div>
    </section>

    <section class="content-card">
      <div class="card-header">
        <div class="card-title">
          <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
          </svg>
          筛选条件
        </div>
      </div>
      <div class="card-body">
        <div class="filter-grid">
          <div class="form-group">
            <label class="form-label">状态</label>
            <select class="form-select" v-model="filter.status" @change="loadQuestions">
              <option value="">全部</option>
              <option value="草稿">草稿</option>
              <option value="已审核">已审核</option>
              <option value="已禁用">已禁用</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">题型</label>
            <select class="form-select" v-model="filter.questionType" @change="loadQuestions">
              <option value="">全部</option>
              <option value="单选">单选</option>
              <option value="多选">多选</option>
              <option value="判断">判断</option>
              <option value="填空">填空</option>
              <option value="主观">主观</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">难度</label>
            <select class="form-select" v-model="filter.difficulty" @change="loadQuestions">
              <option value="">全部</option>
              <option value="L1">L1 记忆</option>
              <option value="L2">L2 理解</option>
              <option value="L3">L3 应用</option>
              <option value="L4">L4 分析</option>
              <option value="L5">L5 创造</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">搜索</label>
            <div class="search-box">
              <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <input type="text" v-model="filter.keyword" placeholder="搜索题目内容" @keyup.enter="loadQuestions" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="content-card">
      <div class="card-header">
        <div class="card-title">
          <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          题目列表
          <span class="card-subtitle">共 {{ total }} 道题目</span>
        </div>
        <div class="batch-actions">
          <button class="btn-new btn-sm-new btn-ghost-new" @click="selectAll">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            全选
          </button>
          <button class="btn-new btn-sm-new btn-ghost-new" @click="clearSelection">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
            清空
          </button>
          <button class="btn-new btn-sm-new" style="color: #10b981; border-color: #a7f3d0; background: #ecfdf5;" @click="batchApprove" :disabled="selectedIds.length === 0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            审核
          </button>
          <button class="btn-new btn-sm-new" style="color: #f59e0b; border-color: #fcd34d; background: #fffbeb;" @click="batchDraft" :disabled="selectedIds.length === 0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            草稿
          </button>
          <button class="btn-new btn-sm-new" style="color: #dc2626; border-color: #fecaca; background: #fef2f2;" @click="batchDelete" :disabled="selectedIds.length === 0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            删除
          </button>
        </div>
      </div>
      <div class="card-body" style="padding: 0;">
        <table class="table-new">
          <thead>
            <tr>
              <th style="width: 50px;">
                <input type="checkbox" :checked="selectedIds.length === questions.length && questions.length > 0" @change="toggleSelectAll" />
              </th>
              <th style="width: 80px;">ID</th>
              <th>题目内容</th>
              <th style="width: 100px;">题型</th>
              <th style="width: 100px;">难度</th>
              <th style="width: 100px;">状态</th>
              <th style="width: 150px;">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="question in questions" :key="question.id">
              <td>
                <input type="checkbox" :checked="selectedIds.includes(question.id)" @change="toggleSelection(question.id)" />
              </td>
              <td>{{ question.id }}</td>
              <td>
                <div class="question-content">
                  <latex-renderer :content="question.content" />
                </div>
              </td>
              <td>
                <span class="tag-new" :class="getQuestionTypeClass(question.question_type)">{{ question.question_type }}</span>
              </td>
              <td>
                <span class="tag-new" :class="getDifficultyClass(question.difficulty)">{{ question.difficulty }}</span>
              </td>
              <td>
                <span class="tag-new" :class="getStatusClass(question.status)">{{ question.status }}</span>
              </td>
              <td>
                <div class="action-buttons">
                  <button class="btn-new btn-sm-new btn-ghost-new" @click="editQuestion(question)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                    编辑
                  </button>
                  <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="deleteQuestion(question.id)">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="questions.length === 0">
              <td colspan="7">
                <div class="empty-state-new">
                  <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <p class="empty-title">暂无题目</p>
                  <p class="empty-desc">点击"新增题目"按钮创建第一道题目</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-top: 1px solid #e2e8f0;">
        <div style="font-size: 14px; color: #64748b;">
          已选择 <strong style="color: #1a1a2e;">{{ selectedIds.length }}</strong> 道题目
        </div>
        <div class="pagination">
          <button class="btn-new btn-sm-new btn-ghost-new" :disabled="currentPage === 1" @click="handleCurrentChange(currentPage - 1)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <span style="padding: 0 16px; font-size: 14px; color: #1e293b;">
            第 <strong>{{ currentPage }}</strong> 页 / 共 <strong>{{ Math.ceil(total / pageSize) || 1 }}</strong> 页
          </span>
          <button class="btn-new btn-sm-new btn-ghost-new" :disabled="currentPage >= Math.ceil(total / pageSize)" @click="handleCurrentChange(currentPage + 1)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
          <select class="form-select" v-model="pageSize" @change="handleSizeChange(pageSize)" style="width: 100px; margin-left: 16px;">
            <option :value="10">10条/页</option>
            <option :value="20">20条/页</option>
            <option :value="50">50条/页</option>
            <option :value="100">100条/页</option>
          </select>
        </div>
      </div>
    </section>

    <!-- 新增/编辑题目对话框 -->
    <div v-if="dialogVisible" class="modal-overlay" @click.self="dialogVisible = false">
      <div class="modal-content" style="max-width: 900px; width: 95%;">
        <div class="modal-header">
          <h3 class="modal-title">
            <svg class="w-5 h-5" style="color: #1a1a2e;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="form.id" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            {{ dialogTitle }}
          </h3>
          <button class="modal-close" @click="dialogVisible = false">✕</button>
        </div>
        <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">
          <div class="form-group">
            <label class="form-label">题目内容 <span class="text-error">*</span></label>
            <textarea class="form-textarea" v-model="form.content" rows="4" placeholder="支持LaTeX公式，如：$E=mc^2$ 或 $$\int_a^b f(x)dx$$"></textarea>
            <div class="latex-preview" v-if="form.content">
              <div class="preview-label">预览：</div>
              <latex-renderer :content="form.content" />
            </div>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">题型 <span class="text-error">*</span></label>
              <select class="form-select" v-model="form.question_type">
                <option value="单选">单选</option>
                <option value="多选">多选</option>
                <option value="判断">判断</option>
                <option value="填空">填空</option>
                <option value="主观">主观</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">难度 <span class="text-error">*</span></label>
              <select class="form-select" v-model="form.difficulty">
                <option value="L1">L1 记忆</option>
                <option value="L2">L2 理解</option>
                <option value="L3">L3 应用</option>
                <option value="L4">L4 分析</option>
                <option value="L5">L5 创造</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">知识点</label>
              <select class="form-select" v-model="form.knowledge_point_ids" multiple style="height: 100px;">
                <option v-for="point in knowledgePoints" :key="point.id" :value="point.id">{{ point.name }}</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">解析</label>
            <textarea class="form-textarea" v-model="form.explanation" rows="3" placeholder="支持LaTeX公式"></textarea>
            <div class="latex-preview" v-if="form.explanation">
              <div class="preview-label">预览：</div>
              <latex-renderer :content="form.explanation" />
            </div>
          </div>

          <div class="form-group" v-if="['单选', '多选', '判断'].includes(form.question_type)">
            <label class="form-label">选项</label>
            <div class="options-list">
              <div v-for="(option, index) in form.options" :key="index" class="option-item">
                <div class="option-input-wrapper">
                  <input type="text" class="form-input" v-model="option.content" placeholder="选项内容（支持LaTeX公式）" />
                  <div class="option-preview" v-if="option.content">
                    <latex-renderer :content="option.content" />
                  </div>
                </div>
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

          <div class="form-group">
            <label class="form-label">标签</label>
            <select class="form-select" v-model="form.tags" multiple style="height: 100px;">
              <option v-for="tag in tags" :key="tag.id" :value="tag.name">{{ tag.name }}</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-new btn-ghost-new" @click="dialogVisible = false">取消</button>
          <button class="btn-new btn-primary-new" @click="saveQuestion">
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
  name: 'QuestionBank',
  data() {
    return {
      questions: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      filter: {
        status: '',
        questionType: '',
        difficulty: '',
        keyword: ''
      },
      selectedIds: [],
      dialogVisible: false,
      dialogTitle: '新增题目',
      form: {
        id: null,
        content: '',
        question_type: '单选',
        difficulty: 'L2',
        knowledge_point_ids: [],
        explanation: '',
        options: [
          { content: '', is_correct: false },
          { content: '', is_correct: false }
        ],
        tags: []
      },
      knowledgePoints: [],
      tags: []
    }
  },
  mounted() {
    this.loadQuestions()
    this.loadKnowledgePoints()
    this.loadTags()
  },
  methods: {
    async loadQuestions() {
      try {
        const params = {
          page: this.currentPage,
          per_page: this.pageSize,
          question_type: this.filter.questionType || undefined,
          difficulty: this.filter.difficulty || undefined,
          status: this.filter.status || undefined,
          keyword: this.filter.keyword || undefined
        }
        const data = await this.$axios.get('/questions', { params })
        console.log('API Response:', data)
        this.questions = data.questions || []
        this.total = data.total || 0
        this.selectedIds = []
      } catch (error) {
        console.error('加载题目失败:', error)
        this.$message.error('加载题目失败')
      }
    },
    async loadKnowledgePoints() {
      try {
        const data = await this.$axios.get('/knowledge-points')
        this.knowledgePoints = data || []
      } catch (error) {
        console.error('加载知识点失败:', error)
      }
    },
    async loadTags() {
      try {
        const data = await this.$axios.get('/tags')
        this.tags = data || []
      } catch (error) {
        console.error('加载标签失败:', error)
      }
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.loadQuestions()
    },
    handleCurrentChange(page) {
      this.currentPage = page
      this.loadQuestions()
    },
    toggleSelection(id) {
      const index = this.selectedIds.indexOf(id)
      if (index > -1) {
        this.selectedIds.splice(index, 1)
      } else {
        this.selectedIds.push(id)
      }
    },
    toggleSelectAll() {
      if (this.selectedIds.length === this.questions.length) {
        this.selectedIds = []
      } else {
        this.selectedIds = this.questions.map(q => q.id)
      }
    },
    selectAll() {
      this.selectedIds = this.questions.map(q => q.id)
    },
    clearSelection() {
      this.selectedIds = []
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
    },
    getStatusClass(status) {
      switch (status) {
        case '已审核': return 'tag-success'
        case '草稿': return 'tag-warning'
        case '已禁用': return 'tag-error'
        default: return 'tag-primary'
      }
    },
    addQuestion() {
      this.dialogTitle = '新增题目'
      this.form = {
        id: null,
        content: '',
        question_type: '单选',
        difficulty: 'L2',
        knowledge_point_ids: [],
        explanation: '',
        options: [
          { content: '', is_correct: false },
          { content: '', is_correct: false }
        ],
        tags: []
      }
      this.dialogVisible = true
    },
    editQuestion(row) {
      this.dialogTitle = '编辑题目'
      const kpIds = row.knowledge_points && row.knowledge_points.length > 0 
        ? this.knowledgePoints.filter(kp => row.knowledge_points.includes(kp.name)).map(kp => kp.id)
        : []
      this.form = {
        id: row.id,
        content: row.content,
        question_type: row.question_type,
        difficulty: row.difficulty,
        knowledge_point_ids: kpIds,
        explanation: row.explanation,
        options: row.options && row.options.length > 0 
          ? JSON.parse(JSON.stringify(row.options)) 
          : [{ content: '', is_correct: false }, { content: '', is_correct: false }],
        tags: row.tags || []
      }
      this.dialogVisible = true
    },
    async saveQuestion() {
      try {
        if (!this.form.content.trim()) {
          this.$message.error('请输入题目内容')
          return
        }

        const data = {
          content: this.form.content,
          question_type: this.form.question_type,
          difficulty: this.form.difficulty,
          explanation: this.form.explanation,
          knowledge_point_ids: this.form.knowledge_point_ids,
          tag_names: this.form.tags,
          options: this.form.options.filter(opt => opt.content.trim())
        }

        if (this.form.id) {
          await this.$axios.put(`/questions/${this.form.id}`, data)
          this.$message.success('题目更新成功')
        } else {
          await this.$axios.post('/questions', data)
          this.$message.success('题目创建成功')
        }

        this.dialogVisible = false
        this.loadQuestions()
      } catch (error) {
        console.error('保存题目失败:', error)
        this.$message.error('保存题目失败')
      }
    },
    async deleteQuestion(id) {
      try {
        if (!confirm('确定要删除这个题目吗？')) return
        await this.$axios.delete(`/questions/${id}`)
        this.$message.success('删除成功')
        this.loadQuestions()
      } catch (error) {
        console.error('删除题目失败:', error)
        this.$message.error('删除失败')
      }
    },
    async batchApprove() {
      try {
        await this.$axios.post('/questions/batch-review', this.selectedIds)
        this.$message.success(`成功审核${this.selectedIds.length}道题目`)
        this.clearSelection()
        this.loadQuestions()
      } catch (error) {
        console.error('批量审核失败:', error)
        this.$message.error('批量审核失败')
      }
    },
    async batchDraft() {
      try {
        await this.$axios.post('/questions/batch-draft', this.selectedIds)
        this.$message.success(`成功将${this.selectedIds.length}道题目设为草稿`)
        this.clearSelection()
        this.loadQuestions()
      } catch (error) {
        console.error('批量设为草稿失败:', error)
        this.$message.error('批量设为草稿失败')
      }
    },
    async batchDelete() {
      try {
        if (!confirm(`确定要删除选中的${this.selectedIds.length}道题目吗？`)) return
        await this.$axios.post('/questions/batch-delete', this.selectedIds)
        this.$message.success(`成功删除${this.selectedIds.length}道题目`)
        this.clearSelection()
        this.loadQuestions()
      } catch (error) {
        console.error('批量删除失败:', error)
        this.$message.error('批量删除失败')
      }
    },
    addOption() {
      this.form.options.push({ content: '', is_correct: false })
    },
    removeOption(index) {
      if (this.form.options.length <= 2) {
        this.$message.warning('至少需要保留两个选项')
        return
      }
      this.form.options.splice(index, 1)
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

.welcome-actions {
  display: flex;
  gap: @spacing-md;
}

// 筛选网格
.filter-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: @spacing-lg;

  @media (max-width: @breakpoint-lg) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: @breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

// 批量操作
.batch-actions {
  display: flex;
  gap: @spacing-sm;
  flex-wrap: wrap;
}

// 题目内容
.question-content {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

// 操作按钮
.action-buttons {
  display: flex;
  gap: @spacing-xs;
}

// 分页
.pagination {
  display: flex;
  align-items: center;
}

// LaTeX预览
.latex-preview {
  margin-top: @spacing-md;
  padding: @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
  border: 1px solid @border-light;
}

.preview-label {
  font-size: @font-size-xs;
  color: @text-muted;
  margin-bottom: @spacing-xs;
}

// 选项列表
.options-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
}

.option-item {
  display: flex;
  align-items: flex-start;
  gap: @spacing-md;
  padding: @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
  border: 1px solid @border-light;
}

.option-input-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
}

.option-preview {
  padding: @spacing-sm @spacing-md;
  background: @bg-card;
  border-radius: @radius-sm;
  border: 1px solid @border-light;
  font-size: @font-size-sm;
}

// 复选框标签
.checkbox-label {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  font-size: @font-size-sm;
  color: @text-primary;
  cursor: pointer;
  white-space: nowrap;

  input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
  }
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
  .welcome-header {
    flex-direction: column;
    gap: @spacing-md;
    align-items: flex-start;
  }

  .batch-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
