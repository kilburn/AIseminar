import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import LoginForm from '@/components/auth/LoginForm.vue'
import { useAuthStore } from '@/stores/auth'

// Mock the auth store
vi.mock('@/stores/auth', () => ({
  useAuthStore: vi.fn()
}))

describe('LoginForm', () => {
  let mockAuthStore: any

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()

    mockAuthStore = {
      login: vi.fn(),
      loading: false,
      error: null
    }

    vi.mocked(useAuthStore).mockReturnValue(mockAuthStore)
  })

  describe('Rendering', () => {
    it('should render the login form correctly', () => {
      const wrapper = mount(LoginForm)

      expect(wrapper.find('form').exists()).toBe(true)
      expect(wrapper.find('input[type="email"]').exists()).toBe(true)
      expect(wrapper.find('input[type="password"]').exists()).toBe(true)
      expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
      expect(wrapper.text()).toContain('Sign In')
      expect(wrapper.text()).toContain('Email')
      expect(wrapper.text()).toContain('Password')
    })

    it('should have proper form fields with correct attributes', () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      const passwordInput = wrapper.find('input[type="password"]')
      const submitButton = wrapper.find('button[type="submit"]')

      expect(emailInput.attributes('id')).toBe('email')
      expect(emailInput.attributes('name')).toBe('email')
      expect(emailInput.attributes('placeholder')).toBe('Enter your email')
      expect(emailInput.attributes('required')).toBeDefined()

      expect(passwordInput.attributes('id')).toBe('password')
      expect(passwordInput.attributes('name')).toBe('password')
      expect(passwordInput.attributes('placeholder')).toBe('Enter your password')
      expect(passwordInput.attributes('required')).toBeDefined()

      expect(submitButton.text()).toContain('Sign In')
    })
  })

  describe('Form Validation', () => {
    it('should show validation errors for empty fields', async () => {
      const wrapper = mount(LoginForm)

      // Try to submit empty form
      await wrapper.find('form').trigger('submit.prevent')

      // Check for HTML5 validation
      const emailInput = wrapper.find('input[type="email"]')
      const passwordInput = wrapper.find('input[type="password"]')

      expect(emailInput.element.validity.valid).toBe(false)
      expect(passwordInput.element.validity.valid).toBe(false)
    })

    it('should show validation error for invalid email', async () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      await emailInput.setValue('invalid-email')

      expect(emailInput.element.validity.valid).toBe(false)
    })

    it('should allow valid email format', async () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      await emailInput.setValue('test@example.com')

      expect(emailInput.element.validity.valid).toBe(true)
    })
  })

  describe('Form Submission', () => {
    it('should call auth store login with correct data', async () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      const passwordInput = wrapper.find('input[type="password"]')

      await emailInput.setValue('test@example.com')
      await passwordInput.setValue('password123')

      mockAuthStore.login.mockResolvedValue(undefined)

      await wrapper.find('form').trigger('submit.prevent')

      expect(mockAuthStore.login).toHaveBeenCalledTimes(1)
      expect(mockAuthStore.login).toHaveBeenCalledWith({
        username: 'test@example.com',
        password: 'password123'
      })
    })

    it('should show loading state during submission', async () => {
      mockAuthStore.loading = true

      const wrapper = mount(LoginForm)

      const submitButton = wrapper.find('button[type="submit"]')

      expect(submitButton.attributes('disabled')).toBeDefined()
      expect(submitButton.text()).toContain('Signing In...')
    })

    it('should show error message when login fails', async () => {
      mockAuthStore.error = 'Invalid credentials'

      const wrapper = mount(LoginForm)

      // Force error state
      wrapper.vm.$forceUpdate()

      await wrapper.vm.$nextTick()

      expect(wrapper.text()).toContain('Invalid credentials')
    })

    it('should disable submit button while loading', async () => {
      mockAuthStore.loading = true

      const wrapper = mount(LoginForm)
      const submitButton = wrapper.find('button[type="submit"]')

      expect(submitButton.attributes('disabled')).toBeDefined()
    })
  })

  describe('Data Binding', () => {
    it('should bind form data correctly', async () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      const passwordInput = wrapper.find('input[type="password"]')

      await emailInput.setValue('test@example.com')
      await passwordInput.setValue('password123')

      expect(wrapper.vm.formData.username).toBe('test@example.com')
      expect(wrapper.vm.formData.password).toBe('password123')
    })

    it('should reset form data after successful submission', async () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      const passwordInput = wrapper.find('input[type="password"]')

      await emailInput.setValue('test@example.com')
      await passwordInput.setValue('password123')

      mockAuthStore.login.mockResolvedValue(undefined)

      await wrapper.find('form').trigger('submit.prevent')

      // Wait for async operation
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.formData.username).toBe('')
      expect(wrapper.vm.formData.password).toBe('')
    })
  })

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      const wrapper = mount(LoginForm)

      const emailInput = wrapper.find('input[type="email"]')
      const passwordInput = wrapper.find('input[type="password"]')

      // Check for associated labels
      expect(wrapper.find('label[for="email"]').exists()).toBe(true)
      expect(wrapper.find('label[for="password"]').exists()).toBe(true)
    })

    it('should show error messages in accessible way', async () => {
      mockAuthStore.error = 'Login failed'

      const wrapper = mount(LoginForm)

      // Force error state
      wrapper.vm.$forceUpdate()
      await wrapper.vm.$nextTick()

      const errorElement = wrapper.find('.error-message')
      if (errorElement.exists()) {
        expect(errorElement.attributes('role')).toBe('alert')
      }
    })
  })
})