<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900">Analytics Dashboard</h1>
        <p class="mt-2 text-sm text-gray-700">
          Explore insights and patterns from your tweet analysis with interactive visualizations.
        </p>
      </div>

      <!-- Coming Soon Placeholder -->
      <div class="card text-center py-12">
        <div class="w-16 h-16 bg-yellow-100 rounded-lg flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Coming Soon</h3>
        <p class="text-gray-600 mb-6">
          Analytics and visualization features will be available in Phase 5 of the implementation.
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