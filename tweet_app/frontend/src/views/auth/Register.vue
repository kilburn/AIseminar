<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center mb-8">
        <div class="flex justify-center">
          <div class="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-xl">T</span>
          </div>
        </div>
        <h2 class="mt-4 text-3xl font-bold text-gray-900">Create your account</h2>
        <p class="mt-2 text-sm text-gray-600">
          Already have an account?
          <RouterLink to="/auth/login" class="font-medium text-primary-600 hover:text-primary-500">
            Sign in here
          </RouterLink>
        </p>
      </div>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">
              Username
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="formData.username"
                name="username"
                type="text"
                required
                class="input"
                :class="{ 'border-red-500': errors.username }"
              />
              <p v-if="errors.username" class="mt-1 text-sm text-red-600">{{ errors.username }}</p>
            </div>
          </div>

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
            <label for="full_name" class="block text-sm font-medium text-gray-700">
              Full name (optional)
            </label>
            <div class="mt-1">
              <input
                id="full_name"
                v-model="formData.full_name"
                name="full_name"
                type="text"
                class="input"
              />
            </div>
          </div>

          <div>
            <label for="organization" class="block text-sm font-medium text-gray-700">
              Organization (optional)
            </label>
            <div class="mt-1">
              <input
                id="organization"
                v-model="formData.organization"
                name="organization"
                type="text"
                class="input"
              />
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
                required
                class="input"
                :class="{ 'border-red-500': errors.password }"
              />
              <p v-if="errors.password" class="mt-1 text-sm text-red-600">{{ errors.password }}</p>
            </div>
          </div>

          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700">
              Confirm password
            </label>
            <div class="mt-1">
              <input
                id="confirm_password"
                v-model="formData.confirm_password"
                name="confirm_password"
                type="password"
                required
                class="input"
                :class="{ 'border-red-500': errors.confirm_password }"
              />
              <p v-if="errors.confirm_password" class="mt-1 text-sm text-red-600">{{ errors.confirm_password }}</p>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="w-full btn-primary"
            >
              <span v-if="authStore.isLoading" class="loading-spinner mr-2"></span>
              {{ authStore.isLoading ? 'Creating account...' : 'Create account' }}
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
import type { RegisterFormData } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const formData = reactive<RegisterFormData>({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  full_name: '',
  organization: ''
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: ''
})

const validateForm = (): boolean => {
  let isValid = true

  // Reset errors
  errors.username = ''
  errors.email = ''
  errors.password = ''
  errors.confirm_password = ''

  // Username validation
  if (!formData.username) {
    errors.username = 'Username is required'
    isValid = false
  } else if (formData.username.length < 3) {
    errors.username = 'Username must be at least 3 characters'
    isValid = false
  }

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
  } else if (formData.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  }

  // Confirm password validation
  if (!formData.confirm_password) {
    errors.confirm_password = 'Please confirm your password'
    isValid = false
  } else if (formData.password !== formData.confirm_password) {
    errors.confirm_password = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) return

  try {
    await authStore.register(formData)
    notificationStore.success('Account created successfully! Welcome!')
    router.push('/')
  } catch (error: any) {
    if (error.response?.data?.detail) {
      notificationStore.error(error.response.data.detail)
    } else {
      notificationStore.error('Registration failed. Please try again.')
    }
  }
}
</script>