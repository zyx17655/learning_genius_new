<template>
  <div class="page-wrapper">
    <section class="welcome-section">
      <div class="welcome-header">
        <div>
          <h1 class="welcome-title">题目质量对比 🆚</h1>
          <p class="welcome-subtitle">对比题库题目与真题质量，AI智能评估哪边更合理</p>
        </div>
      </div>
    </section>

    <!-- A/B 对比区域 -->
    <section class="content-card">
      <div class="card-header">
        <div class="card-title">
          <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          A/B 对比分析
        </div>
        <div class="header-actions">
          <!-- 对比模式选择 -->
          <div class="compare-mode-selector">
            <span class="mode-label">对比模式:</span>
            <select class="form-select mode-select" v-model="compareMode">
              <option value="overall">整体对比</option>
              <option value="single">逐题对比</option>
            </select>
          </div>
          <button 
            class="btn-new btn-primary-new" 
            @click="startCompare"
            :disabled="!canCompare || comparing"
          >
            <svg v-if="!comparing" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
            <svg v-else class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            {{ comparing ? '分析中...' : '开始对比' }}
          </button>
        </div>
      </div>
      
      <div class="card-body">
        <div class="compare-container">
          <!-- 左侧 A 区 - 题库题目 -->
          <div class="compare-panel panel-a">
            <div class="panel-header">
              <div class="panel-badge badge-a">A</div>
              <h3 class="panel-title">题库题目</h3>
              <span class="panel-subtitle">已选 {{ sideA.selectedQuestions.length }} 题</span>
            </div>
            
            <div class="panel-content">
              <!-- 题目选择 -->
              <div v-if="sideA.selectedQuestions.length === 0" class="question-selector">
                <div class="form-group">
                  <label class="form-label">搜索题目</label>
                  <div class="search-box">
                    <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                    </svg>
                    <input 
                      type="text" 
                      v-model="sideA.keyword" 
                      placeholder="输入关键词搜索题目"
                      @keyup.enter="searchQuestionsA"
                    />
                  </div>
                </div>
                
                <div class="form-group">
                  <label class="form-label">筛选条件</label>
                  <div class="filter-row">
                    <select class="form-select" v-model="sideA.filter.type" @change="searchQuestionsA">
                      <option value="">全部题型</option>
                      <option value="单选">单选</option>
                      <option value="多选">多选</option>
                      <option value="判断">判断</option>
                      <option value="填空">填空</option>
                      <option value="主观">主观</option>
                    </select>
                    <select class="form-select" v-model="sideA.filter.difficulty" @change="searchQuestionsA">
                      <option value="">全部难度</option>
                      <option value="L1">L1 记忆</option>
                      <option value="L2">L2 理解</option>
                      <option value="L3">L3 应用</option>
                      <option value="L4">L4 分析</option>
                      <option value="L5">L5 创造</option>
                    </select>
                  </div>
                </div>

                <button class="btn-new btn-primary-new" @click="searchQuestionsA">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                  搜索题目
                </button>

                <!-- 搜索结果列表 -->
                <div v-if="sideA.searchResults.length > 0" class="search-results">
                  <div class="results-header">
                    <span>搜索结果 ({{ sideA.searchResults.length }})</span>
                    <button 
                      class="btn-new btn-sm-new btn-ghost-new" 
                      @click="selectAllResults"
                      :disabled="sideA.searchResults.length === 0"
                    >
                      全选
                    </button>
                  </div>
                  <div class="results-list">
                    <div 
                      v-for="q in sideA.searchResults" 
                      :key="q.id"
                      class="result-item"
                      :class="{ 'result-selected': isQuestionSelected(q.id) }"
                      @click="toggleQuestionSelection(q)"
                    >
                      <div class="result-checkbox">
                        <input 
                          type="checkbox" 
                          :checked="isQuestionSelected(q.id)"
                          @click.stop
                          @change="toggleQuestionSelection(q)"
                        />
                      </div>
                      <div class="result-content-wrapper">
                        <div class="result-content">
                          <latex-renderer :content="q.content.substring(0, 100) + (q.content.length > 100 ? '...' : '')" />
                        </div>
                        <div class="result-meta">
                          <span class="tag-new" :class="getQuestionTypeClass(q.question_type)">{{ q.question_type }}</span>
                          <span class="tag-new" :class="getDifficultyClass(q.difficulty)">{{ q.difficulty }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 已选择数量提示 -->
                  <div v-if="sideA.tempSelected.length > 0" class="selection-bar">
                    <span>已选择 {{ sideA.tempSelected.length }} 道题目</span>
                    <button class="btn-new btn-sm-new btn-primary-new" @click="confirmSelection">
                      确认选择
                    </button>
                  </div>
                </div>
              </div>

              <!-- 已选题目展示 -->
              <div v-else class="selected-questions">
                <div class="selected-header">
                  <span class="selected-label">已选择 {{ sideA.selectedQuestions.length }} 道题目</span>
                  <button class="btn-new btn-sm-new btn-ghost-new" @click="clearSelectionA">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                    重新选择
                  </button>
                </div>
                
                <!-- 题目列表 -->
                <div class="selected-questions-list">
                  <div 
                    v-for="(q, index) in sideA.selectedQuestions" 
                    :key="q.id"
                    class="selected-question-item"
                  >
                    <div class="question-index">{{ index + 1 }}</div>
                    <div class="question-card-compact">
                      <div class="question-type-badge">
                        <span class="tag-new" :class="getQuestionTypeClass(q.question_type)">{{ q.question_type }}</span>
                        <span class="tag-new" :class="getDifficultyClass(q.difficulty)">{{ q.difficulty }}</span>
                      </div>
                      <div class="question-content-compact">
                        <latex-renderer :content="q.content.substring(0, 150) + (q.content.length > 150 ? '...' : '')" />
                      </div>
                    </div>
                    <button class="btn-remove" @click="removeSelectedQuestion(index)">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                </div>
                
                <!-- 添加更多题目 -->
                <button class="btn-new btn-ghost-new" style="width: 100%; margin-top: 16px;" @click="showSearchAgain">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  添加更多题目
                </button>
              </div>
            </div>
          </div>

          <!-- 中间对比标识 -->
          <div class="compare-divider">
            <div class="vs-badge">VS</div>
          </div>

          <!-- 右侧 B 区 - 真题上传 -->
          <div class="compare-panel panel-b">
            <div class="panel-header">
              <div class="panel-badge badge-b">B</div>
              <h3 class="panel-title">真题</h3>
              <span class="panel-subtitle">上传或输入真题</span>
            </div>
            
            <div class="panel-content">
              <!-- 输入方式切换 -->
              <div class="input-tabs">
                <button 
                  :class="['tab-btn', sideB.inputType === 'text' ? 'tab-active' : '']"
                  @click="sideB.inputType = 'text'"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                  </svg>
                  手动输入
                </button>
                <button 
                  :class="['tab-btn', sideB.inputType === 'file' ? 'tab-active' : '']"
                  @click="sideB.inputType = 'file'"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                  </svg>
                  文件上传
                </button>
              </div>

              <!-- 文本输入 -->
              <div v-if="sideB.inputType === 'text'" class="text-input-area">
                <div class="form-group">
                  <label class="form-label">题目内容 <span class="text-error">*</span></label>
                  <textarea 
                    class="form-textarea" 
                    v-model="sideB.question.content" 
                    rows="4"
                    placeholder="输入题目内容，支持LaTeX公式"
                  ></textarea>
                </div>

                <div class="form-grid-2">
                  <div class="form-group">
                    <label class="form-label">题型</label>
                    <select class="form-select" v-model="sideB.question.type">
                      <option value="单选">单选</option>
                      <option value="多选">多选</option>
                      <option value="判断">判断</option>
                      <option value="填空">填空</option>
                      <option value="主观">主观</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label class="form-label">难度</label>
                    <select class="form-select" v-model="sideB.question.difficulty">
                      <option value="L1">L1 记忆</option>
                      <option value="L2">L2 理解</option>
                      <option value="L3">L3 应用</option>
                      <option value="L4">L4 分析</option>
                      <option value="L5">L5 创造</option>
                    </select>
                  </div>
                </div>

                <!-- 选项输入 -->
                <div v-if="['单选', '多选', '判断'].includes(sideB.question.type)" class="form-group">
                  <label class="form-label">选项</label>
                  <div class="options-input-list">
                    <div v-for="(opt, idx) in sideB.question.options" :key="idx" class="option-input-item">
                      <span class="option-label">{{ String.fromCharCode(65 + idx) }}.</span>
                      <input 
                        type="text" 
                        class="form-input" 
                        v-model="opt.content" 
                        placeholder="选项内容"
                      />
                      <label class="checkbox-label">
                        <input type="checkbox" v-model="opt.is_correct" />
                        <span>正确</span>
                      </label>
                      <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="removeOptionB(idx)">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <button class="btn-new btn-ghost-new" style="width: 100%;" @click="addOptionB">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                      </svg>
                      添加选项
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">答案</label>
                  <input type="text" class="form-input" v-model="sideB.question.answer" placeholder="正确答案" />
                </div>

                <div class="form-group">
                  <label class="form-label">解析</label>
                  <textarea 
                    class="form-textarea" 
                    v-model="sideB.question.explanation" 
                    rows="3"
                    placeholder="答案解析"
                  ></textarea>
                </div>
              </div>

              <!-- 文件上传 -->
              <div v-else class="file-upload-area">
                <div 
                  class="upload-zone"
                  :class="{ 'upload-dragover': isDragging }"
                  @dragover.prevent="isDragging = true"
                  @dragleave.prevent="isDragging = false"
                  @drop.prevent="handleFileDrop"
                  @click="$refs.fileInput.click()"
                >
                  <input 
                    ref="fileInput"
                    type="file" 
                    style="display: none;"
                    accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
                    @change="handleFileSelect"
                  />
                  <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                  </svg>
                  <p class="upload-title">点击或拖拽文件到此处</p>
                  <p class="upload-desc">支持 PDF、Word、TXT、图片格式</p>
                </div>

                <!-- 已上传文件 -->
                <div v-if="sideB.uploadedFile" class="uploaded-file">
                  <div class="file-info">
                    <svg class="file-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <div class="file-details">
                      <div class="file-name">{{ sideB.uploadedFile.name }}</div>
                      <div class="file-size">{{ formatFileSize(sideB.uploadedFile.size) }}</div>
                    </div>
                  </div>
                  <button class="btn-new btn-sm-new" style="color: #dc2626;" @click="clearUploadedFile">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>

                <!-- OCR识别结果 -->
                <div v-if="sideB.ocrResult" class="ocr-result">
                  <div class="ocr-header">
                    <span class="ocr-label">识别结果</span>
                    <button class="btn-new btn-sm-new btn-ghost-new" @click="editOcrResult">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                      编辑
                    </button>
                  </div>
                  <div class="ocr-content">{{ sideB.ocrResult }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 整体对比结果 -->
    <section v-if="overallResult" class="content-card result-card">
      <div class="card-header">
        <div class="card-title">
          <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          AI 整体对比分析结果
        </div>
        <div class="result-badge" :class="'result-' + overallResult.winner">
          {{ overallResult.winner === 'A' ? '题库整体更优' : overallResult.winner === 'B' ? '真题整体更优' : '各有优劣' }}
        </div>
      </div>

      <div class="card-body">
        <!-- 评分对比 -->
        <div class="score-comparison">
          <div class="score-item">
            <div class="score-label">题库题目 (A)</div>
            <div class="score-bar">
              <div class="score-fill" :style="{ width: overallResult.scores.A + '%' }"></div>
            </div>
            <div class="score-value">{{ overallResult.scores.A }}分</div>
          </div>
          <div class="score-item">
            <div class="score-label">真题 (B)</div>
            <div class="score-bar">
              <div class="score-fill score-fill-b" :style="{ width: overallResult.scores.B + '%' }"></div>
            </div>
            <div class="score-value">{{ overallResult.scores.B }}分</div>
          </div>
        </div>

        <!-- 详细分析 -->
        <div class="analysis-section">
          <h4 class="analysis-title">整体分析</h4>
          <div class="analysis-content" v-html="formatAnalysis(overallResult.analysis)"></div>
        </div>

        <!-- 维度对比 -->
        <div v-if="overallResult.dimensions" class="dimensions-section">
          <h4 class="analysis-title">多维度对比</h4>
          <div class="dimensions-grid">
            <div v-for="(dim, key) in overallResult.dimensions" :key="key" class="dimension-item">
              <div class="dimension-name">{{ dim.name }}</div>
              <div class="dimension-compare">
                <div class="dim-score dim-a">{{ dim.scoreA }}</div>
                <div class="dim-bar">
                  <div class="dim-fill-a" :style="{ width: (dim.scoreA / (dim.scoreA + dim.scoreB || 1) * 100) + '%' }"></div>
                </div>
                <div class="dim-score dim-b">{{ dim.scoreB }}</div>
              </div>
              <div class="dimension-desc">{{ dim.description }}</div>
            </div>
          </div>
        </div>

        <!-- 改进建议 -->
        <div v-if="overallResult.suggestions" class="suggestions-section">
          <h4 class="analysis-title">改进建议</h4>
          <div class="suggestions-content">
            <div v-for="(suggestion, idx) in overallResult.suggestions" :key="idx" class="suggestion-item">
              <div class="suggestion-target">{{ suggestion.target === 'A' ? '题库题目' : '真题' }}</div>
              <div class="suggestion-text">{{ suggestion.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 逐题对比结果 -->
    <section v-if="compareResults.length > 0" class="content-card result-card">
      <div class="card-header">
        <div class="card-title">
          <svg class="title-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          AI 单题对比分析结果
        </div>
        <div class="result-badge" :class="'result-' + compareResults[0].winner">
          {{ compareResults[0].winner === 'A' ? '题库更优' : compareResults[0].winner === 'B' ? '真题更优' : '各有优劣' }}
        </div>
      </div>

      <div class="card-body">
        <!-- 评分对比 -->
        <div class="score-comparison">
          <div class="score-item">
            <div class="score-label">题库题目 (A)</div>
            <div class="score-bar">
              <div class="score-fill" :style="{ width: compareResults[0].scores.A + '%' }"></div>
            </div>
            <div class="score-value">{{ compareResults[0].scores.A }}分</div>
          </div>
          <div class="score-item">
            <div class="score-label">真题 (B)</div>
            <div class="score-bar">
              <div class="score-fill score-fill-b" :style="{ width: compareResults[0].scores.B + '%' }"></div>
            </div>
            <div class="score-value">{{ compareResults[0].scores.B }}分</div>
          </div>
        </div>

        <!-- 详细分析 -->
        <div class="analysis-section">
          <h4 class="analysis-title">详细分析</h4>
          <div class="analysis-content" v-html="formatAnalysis(compareResults[0].analysis)"></div>
        </div>

        <!-- 维度对比 -->
        <div v-if="compareResults[0].dimensions" class="dimensions-section">
          <h4 class="analysis-title">多维度对比</h4>
          <div class="dimensions-grid">
            <div v-for="(dim, key) in compareResults[0].dimensions" :key="key" class="dimension-item">
              <div class="dimension-name">{{ dim.name }}</div>
              <div class="dimension-compare">
                <div class="dim-score dim-a">{{ dim.scoreA }}</div>
                <div class="dim-bar">
                  <div class="dim-fill-a" :style="{ width: (dim.scoreA / (dim.scoreA + dim.scoreB || 1) * 100) + '%' }"></div>
                </div>
                <div class="dim-score dim-b">{{ dim.scoreB }}</div>
              </div>
              <div class="dimension-desc">{{ dim.description }}</div>
            </div>
          </div>
        </div>

        <!-- 改进建议 -->
        <div v-if="compareResults[0].suggestions" class="suggestions-section">
          <h4 class="analysis-title">改进建议</h4>
          <div class="suggestions-content">
            <div v-for="(suggestion, idx) in compareResults[0].suggestions" :key="idx" class="suggestion-item">
              <div class="suggestion-target">{{ suggestion.target === 'A' ? '题库题目' : '真题' }}</div>
              <div class="suggestion-text">{{ suggestion.content }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'QuestionCompare',
  data() {
    return {
      comparing: false,
      isDragging: false,
      sideA: {
        keyword: '',
        filter: {
          type: '',
          difficulty: ''
        },
        searchResults: [],
        selectedQuestions: [],
        tempSelected: []  // 临时选择，用于批量选择
      },
      sideB: {
        inputType: 'text',
        question: {
          content: '',
          type: '单选',
          difficulty: 'L2',
          options: [
            { content: '', is_correct: false },
            { content: '', is_correct: false }
          ],
          answer: '',
          explanation: ''
        },
        uploadedFile: null,
        ocrResult: ''
      },
      compareResults: [],
      expandedResults: [],
      compareMode: 'overall', // 'overall' - 整体对比, 'single' - 逐题对比
      overallResult: null // 整体对比结果
    }
  },
  computed: {
    canCompare() {
      const hasA = this.sideA.selectedQuestions.length > 0
      const hasB = this.sideB.inputType === 'text'
        ? this.sideB.question.content.trim() !== ''
        : this.sideB.ocrResult !== ''
      // 逐题对比模式要求题目数量相同
      if (this.compareMode === 'single' && hasA) {
        // 真题只能是一道题，所以题库题目也只能选一道
        return hasA && hasB && this.sideA.selectedQuestions.length === 1
      }
      return hasA && hasB
    },
    winCount() {
      const counts = { A: 0, B: 0, tie: 0 }
      this.compareResults.forEach(r => {
        if (r.winner && counts[r.winner] !== undefined) {
          counts[r.winner]++
        }
      })
      return counts
    }
  },
  methods: {
    // 搜索题库题目
    async searchQuestionsA() {
      try {
        const params = {
          page: 1,
          per_page: 20,
          question_type: this.sideA.filter.type || undefined,
          difficulty: this.sideA.filter.difficulty || undefined,
          keyword: this.sideA.keyword || undefined
        }
        const data = await this.$axios.get('/questions', { params })
        this.sideA.searchResults = data.questions || []
        // 重置临时选择
        this.sideA.tempSelected = []
      } catch (error) {
        console.error('搜索题目失败:', error)
        this.$message.error('搜索题目失败')
      }
    },
    
    // 检查题目是否已选择
    isQuestionSelected(questionId) {
      return this.sideA.tempSelected.some(q => q.id === questionId)
    },
    
    // 切换题目选择状态
    toggleQuestionSelection(question) {
      const index = this.sideA.tempSelected.findIndex(q => q.id === question.id)
      if (index > -1) {
        this.sideA.tempSelected.splice(index, 1)
      } else {
        this.sideA.tempSelected.push(question)
      }
    },
    
    // 全选搜索结果
    selectAllResults() {
      this.sideA.searchResults.forEach(q => {
        if (!this.isQuestionSelected(q.id)) {
          this.sideA.tempSelected.push(q)
        }
      })
    },
    
    // 确认选择
    confirmSelection() {
      this.sideA.selectedQuestions = [...this.sideA.tempSelected]
      this.sideA.searchResults = []
      this.sideA.keyword = ''
      this.sideA.tempSelected = []
    },
    
    // 显示搜索再次添加
    showSearchAgain() {
      this.sideA.searchResults = []
      this.sideA.keyword = ''
      this.sideA.tempSelected = []
    },
    
    // 移除已选题目
    removeSelectedQuestion(index) {
      this.sideA.selectedQuestions.splice(index, 1)
    },
    
    // 清除A区选择
    clearSelectionA() {
      this.sideA.selectedQuestions = []
      this.sideA.searchResults = []
      this.sideA.keyword = ''
      this.sideA.tempSelected = []
    },
    
    // 添加B区选项
    addOptionB() {
      this.sideB.question.options.push({ content: '', is_correct: false })
    },
    
    // 删除B区选项
    removeOptionB(index) {
      if (this.sideB.question.options.length <= 2) {
        this.$message.warning('至少需要保留两个选项')
        return
      }
      this.sideB.question.options.splice(index, 1)
    },
    
    // 文件选择
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.uploadFile(file)
      }
    },
    
    // 文件拖拽
    handleFileDrop(event) {
      this.isDragging = false
      const file = event.dataTransfer.files[0]
      if (file) {
        this.uploadFile(file)
      }
    },
    
    // 上传文件并OCR
    async uploadFile(file) {
      this.sideB.uploadedFile = file
      
      const formData = new FormData()
      formData.append('file', file)
      
      try {
        this.$message.info('正在识别文件内容...')
        const data = await this.$axios.post('/compare/upload-and-ocr', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        this.sideB.ocrResult = data.text || ''
        this.$message.success('文件识别成功')
      } catch (error) {
        console.error('文件识别失败:', error)
        this.$message.error('文件识别失败: ' + (error.message || '未知错误'))
      }
    },
    
    // 清除上传文件
    clearUploadedFile() {
      this.sideB.uploadedFile = null
      this.sideB.ocrResult = ''
    },
    
    // 编辑OCR结果
    editOcrResult() {
      this.sideB.inputType = 'text'
      this.sideB.question.content = this.sideB.ocrResult
    },
    
    // 开始对比
    async startCompare() {
      if (!this.canCompare) return

      this.comparing = true
      this.compareResults = []
      this.expandedResults = []
      this.overallResult = null

      try {
        if (this.compareMode === 'overall') {
          // 整体对比模式 - 使用新的批量API
          const payload = {
            questionsA: this.sideA.selectedQuestions,
            questionsB: [this.sideB.inputType === 'text'
              ? this.sideB.question
              : { content: this.sideB.ocrResult, question_type: '未知', difficulty: '未知' }],
            compareMode: 'overall'
          }

          const data = await this.$axios.post('/compare/batch', payload)

          if (data.compareMode === 'overall' && data.overallResult) {
            this.overallResult = data.overallResult
            this.$message.success('整体对比分析完成')
          }
        } else {
          // 逐题对比模式（单题对比）
          const questionA = this.sideA.selectedQuestions[0]

          const payload = {
            questionA: questionA,
            questionB: this.sideB.inputType === 'text'
              ? this.sideB.question
              : { content: this.sideB.ocrResult }
          }

          const data = await this.$axios.post('/compare/questions', payload)
          this.compareResults = [data]
          this.$message.success('单题对比分析完成')
        }
      } catch (error) {
        console.error('对比分析失败:', error)
        this.$message.error('对比分析失败: ' + (error.message || '未知错误'))
      } finally {
        this.comparing = false
      }
    },
    
    // 切换结果详情展开
    toggleResultDetail(index) {
      const pos = this.expandedResults.indexOf(index)
      if (pos > -1) {
        this.expandedResults.splice(pos, 1)
      } else {
        this.expandedResults.push(index)
      }
    },
    
    // 格式化文件大小
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    // 格式化分析文本
    formatAnalysis(text) {
      return text.replace(/\n/g, '<br>')
    },
    
    // 获取题型样式
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
    
    // 获取难度样式
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

// 对比容器
.compare-container {
  display: flex;
  gap: @spacing-lg;
  align-items: stretch;

  @media (max-width: @breakpoint-lg) {
    flex-direction: column;
  }
}

// 对比面板
.compare-panel {
  flex: 1;
  background: @bg-card;
  border-radius: @radius-lg;
  border: 1px solid @border-color;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: @spacing-lg;
  background: @bg-hover;
  border-bottom: 1px solid @border-color;
  display: flex;
  align-items: center;
  gap: @spacing-md;
}

.panel-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: @font-size-md;
  color: @text-white;
}

.badge-a {
  background: @primary-color;
}

.badge-b {
  background: #10b981;
}

.panel-title {
  font-size: @font-size-lg;
  font-weight: 600;
  color: @text-primary;
  margin: 0;
}

.panel-subtitle {
  font-size: @font-size-sm;
  color: @text-muted;
  margin-left: auto;
}

.panel-content {
  padding: @spacing-lg;
  flex: 1;
  overflow-y: auto;
}

// 头部操作区
.header-actions {
  display: flex;
  align-items: center;
  gap: @spacing-md;
}

// 对比模式选择器
.compare-mode-selector {
  display: flex;
  align-items: center;
  gap: @spacing-sm;
}

.mode-label {
  font-size: @font-size-sm;
  color: @text-secondary;
  white-space: nowrap;
}

.mode-select {
  width: 120px;
}

// 中间分隔线
.compare-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 @spacing-md;

  @media (max-width: @breakpoint-lg) {
    padding: @spacing-md 0;
  }
}

.vs-badge {
  width: 48px;
  height: 48px;
  background: @bg-card;
  border: 2px solid @border-color;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: @font-size-lg;
  color: @text-secondary;

  @media (max-width: @breakpoint-lg) {
    transform: rotate(90deg);
  }
}

// 题目选择器
.question-selector {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
}

.filter-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: @spacing-sm;
}

// 搜索结果
.search-results {
  margin-top: @spacing-md;
  border: 1px solid @border-color;
  border-radius: @radius-md;
  overflow: hidden;
}

.results-header {
  padding: @spacing-sm @spacing-md;
  background: @bg-hover;
  font-size: @font-size-sm;
  font-weight: 500;
  color: @text-secondary;
  border-bottom: 1px solid @border-color;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-list {
  max-height: 300px;
  overflow-y: auto;
}

.result-item {
  padding: @spacing-md;
  border-bottom: 1px solid @border-light;
  cursor: pointer;
  transition: background @transition-fast;
  display: flex;
  align-items: flex-start;
  gap: @spacing-sm;

  &:hover,
  &.result-selected {
    background: fade(@primary-color, 5%);
  }

  &:last-child {
    border-bottom: none;
  }
}

.result-checkbox {
  padding-top: 2px;
  
  input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
  }
}

.result-content-wrapper {
  flex: 1;
}

.result-content {
  font-size: @font-size-sm;
  color: @text-primary;
  margin-bottom: @spacing-sm;
  line-height: 1.5;
}

.result-meta {
  display: flex;
  gap: @spacing-xs;
}

// 选择栏
.selection-bar {
  padding: @spacing-md;
  background: fade(@primary-color, 10%);
  border-top: 1px solid fade(@primary-color, 20%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: @font-size-sm;
  font-weight: 500;
  color: @primary-color;
}

// 已选题目展示
.selected-questions {
  .selected-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: @spacing-md;
  }

  .selected-label {
    font-size: @font-size-sm;
    font-weight: 500;
    color: @success-color;
  }
}

.selected-questions-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
  max-height: 500px;
  overflow-y: auto;
}

.selected-question-item {
  display: flex;
  align-items: flex-start;
  gap: @spacing-sm;
  padding: @spacing-md;
  background: @bg-hover;
  border: 1px solid @border-color;
  border-radius: @radius-md;
}

.question-index {
  width: 24px;
  height: 24px;
  background: @primary-color;
  color: @text-white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: @font-size-xs;
  font-weight: 600;
  flex-shrink: 0;
}

.question-card-compact {
  flex: 1;
  min-width: 0;
}

.question-type-badge {
  display: flex;
  gap: @spacing-xs;
  margin-bottom: @spacing-xs;
}

.question-content-compact {
  font-size: @font-size-sm;
  color: @text-primary;
  line-height: 1.5;
}

.btn-remove {
  padding: @spacing-xs;
  color: @error-color;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: @radius-sm;
  
  &:hover {
    background: fade(@error-color, 10%);
  }
}

// 输入方式切换
.input-tabs {
  display: flex;
  gap: @spacing-xs;
  margin-bottom: @spacing-lg;
  border-bottom: 1px solid @border-color;
  padding-bottom: @spacing-md;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  padding: @spacing-sm @spacing-md;
  font-size: @font-size-sm;
  font-weight: 500;
  color: @text-secondary;
  background: transparent;
  border: 1px solid transparent;
  border-radius: @radius-md;
  cursor: pointer;
  transition: all @transition-fast;

  &:hover {
    background: @bg-hover;
    color: @text-primary;
  }

  &.tab-active {
    background: fade(@primary-color, 10%);
    color: @primary-color;
    border-color: fade(@primary-color, 20%);
  }
}

// 文本输入区
.text-input-area {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: @spacing-md;
}

.options-input-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
}

