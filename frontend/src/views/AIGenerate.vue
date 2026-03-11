<template>
  <div class="ai-generate">
    <el-card>
      <h2>AI智能生题</h2>
      
      <el-form :model="form" label-width="100px">
        <el-form-item label="知识范围">
          <el-tree
            :data="knowledgeTree"
            show-checkbox
            node-key="id"
            :default-expanded-keys="[1]"
            v-model="form.knowledge_point_ids"
            style="max-height: 300px; overflow-y: auto;"
          ></el-tree>
        </el-form-item>
        
        <el-form-item label="题型">
          <el-checkbox-group v-model="form.question_types">
            <el-checkbox label="单选">单选</el-checkbox>
            <el-checkbox label="多选">多选</el-checkbox>
            <el-checkbox label="判断">判断</el-checkbox>
            <el-checkbox label="填空">填空</el-checkbox>
            <el-checkbox label="主观">主观</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="难度">
          <el-radio-group v-model="form.difficulty">
            <el-radio label="简单">简单</el-radio>
            <el-radio label="中等">中等</el-radio>
            <el-radio label="困难">困难</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="题目数量">
          <el-slider v-model="form.question_count" :min="1" :max="20" show-input></el-slider>
        </el-form-item>
        
        <el-form-item label="高级要求">
          <el-collapse>
            <el-collapse-item title="高级设置">
              <el-checkbox v-model="form.advanced.distractors_based_on_misconceptions">干扰项基于常见误区</el-checkbox>
              <el-checkbox v-model="form.advanced.combine_with_fault_cases">结合实际故障案例</el-checkbox>
              <el-input type="textarea" v-model="form.advanced.custom_requirements" placeholder="自定义文本要求" :rows="3"></el-input>
            </el-collapse-item>
          </el-collapse>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="generateQuestions" :disabled="isGenerating">
            {{ isGenerating ? '生成中...' : '开始生成' }}
          </el-button>
          <el-button @click="cancelGeneration" v-if="isGenerating">取消生成</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 生成进度 -->
      <el-card v-if="isGenerating" class="progress-card">
        <h3>生成进度</h3>
        <el-progress :percentage="generationProgress" :status="generationStatus"></el-progress>
        <p>已生成: {{ generatedCount }}/{{ form.question_count }} 题</p>
      </el-card>
      
      <!-- 生成结果 -->
      <el-card v-if="generatedQuestions.length > 0" class="result-card">
        <div class="result-header">
          <h3>生成结果</h3>
          <div>
            <el-button type="success" @click="batchAdopt" :disabled="selectedQuestions.length === 0">批量采纳</el-button>
            <el-button type="danger" @click="batchDiscard" :disabled="selectedQuestions.length === 0">批量丢弃</el-button>
          </div>
        </div>
        
        <div v-for="(question, index) in generatedQuestions" :key="index" class="question-card">
          <el-checkbox v-model="question.selected" @change="handleQuestionSelect"></el-checkbox>
          <div class="question-content">
            <h4><latex-renderer :content="index + 1 + '. ' + question.content" /></h4>
            <div v-if="['单选', '多选', '判断'].includes(question.question_type)" class="options">
              <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option-item">
                <el-tag :type="option.is_correct ? 'success' : ''">{{ String.fromCharCode(65 + optIndex) }}. <latex-renderer :content="option.content" /></el-tag>
              </div>
            </div>
            <div class="explanation" v-if="question.explanation">
              <h5>解析：</h5>
              <p><latex-renderer :content="question.explanation" /></p>
            </div>
            <div class="interpretability">
              <el-collapse>
                <el-collapse-item title="可解释性信息">
                  <p v-if="question.design_reason"><strong>题目设计依据：</strong><latex-renderer :content="question.design_reason" /></p>
                  <p v-if="question.difficulty_reason"><strong>难度设定理由：</strong><latex-renderer :content="question.difficulty_reason" /></p>
                  <p v-if="question.distractor_reasons && question.distractor_reasons.length > 0">
                    <strong>干扰项设计理由：</strong>
                    <div v-for="(dr, drIdx) in question.distractor_reasons" :key="drIdx" class="distractor-item">
                      <el-tag size="small" type="info">{{ dr.option }}</el-tag>
                      <span class="distractor-type">[{{ dr.type }}]</span>
                      <latex-renderer :content="dr.reason" />
                    </div>
                  </p>
                </el-collapse-item>
              </el-collapse>
            </div>
            <div class="actions">
              <el-button size="small" type="success" @click="adoptQuestion(index)">采纳</el-button>
              <el-button size="small" type="danger" @click="discardQuestion(index)">丢弃</el-button>
              <el-button size="small" @click="editQuestion(index)">编辑</el-button>
              <el-button size="small" @click="regenerateQuestion(index)">重新生成</el-button>
            </div>
          </div>
        </div>
        
        <div class="result-footer" v-if="generatedQuestions.length > 0">
          <el-button type="primary" @click="confirmAdoption" :disabled="selectedQuestions.length === 0">确认入库</el-button>
        </div>
      </el-card>
    </el-card>
    
    <!-- 编辑题目对话框 -->
    <el-dialog :title="'编辑题目'" :visible.sync="editDialogVisible" width="800px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="题目内容">
          <el-input type="textarea" v-model="editForm.content" :rows="4"></el-input>
        </el-form-item>
        <el-form-item label="题型">
          <el-select v-model="editForm.question_type">
            <el-option label="单选" value="单选"></el-option>
            <el-option label="多选" value="多选"></el-option>
            <el-option label="判断" value="判断"></el-option>
            <el-option label="填空" value="填空"></el-option>
            <el-option label="主观" value="主观"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="editForm.difficulty">
            <el-option label="简单" value="简单"></el-option>
            <el-option label="中等" value="中等"></el-option>
            <el-option label="困难" value="困难"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="解析">
          <el-input type="textarea" v-model="editForm.explanation" :rows="3"></el-input>
        </el-form-item>
        <el-form-item label="选项" v-if="['单选', '多选', '判断'].includes(editForm.question_type)">
          <div v-for="(option, index) in editForm.options" :key="index" class="option-item">
            <el-input v-model="option.content" placeholder="选项内容" style="width: 80%;"></el-input>
            <el-checkbox v-model="option.is_correct" style="margin-left: 10px;">正确</el-checkbox>
            <el-button type="danger" size="small" @click="removeOption(index)" style="margin-left: 10px;">删除</el-button>
          </div>
          <el-button type="primary" size="small" @click="addOption" style="margin-top: 10px;">添加选项</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEditedQuestion">保存</el-button>
      </div>
    </el-dialog>
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
      knowledgeTree: [],
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
      editIndex: -1
    }
  },
  mounted() {
    this.loadKnowledgeTree()
  },
  methods: {
    loadKnowledgeTree() {
      // 这里应该调用API获取知识点树
      this.knowledgeTree = [
        {
          id: 1,
          label: '课程总览',
          children: [
            {
              id: 2,
              label: '基础知识',
              children: [
                { id: 5, label: '基本定义' },
                { id: 6, label: '发展历史' }
              ]
            },
            {
              id: 3,
              label: '核心概念',
              children: [
                { id: 7, label: '核心原理' },
                { id: 8, label: '关键技术' }
              ]
            },
            {
              id: 4,
              label: '实践应用',
              children: [
                { id: 9, label: '实际操作' },
                { id: 10, label: '故障处理' }
              ]
            }
          ]
        }
      ]
    },
    generateQuestions() {
      if (this.form.knowledge_point_ids.length === 0) {
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
      
      // 模拟生成过程
      const total = this.form.question_count
      let current = 0
      
      const interval = setInterval(() => {
        current++
        this.generatedCount = current
        this.generationProgress = Math.round((current / total) * 100)
        
        // 模拟生成题目
        const questionTypes = this.form.question_types
        const question = {
          selected: false,
          content: `这是生成的第${current}道${this.form.difficulty}难度的${questionTypes[current % questionTypes.length]}题`,
          question_type: questionTypes[current % questionTypes.length],
          difficulty: this.form.difficulty,
          explanation: `这是第${current}道题的解析`,
          options: [
            { content: '选项A', is_correct: current % 4 === 0 },
            { content: '选项B', is_correct: current % 4 === 1 },
            { content: '选项C', is_correct: current % 4 === 2 },
            { content: '选项D', is_correct: current % 4 === 3 }
          ],
          interpretability: {
            knowledge_alignment: '知识点对齐说明',
            concept_source: '知识库章节来源',
            distractor_strategy: '干扰项设计策略',
            option_basis: '各选项详细依据'
          }
        }
        this.generatedQuestions.push(question)
        
        if (current >= total) {
          clearInterval(interval)
          this.isGenerating = false
          this.generationStatus = 'success'
          this.$message.success('题目生成完成')
        }
      }, 1000)
    },
    cancelGeneration() {
      this.isGenerating = false
      this.generationProgress = 0
      this.generatedCount = 0
      this.$message.info('生成已取消')
    },
    handleQuestionSelect() {
      this.selectedQuestions = this.generatedQuestions.filter(q => q.selected)
    },
    adoptQuestion(index) {
      this.generatedQuestions[index].status = '已采纳'
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
      // 模拟重新生成
      this.$message.info('正在重新生成题目...')
      setTimeout(() => {
        this.generatedQuestions[index].content = `这是重新生成的${this.form.difficulty}难度题目`
        this.$message.success('题目重新生成成功')
      }, 1000)
    },
    batchAdopt() {
      this.generatedQuestions.forEach(q => {
        if (q.selected) {
          q.status = '已采纳'
        }
      })
      this.$message.success(`成功采纳${this.selectedQuestions.length}道题目`)
    },
    batchDiscard() {
      this.generatedQuestions = this.generatedQuestions.filter(q => !q.selected)
      this.selectedQuestions = []
      this.$message.success(`成功丢弃${this.selectedQuestions.length}道题目`)
    },
    confirmAdoption() {
      const selectedQuestions = this.generatedQuestions.filter(q => q.selected)
      if (selectedQuestions.length === 0) {
        this.$message.error('请选择要入库的题目')
        return
      }
      
      // 调用API将选中的题目入库
      this.$axios.post('/api/ai/questions/adopt', {
        questions: selectedQuestions
      }).then(response => {
        this.$message.success(response.data.message)
        this.generatedQuestions = []
        this.selectedQuestions = []
      }).catch(error => {
        this.$message.error('入库失败，请重试')
        console.error(error)
      })
    },
    addOption() {
      this.editForm.options.push({ content: '', is_correct: false })
    },
    removeOption(index) {
      this.editForm.options.splice(index, 1)
    }
  }
}
</script>

<style scoped>
.ai-generate {
  padding: 20px;
}

.progress-card {
  margin-top: 20px;
}

.result-card {
  margin-top: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-card {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #f9fafc;
}

.question-content {
  margin-left: 25px;
}

.options {
  margin: 10px 0;
}

.option-item {
  margin-bottom: 8px;
}

.explanation {
  margin: 10px 0;
  padding: 10px;
  background-color: #ecf5ff;
  border-radius: 4px;
}

.interpretability {
  margin: 10px 0;
}

.actions {
  margin-top: 10px;
}

.result-footer {
  margin-top: 20px;
  text-align: right;
}
</style>