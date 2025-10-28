import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token to requests
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Handle 401 errors
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const authStore = useAuthStore()

      try {
        // Try to refresh the token
        await authStore.refreshTokens()

        // Retry the original request with new token
        if (authStore.accessToken) {
          originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // If refresh fails, logout and redirect to login
        await authStore.logout()

        // Show notification
        const notificationStore = useNotificationStore()
        notificationStore.error('Your session has expired. Please log in again.')

        // Redirect to login page
        if (window.location.pathname !== '/auth/login') {
          window.location.href = '/auth/login'
        }
      }
    }

    // Handle other errors
    const notificationStore = useNotificationStore()

    if (error.response?.status >= 500) {
      notificationStore.error('Server error. Please try again later.')
    } else if (error.response?.status === 429) {
      notificationStore.error('Too many requests. Please wait and try again.')
    } else if (error.code === 'ECONNABORTED') {
      notificationStore.error('Request timeout. Please check your connection and try again.')
    } else if (!error.response) {
      notificationStore.error('Network error. Please check your connection.')
    }

    return Promise.reject(error)
  }
)

// API wrapper functions
export const api = {
  get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.get(url, config).then(response => response.data)
  },

  post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.post(url, data, config).then(response => response.data)
  },

  put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.put(url, data, config).then(response => response.data)
  },

  patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.patch(url, data, config).then(response => response.data)
  },

  delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.delete(url, config).then(response => response.data)
  },

  // File upload
  upload: <T = any>(url: string, file: File, config?: AxiosRequestConfig): Promise<T> => {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post(url, formData, {
      ...config,
      headers: {
        ...config?.headers,
        'Content-Type': 'multipart/form-data',
      },
    }).then(response => response.data)
  },

  // Download file
  download: (url: string, filename?: string): Promise<void> => {
    return apiClient.get(url, {
      responseType: 'blob',
    }).then(response => {
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    })
  },
}

export default apiClient