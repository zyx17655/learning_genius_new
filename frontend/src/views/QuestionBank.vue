<template>
  <div class="question-bank">
    <el-card>
      <div class="card-header">
        <h2>题库管理</h2>
        <el-button type="primary" @click="addQuestion">新增题目</el-button>
      </div>
      
      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-select v-model="filter.status" placeholder="状态" @change="loadQuestions">
              <el-option label="全部" value=""></el-option>
              <el-option label="草稿" value="草稿"></el-option>
              <el-option label="已审核" value="已审核"></el-option>
              <el-option label="已禁用" value="已禁用"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filter.questionType" placeholder="题型" @change="loadQuestions">
              <el-option label="全部" value=""></el-option>
              <el-option label="单选" value="单选"></el-option>
              <el-option label="多选" value="多选"></el-option>
              <el-option label="判断" value="判断"></el-option>
              <el-option label="填空" value="填空"></el-option>
              <el-option label="主观" value="主观"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filter.difficulty" placeholder="难度" @change="loadQuestions">
              <el-option label="全部" value=""></el-option>
              <el-option label="L1 记忆" value="L1"></el-option>
              <el-option label="L2 理解" value="L2"></el-option>
              <el-option label="L3 应用" value="L3"></el-option>
              <el-option label="L4 分析" value="L4"></el-option>
              <el-option label="L5 创造" value="L5"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-input v-model="filter.keyword" placeholder="搜索题目" suffix-icon="el-icon-search" @keyup.enter="loadQuestions"></el-input>
          </el-col>
        </el-row>
      </div>
      
      <div class="batch-actions" style="margin-top: 10px;">
        <el-button type="info" @click="selectAll">全选</el-button>
        <el-button type="info" @click="clearSelection">清空选择</el-button>
        <el-button type="success" @click="batchApprove" :disabled="selectedIds.length === 0">批量审核</el-button>
        <el-button type="warning" @click="batchDraft" :disabled="selectedIds.length === 0">批量设为草稿</el-button>
        <el-button type="danger" @click="batchDelete" :disabled="selectedIds.length === 0">批量删除</el-button>
      </div>
      
      <el-table ref="questionTable" :data="questions" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="题目ID" width="80"></el-table-column>
        <el-table-column prop="content" label="题目内容" min-width="300">
          <template slot-scope="scope">
            <div class="question-content">
              <latex-renderer :content="scope.row.content" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="question_type" label="题型" width="100"></el-table-column>
        <el-table-column prop="difficulty" label="难度" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <div class="action-buttons">
              <el-button size="small" @click="editQuestion(scope.row)">编辑</el-button>
              <el-button size="small" class="delete-btn" @click="deleteQuestion(scope.row.id)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination" style="margin-top: 20px;">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
    </el-card>
    
    <!-- 新增/编辑题目对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="800px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="题目内容">
          <el-input type="textarea" v-model="form.content" :rows="4" placeholder="支持LaTeX公式，如：$E=mc^2$ 或 $$\\int_a^b f(x)dx$$"></el-input>
          <div class="latex-preview" v-if="form.content">
            <div class="preview-label">预览：</div>
            <latex-renderer :content="form.content" />
          </div>
        </el-form-item>
        <el-form-item label="题型">
          <el-select v-model="form.question_type">
            <el-option label="单选" value="单选"></el-option>
            <el-option label="多选" value="多选"></el-option>
            <el-option label="判断" value="判断"></el-option>
            <el-option label="填空" value="填空"></el-option>
            <el-option label="主观" value="主观"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="form.difficulty">
            <el-option label="L1 记忆" value="L1"></el-option>
            <el-option label="L2 理解" value="L2"></el-option>
            <el-option label="L3 应用" value="L3"></el-option>
            <el-option label="L4 分析" value="L4"></el-option>
            <el-option label="L5 创造" value="L5"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="知识点">
          <el-select v-model="form.knowledge_point_ids" multiple placeholder="选择知识点">
            <el-option v-for="point in knowledgePoints" :key="point.id" :label="point.name" :value="point.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="解析">
          <el-input type="textarea" v-model="form.explanation" :rows="3" placeholder="支持LaTeX公式"></el-input>
          <div class="latex-preview" v-if="form.explanation">
            <div class="preview-label">预览：</div>
            <latex-renderer :content="form.explanation" />
          </div>
        </el-form-item>
        <el-form-item label="选项" v-if="['单选', '多选', '判断'].includes(form.question_type)">
          <div v-for="(option, index) in form.options" :key="index" class="option-item">
            <div class="option-input-wrapper">
              <el-input v-model="option.content" placeholder="选项内容（支持LaTeX公式）" style="width: 100%;"></el-input>
              <div class="option-preview" v-if="option.content">
                <latex-renderer :content="option.content" />
              </div>
            </div>
            <el-checkbox v-model="option.is_correct" style="margin-left: 10px;">正确</el-checkbox>
            <el-button type="danger" size="small" @click="removeOption(index)" style="margin-left: 10px;">删除</el-button>
          </div>
          <el-button type="primary" size="small" @click="addOption" style="margin-top: 10px;">添加选项</el-button>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="form.tags" multiple placeholder="选择标签">
            <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.name"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveQuestion">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import api from '@/api'

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
        const res = await api.getQuestions(params)
        this.questions = res.questions || []
        this.total = res.total || 0
      } catch (error) {
        console.error('加载题目失败:', error)
        this.$message.error('加载题目失败')
      }
    },
    async loadKnowledgePoints() {
      try {
        const res = await api.getKnowledgePoints()
        this.knowledgePoints = res || []
      } catch (error) {
        console.error('加载知识点失败:', error)
      }
    },
    async loadTags() {
      try {
        const res = await api.getTags()
        this.tags = res || []
      } catch (error) {
        console.error('加载标签失败:', error)
      }
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.loadQuestions()
    },
    handleCurrentChange(page) {
      this.currentPage = page
      this.loadQuestions()
    },
    handleSelectionChange(selection) {
      this.selectedIds = selection.map(item => item.id)
    },
    selectAll() {
      this.$refs.questionTable.toggleAllSelection()
    },
    clearSelection() {
      this.$refs.questionTable.clearSelection()
    },
    getStatusType(status) {
      switch (status) {
        case '已审核': return 'success'
        case '草稿': return 'info'
        case '已禁用': return 'danger'
        default: return ''
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
          await api.updateQuestion(this.form.id, data)
          this.$message.success('题目更新成功')
        } else {
          await api.createQuestion(data)
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
        await this.$confirm('确定要删除这个题目吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await api.deleteQuestion(id)
        this.$message.success('删除成功')
        this.loadQuestions()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除题目失败:', error)
          this.$message.error('删除失败')
        }
      }
    },
    async batchApprove() {
      try {
        await api.batchReview(this.selectedIds)
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
        await api.batchDraft(this.selectedIds)
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
        await this.$confirm(`确定要删除选中的${this.selectedIds.length}道题目吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await api.batchDelete(this.selectedIds)
        this.$message.success(`成功删除${this.selectedIds.length}道题目`)
        this.clearSelection()
        this.loadQuestions()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
          this.$message.error('批量删除失败')
        }
      }
    },
    addOption() {
      this.form.options.push({ content: '', is_correct: false })
    },
    removeOption(index) {
      this.form.options.splice(index, 1)
    }
  }
}
</script>

<style scoped>
.question-bank {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-section {
  margin-bottom: 20px;
}

.batch-actions {
  margin-bottom: 15px;
}

.question-content {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.action-buttons {
  display: flex;
  flex-wrap: nowrap;
  white-space: nowrap;
}

.action-buttons .el-button {
  margin-left: 5px;
}

.action-buttons .el-button:first-child {
  margin-left: 0;
}

.delete-btn {
  color: #f56c6c !important;
  border-color: #f56c6c !important;
}

.delete-btn:hover {
  color: #fff !important;
  background-color: #f56c6c !important;
}

.latex-preview {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.preview-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.option-input-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.option-preview {
  margin-top: 5px;
  padding: 5px 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
}

.question-content {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  white-space: normal;
}
</style>