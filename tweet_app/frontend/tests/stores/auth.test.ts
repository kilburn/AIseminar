import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import * as authApi from '@/services/api/auth'

// Mock the auth API
vi.mock('@/services/api/auth', () => ({
  login: vi.fn(),
  logout: vi.fn(),
  register: vi.fn(),
  refreshToken: vi.fn(),
  getCurrentUser: vi.fn(),
}))

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()

    // Reset localStorage
    localStorage.clear()
  })

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const authStore = useAuthStore()

      expect(authStore.user).toBeNull()
      expect(authStore.isAuthenticated).toBe(false)
      expect(authStore.token).toBeNull()
      expect(authStore.refreshToken).toBeNull()
      expect(authStore.loading).toBe(false)
      expect(authStore.error).toBeNull()
    })
  })

  describe('Login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        access_token: 'mock_access_token',
        refresh_token: 'mock_refresh_token',
        token_type: 'bearer',
        user: {
          id: '123',
          username: 'testuser',
          email: 'test@example.com',
          full_name: 'Test User'
        }
      }

      vi.mocked(authApi.login).mockResolvedValue(mockResponse)

      const authStore = useAuthStore()

      await authStore.login({
        username: 'test@example.com',
        password: 'password123'
      })

      expect(authStore.loading).toBe(false)
      expect(authStore.isAuthenticated).toBe(true)
      expect(authStore.token).toBe('mock_access_token')
      expect(authStore.refreshToken).toBe('mock_refresh_token')
      expect(authStore.user).toEqual(mockResponse.user)
      expect(authStore.error).toBeNull()
      expect(localStorage.getItem('token')).toBe('mock_access_token')
      expect(localStorage.getItem('refreshToken')).toBe('mock_refresh_token')
    })

    it('should handle login failure', async () => {
      const mockError = new Error('Invalid credentials')
      vi.mocked(authApi.login).mockRejectedValue(mockError)

      const authStore = useAuthStore()

      await authStore.login({
        username: 'test@example.com',
        password: 'wrongpassword'
      })

      expect(authStore.loading).toBe(false)
      expect(authStore.isAuthenticated).toBe(false)
      expect(authStore.token).toBeNull()
      expect(authStore.refreshToken).toBeNull()
      expect(authStore.user).toBeNull()
      expect(authStore.error).toBe('Invalid credentials')
      expect(localStorage.getItem('token')).toBeNull()
      expect(localStorage.getItem('refreshToken')).toBeNull()
    })
  })

  describe('Register', () => {
    it('should register successfully', async () => {
      const mockUser = {
        id: '123',
        username: 'testuser',
        email: 'test@example.com',
        full_name: 'Test User'
      }

      vi.mocked(authApi.register).mockResolvedValue(mockUser)

      const authStore = useAuthStore()

      await authStore.register({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User'
      })

      expect(authStore.loading).toBe(false)
      expect(authStore.error).toBeNull()
      // User should not be logged in immediately after registration
      expect(authStore.isAuthenticated).toBe(false)
    })

    it('should handle registration failure', async () => {
      const mockError = new Error('User already exists')
      vi.mocked(authApi.register).mockRejectedValue(mockError)

      const authStore = useAuthStore()

      await authStore.register({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123'
      })

      expect(authStore.loading).toBe(false)
      expect(authStore.error).toBe('User already exists')
    })
  })

  describe('Logout', () => {
    it('should logout successfully', async () => {
      // Setup logged in state
      const authStore = useAuthStore()
      authStore.token = 'mock_token'
      authStore.refreshToken = 'mock_refresh_token'
      authStore.user = { id: '123', username: 'testuser' }
      authStore.isAuthenticated = true

      // Set localStorage
      localStorage.setItem('token', 'mock_token')
      localStorage.setItem('refreshToken', 'mock_refresh_token')

      vi.mocked(authApi.logout).mockResolvedValue(undefined)

      await authStore.logout()

      expect(authStore.user).toBeNull()
      expect(authStore.isAuthenticated).toBe(false)
      expect(authStore.token).toBeNull()
      expect(authStore.refreshToken).toBeNull()
      expect(localStorage.getItem('token')).toBeNull()
      expect(localStorage.getItem('refreshToken')).toBeNull()
    })
  })

  describe('Get Current User', () => {
    it('should fetch current user successfully', async () => {
      const mockUser = {
        id: '123',
        username: 'testuser',
        email: 'test@example.com',
        full_name: 'Test User'
      }

      vi.mocked(authApi.getCurrentUser).mockResolvedValue(mockUser)

      const authStore = useAuthStore()

      await authStore.getCurrentUser()

      expect(authStore.user).toEqual(mockUser)
      expect(authStore.loading).toBe(false)
      expect(authStore.error).toBeNull()
    })

    it('should handle getting current user failure', async () => {
      const mockError = new Error('Not authenticated')
      vi.mocked(authApi.getCurrentUser).mockRejectedValue(mockError)

      const authStore = useAuthStore()

      await authStore.getCurrentUser()

      expect(authStore.user).toBeNull()
      expect(authStore.loading).toBe(false)
      expect(authStore.error).toBe('Not authenticated')
    })
  })

  describe('Token Management', () => {
    it('should initialize from localStorage', () => {
      localStorage.setItem('token', 'stored_token')
      localStorage.setItem('refreshToken', 'stored_refresh_token')

      const authStore = useAuthStore()

      expect(authStore.token).toBe('stored_token')
      expect(authStore.refreshToken).toBe('stored_refresh_token')
    })

    it('should clear tokens on error', () => {
      const authStore = useAuthStore()
      authStore.token = 'mock_token'
      authStore.refreshToken = 'mock_refresh_token'
      authStore.isAuthenticated = true

      localStorage.setItem('token', 'mock_token')
      localStorage.setItem('refreshToken', 'mock_refresh_token')

      authStore.clearTokens()

      expect(authStore.token).toBeNull()
      expect(authStore.refreshToken).toBeNull()
      expect(authStore.isAuthenticated).toBe(false)
      expect(localStorage.getItem('token')).toBeNull()
      expect(localStorage.getItem('refreshToken')).toBeNull()
    })
  })
})