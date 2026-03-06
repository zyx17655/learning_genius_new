import axios from 'axios'

const API_BASE_URL = 'http://localhost:5001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  getKnowledgePoints() {
    return api.get('/knowledge-points')
  },
  
  getQuestions(params) {
    return api.get('/questions', { params })
  },
  
  getQuestion(id) {
    return api.get(`/questions/${id}`)
  },
  
  createQuestion(data) {
    return api.post('/questions', data)
  },
  
  updateQuestion(id, data) {
    return api.put(`/questions/${id}`, data)
  },
  
  deleteQuestion(id) {
    return api.delete(`/questions/${id}`)
  },
  
  reviewQuestion(id, reviewer = '系统') {
    return api.post(`/questions/${id}/review`, null, { params: { reviewer } })
  },
  
  batchReview(ids, reviewer = '系统') {
    return api.post('/questions/batch-review', ids, { params: { reviewer } })
  },
  
  batchDraft(ids) {
    return api.post('/questions/batch-draft', ids)
  },
  
  batchDelete(ids) {
    return api.post('/questions/batch-delete', ids)
  },
  
  getStats() {
    return api.get('/stats')
  },
  
  generateQuestions(data) {
    return api.post('/ai/generate', data)
  },
  
  getGeneratedQuestions(taskId) {
    return api.get(`/ai/tasks/${taskId}/questions`)
  },
  
  adoptQuestions(taskId, questionIds) {
    return api.post(`/ai/tasks/${taskId}/adopt`, questionIds)
  },
  
  toggleDraft(questionId) {
    return api.post(`/ai/questions/${questionId}/toggle-draft`)
  },
  
  toggleDiscard(questionId) {
    return api.post(`/ai/questions/${questionId}/toggle-discard`)
  },
  
  updateGeneratedQuestion(questionId, data) {
    return api.put(`/ai/questions/${questionId}`, data)
  },
  
  getKnowledgeDocuments() {
    return api.get('/knowledge/documents')
  },
  
  uploadKnowledgeDocument(formData, onProgress) {
    return api.post('/knowledge/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: onProgress
    })
  },
  
  deleteKnowledgeDocument(id) {
    return api.delete(`/knowledge/documents/${id}`)
  },
  
  getKnowledgeCategories() {
    return api.get('/knowledge/categories')
  },
  
  searchKnowledge(params) {
    return api.post('/knowledge/search', params)
  },
  
  getKnowledgeChunks(category, maxChars = 6000) {
    return api.get(`/knowledge/chunks/${category}`, { params: { max_chars: maxChars } })
  },
  
  getKnowledgeStats() {
    return api.get('/knowledge/stats')
  }
}
