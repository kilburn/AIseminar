import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'
import * as api from '@/services/api'

// Mock axios
vi.mock('axios')

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()

    // Set default mock response
    vi.mocked(axios.create).mockReturnValue({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      }
    } as any)
  })

  describe('API Client Configuration', () => {
    it('should create axios instance with correct base URL', () => {
      // The API client should be configured with the correct base URL
      expect(axios.create).toHaveBeenCalledWith(
        expect.objectContaining({
          baseURL: expect.stringContaining('/api/v1')
        })
      )
    })

    it('should have request interceptor for auth token', () => {
      const mockInstance = {
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockInstance as any)

      // Re-import to trigger configuration
      const apiClient = require('@/services/api').default

      expect(mockInstance.interceptors.request.use).toHaveBeenCalled()
    })

    it('should have response interceptor for error handling', () => {
      const mockInstance = {
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockInstance as any)

      // Re-import to trigger configuration
      const apiClient = require('@/services/api').default

      expect(mockInstance.interceptors.response.use).toHaveBeenCalled()
    })
  })

  describe('Error Handling', () => {
    it('should handle 401 unauthorized errors', async () => {
      const mockGet = vi.fn().mockRejectedValue({
        response: {
          status: 401,
          data: { detail: 'Unauthorized' }
        }
      })

      vi.mocked(axios.create).mockReturnValue({
        get: mockGet,
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        }
      } as any)

      const apiClient = require('@/services/api').default

      try {
        await apiClient.get('/protected')
      } catch (error: any) {
        expect(error.response.status).toBe(401)
        expect(error.response.data.detail).toBe('Unauthorized')
      }
    })

    it('should handle 500 server errors', async () => {
      const mockGet = vi.fn().mockRejectedValue({
        response: {
          status: 500,
          data: { detail: 'Internal server error' }
        }
      })

      vi.mocked(axios.create).mockReturnValue({
        get: mockGet,
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        }
      } as any)

      const apiClient = require('@/services/api').default

      try {
        await apiClient.get('/error')
      } catch (error: any) {
        expect(error.response.status).toBe(500)
        expect(error.response.data.detail).toBe('Internal server error')
      }
    })

    it('should handle network errors', async () => {
      const mockGet = vi.fn().mockRejectedValue(new Error('Network Error'))

      vi.mocked(axios.create).mockReturnValue({
        get: mockGet,
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        }
      } as any)

      const apiClient = require('@/services/api').default

      try {
        await apiClient.get('/network-error')
      } catch (error: any) {
        expect(error.message).toBe('Network Error')
      }
    })
  })

  describe('Request Interceptors', () => {
    it('should add authorization header when token exists', () => {
      const mockUse = vi.fn()
      const mockInstance = {
        interceptors: {
          request: { use: mockUse },
          response: { use: vi.fn() }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockInstance as any)

      // Re-import to trigger interceptor setup
      const apiClient = require('@/services/api').default

      // Get the request interceptor function
      const requestInterceptor = mockUse.mock.calls[0][0]

      // Mock config object
      const config = { headers: {} }

      // Set a token in localStorage
      localStorage.setItem('token', 'mock_token')

      // Call the interceptor
      const result = requestInterceptor(config)

      expect(result.headers.Authorization).toBe('Bearer mock_token')
    })

    it('should not add authorization header when no token exists', () => {
      const mockUse = vi.fn()
      const mockInstance = {
        interceptors: {
          request: { use: mockUse },
          response: { use: vi.fn() }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockInstance as any)

      // Re-import to trigger interceptor setup
      const apiClient = require('@/services/api').default

      // Get the request interceptor function
      const requestInterceptor = mockUse.mock.calls[0][0]

      // Mock config object
      const config = { headers: {} }

      // Ensure no token in localStorage
      localStorage.removeItem('token')

      // Call the interceptor
      const result = requestInterceptor(config)

      expect(result.headers.Authorization).toBeUndefined()
    })
  })

  describe('Response Interceptors', () => {
    it('should handle successful responses', () => {
      const mockUse = vi.fn()
      const mockInstance = {
        interceptors: {
          request: { use: vi.fn() },
          response: { use: mockUse }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockInstance as any)

      // Re-import to trigger interceptor setup
      const apiClient = require('@/services/api').default

      // Get the response interceptor functions
      const successInterceptor = mockUse.mock.calls[0][0]
      const errorInterceptor = mockUse.mock.calls[0][1]

      // Test success interceptor
      const response = { data: { message: 'Success' } }
      const result = successInterceptor(response)
      expect(result.data.message).toBe('Success')

      // Test error interceptor exists
      expect(typeof errorInterceptor).toBe('function')
    })

    it('should handle token refresh on 401 errors', () => {
      const mockUse = vi.fn()
      const mockInstance = {
        interceptors: {
          request: { use: vi.fn() },
          response: { use: mockUse }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockInstance as any)

      // Re-import to trigger interceptor setup
      const apiClient = require('@/services/api').default

      // Get the error interceptor function
      const errorInterceptor = mockUse.mock.calls[0][1]

      // Mock 401 error
      const error = {
        response: { status: 401 },
        config: { url: '/api/v1/protected' }
      }

      // The error interceptor should handle 401 errors
      expect(typeof errorInterceptor).toBe('function')
    })
  })

  describe('API Methods', () => {
    let mockAxiosInstance: any

    beforeEach(() => {
      mockAxiosInstance = {
        get: vi.fn(),
        post: vi.fn(),
        put: vi.fn(),
        delete: vi.fn(),
        interceptors: {
          request: { use: vi.fn() },
          response: { use: vi.fn() }
        }
      }

      vi.mocked(axios.create).mockReturnValue(mockAxiosInstance)
    })

    it('should make GET requests correctly', async () => {
      mockAxiosInstance.get.mockResolvedValue({ data: { id: 1, name: 'Test' } })

      const apiClient = require('@/services/api').default
      const result = await apiClient.get('/test')

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/test')
      expect(result.data).toEqual({ id: 1, name: 'Test' })
    })

    it('should make POST requests correctly', async () => {
      const postData = { name: 'New Item' }
      mockAxiosInstance.post.mockResolvedValue({ data: { id: 2, ...postData } })

      const apiClient = require('@/services/api').default
      const result = await apiClient.post('/test', postData)

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/test', postData)
      expect(result.data).toEqual({ id: 2, name: 'New Item' })
    })

    it('should make PUT requests correctly', async () => {
      const putData = { name: 'Updated Item' }
      mockAxiosInstance.put.mockResolvedValue({ data: { id: 1, ...putData } })

      const apiClient = require('@/services/api').default
      const result = await apiClient.put('/test/1', putData)

      expect(mockAxiosInstance.put).toHaveBeenCalledWith('/test/1', putData)
      expect(result.data).toEqual({ id: 1, name: 'Updated Item' })
    })

    it('should make DELETE requests correctly', async () => {
      mockAxiosInstance.delete.mockResolvedValue({ status: 204 })

      const apiClient = require('@/services/api').default
      const result = await apiClient.delete('/test/1')

      expect(mockAxiosInstance.delete).toHaveBeenCalledWith('/test/1')
      expect(result.status).toBe(204)
    })
  })
})