.option-input-item {
  display: flex;
  align-items: center;
  gap: @spacing-sm;

  .option-label {
    font-weight: 600;
    color: @text-secondary;
    min-width: 24px;
  }

  .form-input {
    flex: 1;
  }
}

// 文件上传区
.file-upload-area {
  display: flex;
  flex-direction: column;
  gap: @spacing-md;
}

.upload-zone {
  border: 2px dashed @border-color;
  border-radius: @radius-lg;
  padding: @spacing-2xl;
  text-align: center;
  cursor: pointer;
  transition: all @transition-fast;

  &:hover,
  &.upload-dragover {
    border-color: @primary-color;
    background: fade(@primary-color, 5%);
  }
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: @text-muted;
  margin-bottom: @spacing-md;
}

.upload-title {
  font-size: @font-size-md;
  font-weight: 500;
  color: @text-primary;
  margin-bottom: @spacing-xs;
}

.upload-desc {
  font-size: @font-size-sm;
  color: @text-muted;
}

// 已上传文件
.uploaded-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: @spacing-md;
  background: @bg-hover;
  border: 1px solid @border-color;
  border-radius: @radius-md;
}

.file-info {
  display: flex;
  align-items: center;
  gap: @spacing-md;
}

.file-icon {
  width: 40px;
  height: 40px;
  color: @primary-color;
}

