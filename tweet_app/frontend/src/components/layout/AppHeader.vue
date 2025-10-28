<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Navigation -->
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <RouterLink to="/" class="flex items-center">
              <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-lg">T</span>
              </div>
              <span class="ml-2 text-xl font-semibold text-gray-900">TweetEval</span>
            </RouterLink>
          </div>

          <!-- Desktop Navigation -->
          <nav class="hidden md:ml-10 md:flex md:space-x-8">
            <RouterLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.to"
              class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-primary-600 transition-colors"
              :class="{ 'text-primary-600 border-b-2 border-primary-600': $route.name === item.name }"
            >
              {{ item.name }}
            </RouterLink>
          </nav>
        </div>

        <!-- Right side items -->
        <div class="flex items-center space-x-4">
          <!-- User Menu (when authenticated) -->
          <div v-if="authStore.isAuthenticated" class="relative">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <span class="text-gray-600 font-medium">
                  {{ authStore.user?.username?.charAt(0).toUpperCase() }}
                </span>
              </div>
            </button>

            <!-- User Dropdown -->
            <div
              v-if="showUserMenu"
              class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
            >
              <div class="py-1">
                <RouterLink
                  to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click="showUserMenu = false"
                >
                  Profile
                </RouterLink>
                <button
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Sign out
                </button>
              </div>
            </div>
          </div>

          <!-- Auth buttons (when not authenticated) -->
          <div v-else class="flex items-center space-x-4">
            <RouterLink
              to="/auth/login"
              class="btn-outline"
            >
              Sign in
            </RouterLink>
            <RouterLink
              to="/auth/register"
              class="btn-primary"
            >
              Sign up
            </RouterLink>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="showMobileMenu = !showMobileMenu"
            class="md:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <div v-if="showMobileMenu && authStore.isAuthenticated" class="md:hidden border-t border-gray-200 pt-4 pb-3">
        <div class="space-y-1">
          <RouterLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.to"
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="[
              $route.name === item.name
                ? 'bg-primary-50 border-primary-500 text-primary-700'
                : 'border-transparent text-gray-600 hover:text-gray-800 hover:bg-gray-50 hover:border-gray-300'
            ]"
            @click="showMobileMenu = false"
          >
            {{ item.name }}
          </RouterLink>
        </div>
        <div class="mt-3 pt-3 border-t border-gray-200">
          <RouterLink
            to="/profile"
            class="block pl-3 pr-4 py-2 text-base font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-50"
            @click="showMobileMenu = false"
          >
            Profile
          </RouterLink>
          <button
            @click="handleLogout"
            class="block w-full text-left pl-3 pr-4 py-2 text-base font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-50"
          >
            Sign out
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)

const navigation = [
  { name: 'Dashboard', to: '/' },
  { name: 'Datasets', to: '/datasets' },
  { name: 'Search', to: '/search' },
  { name: 'Analytics', to: '/analytics' },
]

const handleLogout = async () => {
  try {
    await authStore.logout()
    notificationStore.success('You have been logged out successfully')
    router.push('/auth/login')
  } catch (error) {
    notificationStore.error('Failed to logout')
  } finally {
    showUserMenu.value = false
    showMobileMenu.value = false
  }
}

// Close dropdowns when clicking outside
document.addEventListener('click', (event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showUserMenu.value = false
  }
})
</script>