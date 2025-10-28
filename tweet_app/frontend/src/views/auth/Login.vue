<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center mb-8">
        <div class="flex justify-center">
          <div class="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-xl">T</span>
          </div>
        </div>
        <h2 class="mt-4 text-3xl font-bold text-gray-900">Sign in to your account</h2>
        <p class="mt-2 text-sm text-gray-600">
          Or
          <RouterLink to="/auth/register" class="font-medium text-primary-600 hover:text-primary-500">
            create a new account
          </RouterLink>
        </p>
      </div>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <div class="mt-1">
              <input
                id="email"
                v-model="formData.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input"
                :class="{ 'border-red-500': errors.email }"
              />
              <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="formData.password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="input"
                :class="{ 'border-red-500': errors.password }"
              />
              <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember"
                v-model="formData.remember"
                name="remember"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="remember" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="w-full btn-primary"
            >
              <span v-if="authStore.isLoading" class="loading-spinner mr-2"></span>
              {{ authStore.isLoading ? 'Signing in...' : 'Sign in' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'
import type { LoginFormData } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const formData = reactive<LoginFormData>({
  email: '',
  password: '',
  remember: false
})

const errors = reactive({
  email: '',
  password: ''
})

const validateForm = (): boolean => {
  let isValid = true

  // Reset errors
  errors.email = ''
  errors.password = ''

  // Email validation
  if (!formData.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  // Password validation
  if (!formData.password) {
    errors.password = 'Password is required'
    isValid = false
  }

  return isValid
}

const handleLogin = async () => {
  if (!validateForm()) return

  try {
    await authStore.login(formData)
    notificationStore.success('Welcome back!')

    // Redirect to intended page or dashboard
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/')
  } catch (error: any) {
    if (error.response?.data?.detail) {
      notificationStore.error(error.response.data.detail)
    } else {
      notificationStore.error('Login failed. Please try again.')
    }
  }
}
</script>