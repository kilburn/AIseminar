<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900">Profile</h1>
        <p class="mt-2 text-sm text-gray-700">
          Manage your account settings and preferences.
        </p>
      </div>

      <!-- Coming Soon Placeholder -->
      <div class="card text-center py-12">
        <div class="w-16 h-16 bg-yellow-100 rounded-lg flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Coming Soon</h3>
        <p class="text-gray-600 mb-6">
          Profile management features will be available in Phase 4 of the implementation.
        </p>
        <RouterLink to="/" class="btn-outline">
          Return to Dashboard
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>