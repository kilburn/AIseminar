import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration?: number
  persistent?: boolean
  timestamp: number
}

export const useNotificationStore = defineStore('notifications', () => {
  // State
  const notifications = ref<Notification[]>([])

  // Actions
  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp'>) => {
    const id = Date.now().toString()
    const newNotification: Notification = {
      ...notification,
      id,
      timestamp: Date.now(),
    }

    notifications.value.push(newNotification)

    // Auto-remove notification after duration (if not persistent)
    if (!notification.persistent && notification.duration !== 0) {
      const duration = notification.duration || 5000
      setTimeout(() => {
        removeNotification(id)
      }, duration)
    }

    return id
  }

  const removeNotification = (id: string) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearNotifications = () => {
    notifications.value = []
  }

  // Convenience methods
  const success = (message: string, title?: string, options?: Partial<Omit<Notification, 'id' | 'timestamp' | 'type' | 'message' | 'title'>>) => {
    return addNotification({
      type: 'success',
      message,
      title,
      ...options,
    })
  }

  const error = (message: string, title?: string, options?: Partial<Omit<Notification, 'id' | 'timestamp' | 'type' | 'message' | 'title'>>) => {
    return addNotification({
      type: 'error',
      message,
      title,
      duration: 0, // Errors are persistent by default
      ...options,
    })
  }

  const warning = (message: string, title?: string, options?: Partial<Omit<Notification, 'id' | 'timestamp' | 'type' | 'message' | 'title'>>) => {
    return addNotification({
      type: 'warning',
      message,
      title,
      ...options,
    })
  }

  const info = (message: string, title?: string, options?: Partial<Omit<Notification, 'id' | 'timestamp' | 'type' | 'message' | 'title'>>) => {
    return addNotification({
      type: 'info',
      message,
      title,
      ...options,
    })
  }

  return {
    // State
    notifications,

    // Actions
    addNotification,
    removeNotification,
    clearNotifications,

    // Convenience methods
    success,
    error,
    warning,
    info,
  }
})