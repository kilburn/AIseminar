<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="flex-1">
      <RouterView />
    </main>

    <!-- Footer -->
    <AppFooter />

    <!-- Global Notifications -->
    <NotificationContainer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import NotificationContainer from '@/components/ui/NotificationContainer.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  // Check authentication status on app load
  await authStore.checkAuthStatus()
})
</script>