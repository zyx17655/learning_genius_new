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
            <el-select v-model="filter.status" placeholder="状态">
              <el-option label="全部" value=""></el-option>
              <el-option label="草稿" value="草稿"></el-option>
              <el-option label="已审核" value="已审核"></el-option>
              <el-option label="已禁用" value="已禁用"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filter.questionType" placeholder="题型">
              <el-option label="全部" value=""></el-option>
              <el-option label="单选" value="单选"></el-option>
              <el-option label="多选" value="多选"></el-option>
              <el-option label="判断" value="判断"></el-option>
              <el-option label="填空" value="填空"></el-option>
              <el-option label="主观" value="主观"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filter.difficulty" placeholder="难度">
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
      
      <el-table :data="questions" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="题目ID" width="80"></el-table-column>
        <el-table-column prop="content" label="题目内容">
          <template slot-scope="scope">
            <div class="question-content">{{ scope.row.content }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="question_type" label="题型" width="100"></el-table-column>
        <el-table-column prop="difficulty" label="难度" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="small" @click="editQuestion(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteQuestion(scope.row.id)">删除</el-button>
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
          <el-input type="textarea" v-model="form.content" :rows="4"></el-input>
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
          <el-select v-model="form.knowledge_point_id" placeholder="选择知识点">
            <el-option v-for="point in knowledgePoints" :key="point.id" :label="point.name" :value="point.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="解析">
          <el-input type="textarea" v-model="form.explanation" :rows="3"></el-input>
        </el-form-item>
        <el-form-item label="选项" v-if="['单选', '多选', '判断'].includes(form.question_type)">
          <div v-for="(option, index) in form.options" :key="index" class="option-item">
            <el-input v-model="option.content" placeholder="选项内容" style="width: 80%;"></el-input>
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
        knowledge_point_id: null,
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
    loadQuestions() {
      // 这里应该调用API获取题目列表
      // 暂时使用模拟数据
      this.questions = [
        {
          id: 1,
          content: '下列关于Python的说法，正确的是：',
          question_type: '单选',
          difficulty: 'L2',
          status: '已审核',
          knowledge_point_id: 1,
          explanation: 'Python是一种解释型语言',
          options: [
            { id: 1, content: 'Python是一种编译型语言', is_correct: false },
            { id: 2, content: 'Python是一种解释型语言', is_correct: true },
            { id: 3, content: 'Python是一种汇编语言', is_correct: false },
            { id: 4, content: 'Python是一种机器语言', is_correct: false }
          ],
          tags: ['基础', '重要']
        },
        {
          id: 2,
          content: '以下哪些是Python的内置数据类型？',
          question_type: '多选',
          difficulty: 'L2',
          status: '已审核',
          knowledge_point_id: 1,
          explanation: 'Python的内置数据类型包括列表、字典和元组',
          options: [
            { id: 5, content: 'list', is_correct: true },
            { id: 6, content: 'dict', is_correct: true },
            { id: 7, content: 'tuple', is_correct: true },
            { id: 8, content: 'array', is_correct: false }
          ],
          tags: ['基础']
        }
      ]
      this.total = 2
    },
    loadKnowledgePoints() {
      // 这里应该调用API获取知识点列表
      this.knowledgePoints = [
        { id: 1, name: '课程总览' },
        { id: 2, name: '基础知识' },
        { id: 3, name: '核心概念' },
        { id: 4, name: '实践应用' }
      ]
    },
    loadTags() {
      // 这里应该调用API获取标签列表
      this.tags = [
        { id: 1, name: '重要' },
        { id: 2, name: '难点' },
        { id: 3, name: '常考' },
        { id: 4, name: '基础' },
        { id: 5, name: '进阶' }
      ]
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
      this.$refs.table.toggleAllSelection()
    },
    clearSelection() {
      this.$refs.table.clearSelection()
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
        knowledge_point_id: null,
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
      this.form = {
        id: row.id,
        content: row.content,
        question_type: row.question_type,
        difficulty: row.difficulty,
        knowledge_point_id: row.knowledge_point_id,
        explanation: row.explanation,
        options: JSON.parse(JSON.stringify(row.options)),
        tags: [...row.tags]
      }
      this.dialogVisible = true
    },
    saveQuestion() {
      // 这里应该调用API保存题目
      this.dialogVisible = false
      this.$message.success('题目保存成功')
      this.loadQuestions()
    },
    deleteQuestion(id) {
      this.$confirm('确定要删除这个题目吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用API删除题目
        this.$message.success('删除成功')
        this.loadQuestions()
      }).catch(() => {})
    },
    batchApprove() {
      // 这里应该调用API批量审核题目
      this.$message.success(`成功审核${this.selectedIds.length}道题目`)
      this.clearSelection()
      this.loadQuestions()
    },
    batchDraft() {
      // 这里应该调用API批量设为草稿
      this.$message.success(`成功将${this.selectedIds.length}道题目设为草稿`)
      this.clearSelection()
      this.loadQuestions()
    },
    batchDelete() {
      this.$confirm(`确定要删除选中的${this.selectedIds.length}道题目吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用API批量删除题目
        this.$message.success(`成功删除${this.selectedIds.length}道题目`)
        this.clearSelection()
        this.loadQuestions()
      }).catch(() => {})
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
</style>