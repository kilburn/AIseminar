import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginFormData, RegisterFormData } from '@/types'
import { authService } from '@/services/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value && !!accessToken.value)

  // Actions
  const login = async (formData: LoginFormData) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await authService.login(formData)

      // Store tokens
      accessToken.value = response.access_token
      refreshToken.value = response.refresh_token
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)

      // Store user data
      user.value = response.user

      return response
    } catch (err: any) {
      error.value = err.message || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (formData: RegisterFormData) => {
    try {
      isLoading.value = true
      error.value = null

      const response = await authService.register(formData)

      // Store tokens
      accessToken.value = response.access_token
      refreshToken.value = response.refresh_token
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)

      // Store user data
      user.value = response.user

      return response
    } catch (err: any) {
      error.value = err.message || 'Registration failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      if (accessToken.value) {
        await authService.logout()
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear state regardless of API call success
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  const refreshTokens = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available')
      }

      const response = await authService.refreshToken(refreshToken.value)

      // Update tokens
      accessToken.value = response.access_token
      refreshToken.value = response.refresh_token
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)

      return response
    } catch (err) {
      // If refresh fails, logout the user
      await logout()
      throw err
    }
  }

  const checkAuthStatus = async () => {
    try {
      if (!accessToken.value) {
        return
      }

      isLoading.value = true
      const userData = await authService.getCurrentUser()
      user.value = userData
    } catch (err: any) {
      // If current user call fails, try to refresh tokens
      if (err.response?.status === 401 && refreshToken.value) {
        try {
          await refreshTokens()
          const userData = await authService.getCurrentUser()
          user.value = userData
        } catch (refreshErr) {
          await logout()
        }
      } else {
        await logout()
      }
    } finally {
      isLoading.value = false
    }
  }

  const updateProfile = async (profileData: Partial<User>) => {
    try {
      isLoading.value = true
      error.value = null

      const updatedUser = await authService.updateProfile(profileData)
      user.value = updatedUser

      return updatedUser
    } catch (err: any) {
      error.value = err.message || 'Profile update failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,

    // Getters
    isAuthenticated,

    // Actions
    login,
    register,
    logout,
    refreshTokens,
    checkAuthStatus,
    updateProfile,
    clearError
  }
})