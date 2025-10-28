import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import Dashboard from '@/views/Dashboard.vue'
import { useAuthStore } from '@/stores/auth'

// Mock the auth store
vi.mock('@/stores/auth', () => ({
  useAuthStore: vi.fn()
}))

// Mock the router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/dashboard', component: Dashboard },
    { path: '/login', name: 'login', component: { template: '<div>Login</div>' } }
  ]
})

describe('Dashboard View', () => {
  let mockAuthStore: any

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()

    mockAuthStore = {
      user: {
        id: '123',
        username: 'testuser',
        email: 'test@example.com',
        full_name: 'Test User'
      },
      isAuthenticated: true,
      loading: false,
      error: null
    }

    vi.mocked(useAuthStore).mockReturnValue(mockAuthStore)
  })

  describe('Authentication Guard', () => {
    it('should show loading state while checking authentication', () => {
      mockAuthStore.loading = true

      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.find('.loading-spinner').exists()).toBe(true)
      expect(wrapper.text()).toContain('Loading...')
    })

    it('should redirect to login if not authenticated', async () => {
      mockAuthStore.isAuthenticated = false

      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      await wrapper.vm.$nextTick()

      // Should show redirect message or handle it in navigation guard
      expect(wrapper.text()).toContain('Redirecting to login...')
    })

    it('should render dashboard if authenticated', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.find('.dashboard-container').exists()).toBe(true)
      expect(wrapper.text()).toContain('Welcome back')
    })
  })

  describe('User Information Display', () => {
    it('should display user information correctly', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.text()).toContain('Test User')
      expect(wrapper.text()).toContain('test@example.com')
    })

    it('should handle missing user information gracefully', () => {
      mockAuthStore.user = {
        id: '123',
        username: 'testuser',
        email: 'test@example.com',
        full_name: null
      }

      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.text()).toContain('testuser')
      expect(wrapper.text()).toContain('test@example.com')
    })
  })

  describe('Dashboard Layout', () => {
    it('should have proper navigation elements', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.find('.dashboard-header').exists()).toBe(true)
      expect(wrapper.find('.dashboard-sidebar').exists()).toBe(true)
      expect(wrapper.find('.dashboard-content').exists()).toBe(true)
    })

    it('should have navigation links', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      const navLinks = wrapper.findAll('.nav-link')
      expect(navLinks.length).toBeGreaterThan(0)

      // Check for common navigation items
      const linkTexts = navLinks.map(link => link.text())
      expect(linkTexts.some(text => text.includes('Datasets'))).toBe(true)
      expect(linkTexts.some(text => text.includes('Search'))).toBe(true)
      expect(linkTexts.some(text => text.includes('Analytics'))).toBe(true)
    })
  })

  describe('Dashboard Stats', () => {
    it('should display dashboard statistics', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.find('.stats-container').exists()).toBe(true)

      // Look for stat cards
      const statCards = wrapper.findAll('.stat-card')
      expect(statCards.length).toBeGreaterThan(0)
    })

    it('should handle loading stats', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      // Initially might show loading state for stats
      await wrapper.vm.loadDashboardStats()

      expect(wrapper.vm.loadingStats).toBe(false)
    })
  })

  describe('Recent Activity', () => {
    it('should display recent activity section', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.find('.recent-activity').exists()).toBe(true)
    })

    it('should handle empty activity list', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      // Mock empty activity
      wrapper.vm.recentActivity = []

      expect(wrapper.text()).toContain('No recent activity')
    })

    it('should display activity items', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      // Mock activity data
      const mockActivity = [
        {
          id: '1',
          type: 'dataset_upload',
          description: 'Uploaded new dataset',
          timestamp: new Date().toISOString()
        },
        {
          id: '2',
          type: 'search',
          description: 'Searched for "happy tweets"',
          timestamp: new Date().toISOString()
        }
      ]

      wrapper.vm.recentActivity = mockActivity
      await wrapper.vm.$nextTick()

      const activityItems = wrapper.findAll('.activity-item')
      expect(activityItems.length).toBe(2)
    })
  })

  describe('Error Handling', () => {
    it('should display error message when present', () => {
      mockAuthStore.error = 'Failed to load dashboard'

      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      expect(wrapper.text()).toContain('Failed to load dashboard')
    })

    it('should handle network errors gracefully', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      // Simulate error in loading dashboard data
      await wrapper.vm.loadDashboardStats().catch(() => {})

      expect(wrapper.vm.error).toBeTruthy()
    })
  })

  describe('Responsive Design', () => {
    it('should have responsive classes', () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      const container = wrapper.find('.dashboard-container')
      expect(container.classes()).toContain('responsive-container')
    })
  })

  describe('Navigation Actions', () => {
    it('should handle logout action', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      const logoutButton = wrapper.find('.logout-button')
      if (logoutButton.exists()) {
        await logoutButton.trigger('click')
        expect(mockAuthStore.logout).toHaveBeenCalled()
      }
    })

    it('should navigate to different sections', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [router]
        }
      })

      const datasetsLink = wrapper.find('[data-testid="datasets-link"]')
      if (datasetsLink.exists()) {
        await datasetsLink.trigger('click')
        // Check if navigation occurred
        expect(router.currentRoute.value.path).toBe('/datasets')
      }
    })
  })
})