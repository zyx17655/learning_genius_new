import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5001/api',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
axiosInstance.interceptors.request.use(
  config => {
    // 可以在这里添加认证信息等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
axiosInstance.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      // 处理错误响应
      switch (error.response.status) {
        case 401:
          // 未授权处理
          break
        case 404:
          // 资源不存在处理
          break
        case 500:
          // 服务器错误处理
          break
        default:
          // 其他错误处理
          break
      }
    }
    return Promise.reject(error)
  }
)

export default axiosInstance