.file-name {
  font-size: @font-size-sm;
  font-weight: 500;
  color: @text-primary;
}

.file-size {
  font-size: @font-size-xs;
  color: @text-muted;
}

// OCR结果
.ocr-result {
  border: 1px solid @border-color;
  border-radius: @radius-md;
  overflow: hidden;
}

.ocr-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: @spacing-sm @spacing-md;
  background: @bg-hover;
  border-bottom: 1px solid @border-color;
}

.ocr-label {
  font-size: @font-size-sm;
  font-weight: 500;
  color: @text-secondary;
}

.ocr-content {
  padding: @spacing-md;
  font-size: @font-size-sm;
  color: @text-primary;
  line-height: 1.6;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
}

// 结果卡片
.result-card {
  margin-top: @spacing-xl;
}

.result-summary {
  display: flex;
  gap: @spacing-md;
  align-items: center;
}

.summary-item {
  font-size: @font-size-sm;
  font-weight: 500;
  padding: @spacing-xs @spacing-md;
  border-radius: @radius-full;
  
  &.win-a {
    background: fade(@primary-color, 10%);
    color: @primary-color;
  }
  
  &.win-b {
    background: fade(#10b981, 10%);
    color: #10b981;
  }
  
  &.win-tie {
    background: fade(#f59e0b, 10%);
    color: #f59e0b;
  }
}

// 批量结果列表
.results-list-batch {
  display: flex;
  flex-direction: column;
  gap: @spacing-lg;
}

.result-item-batch {
  border: 1px solid @border-color;
  border-radius: @radius-lg;
  overflow: hidden;
}

.result-header-batch {
  padding: @spacing-md @spacing-lg;
  background: @bg-hover;
  border-bottom: 1px solid @border-color;
  display: flex;
  align-items: center;
  gap: @spacing-md;
  flex-wrap: wrap;
}

.result-index {
  font-size: @font-size-sm;
  font-weight: 600;
  color: @text-secondary;
}

.result-badge-batch {
  padding: @spacing-xs @spacing-md;
  border-radius: @radius-full;
  font-size: @font-size-xs;
  font-weight: 600;

  &.result-A {
    background: fade(@primary-color, 10%);
    color: @primary-color;
  }

  &.result-B {
    background: fade(#10b981, 10%);
    color: #10b981;
  }

  &.result-tie {
    background: fade(#f59e0b, 10%);
    color: #f59e0b;
  }
}

.result-scores-batch {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: @spacing-sm;
  font-size: @font-size-sm;
}

.score-a {
  color: @primary-color;
  font-weight: 600;
}

.score-b {
  color: #10b981;
  font-weight: 600;
}

.score-separator {
  color: @text-muted;
}

.result-content-batch {
  padding: @spacing-lg;
}

.result-question-preview {
  display: flex;
  gap: @spacing-md;
  margin-bottom: @spacing-md;
  padding: @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
}

.preview-label {
  font-size: @font-size-xs;
  font-weight: 500;
  color: @text-muted;
  white-space: nowrap;
}

.preview-text {
  flex: 1;
  font-size: @font-size-sm;
  color: @text-primary;
}

.result-analysis-short {
  font-size: @font-size-sm;
  color: @text-secondary;
  line-height: 1.6;
  margin-bottom: @spacing-md;
}

// 详细结果
.result-detail {
  margin-top: @spacing-lg;
  padding-top: @spacing-lg;
  border-top: 1px solid @border-color;
}

.analysis-full {
  font-size: @font-size-sm;
  color: @text-secondary;
  line-height: 1.8;
  margin-bottom: @spacing-lg;
}

.detail-title {
  font-size: @font-size-sm;
  font-weight: 600;
  color: @text-primary;
  margin-bottom: @spacing-md;
}

// 紧凑的维度对比
.dimensions-grid-compact {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: @spacing-md;
  margin-bottom: @spacing-lg;
}

.dimension-item-compact {
  padding: @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
}

.dimension-name-compact {
  font-size: @font-size-xs;
  font-weight: 500;
  color: @text-secondary;
  margin-bottom: @spacing-sm;
}

.dimension-bar-compact {
  display: flex;
  align-items: center;
  gap: @spacing-sm;
}

.dim-bar-bg {
  flex: 1;
  height: 6px;
  background: fade(#10b981, 20%);
  border-radius: @radius-full;
  overflow: hidden;
  position: relative;
}

.dim-fill-a {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: @primary-color;
  border-radius: @radius-full;
  transition: width 0.5s ease;
}

.dim-scores {
  display: flex;
  gap: @spacing-xs;
  font-size: @font-size-xs;
  font-weight: 600;
}

.dim-score-a {
  color: @primary-color;
}

.dim-score-b {
  color: #10b981;
}

// 紧凑的建议
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: @spacing-sm;
}

.suggestion-item-compact {
  display: flex;
  align-items: flex-start;
  gap: @spacing-sm;
  padding: @spacing-sm @spacing-md;
  background: @bg-hover;
  border-radius: @radius-md;
}

.suggestion-target-badge {
  padding: 2px 8px;
  border-radius: @radius-sm;
  font-size: @font-size-xs;
  font-weight: 500;
  white-space: nowrap;
  
  &.target-A {
    background: fade(@primary-color, 10%);
    color: @primary-color;
  }
  
  &.target-B {
    background: fade(#10b981, 10%);
    color: #10b981;
  }
}

.suggestion-text-compact {
  flex: 1;
  font-size: @font-size-sm;
  color: @text-primary;
  line-height: 1.5;
}

// 动画
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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

.text-error {
  color: @error-color;
}

// 响应式
@media (max-width: @breakpoint-lg) {
  .compare-container {
    flex-direction: column;
  }

  .compare-divider {
    padding: @spacing-md 0;
  }

  .vs-badge {
    transform: rotate(90deg);
  }

  .form-grid-2 {
    grid-template-columns: 1fr;
  }
  
  .dimensions-grid-compact {
    grid-template-columns: 1fr;
  }
  
  .result-header-batch {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .result-scores-batch {
    margin-left: 0;
  }
}
</style>
