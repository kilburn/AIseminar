import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Import styles
import './style.css'

// Create Vue app
const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(router)

// Global error handler
app.config.errorHandler = (error, vm, info) => {
  console.error('Global error:', error)
  console.error('Component:', vm)
  console.error('Info:', info)
}

// Mount app
app.mount('#app')