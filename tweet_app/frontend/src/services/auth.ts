import { api } from './api'
import type { User, LoginFormData, RegisterFormData } from '@/types'

interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

interface RegisterResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

interface RefreshTokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export const authService = {
  // Login user
  async login(formData: LoginFormData): Promise<LoginResponse> {
    return api.post('/auth/login', formData)
  },

  // Register new user
  async register(formData: RegisterFormData): Promise<RegisterResponse> {
    return api.post('/auth/register', formData)
  },

  // Logout user
  async logout(): Promise<void> {
    return api.post('/auth/logout')
  },

  // Refresh access token
  async refreshToken(refreshToken: string): Promise<RefreshTokenResponse> {
    return api.post('/auth/refresh', { refresh_token: refreshToken })
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    return api.get('/auth/me')
  },

  // Update user profile
  async updateProfile(profileData: Partial<User>): Promise<User> {
    return api.put('/auth/profile', profileData)
  },

  // Change password
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    return api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  },

  // Request password reset
  async requestPasswordReset(email: string): Promise<void> {
    return api.post('/auth/forgot-password', { email })
  },

  // Reset password with token
  async resetPassword(token: string, newPassword: string): Promise<void> {
    return api.post('/auth/reset-password', {
      token,
      new_password: newPassword,
    })
  },

  // Verify email
  async verifyEmail(token: string): Promise<void> {
    return api.post('/auth/verify-email', { token })
  },

  // Resend verification email
  async resendVerificationEmail(): Promise<void> {
    return api.post('/auth/resend-verification')
  },
}