<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <div class="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">404</h1>
        <h2 class="text-xl font-medium text-gray-600 mb-4">Page not found</h2>
        <p class="text-gray-600 mb-8">
          Sorry, we couldn't find the page you're looking for. The page might have been removed or is temporarily unavailable.
        </p>
        <div class="space-y-4">
          <RouterLink
            to="/"
            class="btn-primary w-full"
          >
            Go back home
          </RouterLink>
          <button
            @click="$router.go(-1)"
            class="btn-outline w-full"
          >
            Go back
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>