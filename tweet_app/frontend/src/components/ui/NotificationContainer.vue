<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 space-y-2">
      <TransitionGroup
        name="notification"
        tag="div"
        class="space-y-2"
      >
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[notificationClasses(notification.type), 'max-w-sm w-full']"
        >
          <div class="flex items-start">
            <!-- Icon -->
            <div class="flex-shrink-0">
              <component
                :is="iconComponent(notification.type)"
                class="w-5 h-5"
                :class="iconClasses(notification.type)"
              />
            </div>

            <!-- Content -->
            <div class="ml-3 flex-1">
              <h4 v-if="notification.title" class="text-sm font-medium">
                {{ notification.title }}
              </h4>
              <p class="text-sm" :class="notification.title ? 'mt-1 text-gray-600' : ''">
                {{ notification.message }}
              </p>
            </div>

            <!-- Close button -->
            <button
              @click="removeNotification(notification.id)"
              class="ml-4 flex-shrink-0 p-1 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2"
            >
              <svg class="w-4 h-4 text-gray-400 hover:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNotificationStore } from '@/stores/notifications'
import type { Notification } from '@/stores/notifications'

// Icons
const CheckCircleIcon = () => (
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
  </svg>
)

const XCircleIcon = () => (
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
  </svg>
)

const ExclamationIcon = () => (
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
  </svg>
)

const InformationCircleIcon = () => (
  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
  </svg>
)

const notificationStore = useNotificationStore()

const notifications = computed(() => notificationStore.notifications)

const notificationClasses = (type: Notification['type']) => {
  const baseClasses = 'max-w-sm w-full p-4 rounded-lg shadow-lg border'

  switch (type) {
    case 'success':
      return `${baseClasses} bg-green-50 border-green-200`
    case 'error':
      return `${baseClasses} bg-red-50 border-red-200`
    case 'warning':
      return `${baseClasses} bg-yellow-50 border-yellow-200`
    case 'info':
      return `${baseClasses} bg-blue-50 border-blue-200`
    default:
      return `${baseClasses} bg-white border-gray-200`
  }
}

const iconClasses = (type: Notification['type']) => {
  switch (type) {
    case 'success':
      return 'text-green-400'
    case 'error':
      return 'text-red-400'
    case 'warning':
      return 'text-yellow-400'
    case 'info':
      return 'text-blue-400'
    default:
      return 'text-gray-400'
  }
}

const iconComponent = (type: Notification['type']) => {
  switch (type) {
    case 'success':
      return CheckCircleIcon
    case 'error':
      return XCircleIcon
    case 'warning':
      return ExclamationIcon
    case 'info':
      return InformationCircleIcon
    default:
      return InformationCircleIcon
  }
}

const removeNotification = (id: string) => {
  notificationStore.removeNotification(id)
}
</script>

<style scoped>
/* Transition animations */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>