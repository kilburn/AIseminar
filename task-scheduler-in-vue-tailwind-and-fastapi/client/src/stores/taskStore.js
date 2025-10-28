import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { taskApi } from '@/api/tasks'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref([])
  const totalCount = ref(0)
  const totalPages = ref(0)
  const loading = ref(false)
  const error = ref(null)

  const filters = ref({
    search: '',
    status: [],
    priority: [],
    tags: [],
    dueDateFrom: '',
    dueDateTo: '',
    overdueOnly: false,
    completedOnly: false,
    sortBy: 'createdDate',
    sortOrder: 'desc',
    page: 1,
    pageSize: 20
  })

  const hasActiveFilters = computed(() => {
    const { search, status, priority, tags, dueDateFrom, dueDateTo, ...rest } = filters.value
    return (
      search !== '' ||
      status.length > 0 ||
      priority.length > 0 ||
      tags.length > 0 ||
      dueDateFrom !== '' ||
      dueDateTo !== '' ||
      Object.values(rest).some(value => value !== false)
    )
  })

  const activeFilterCount = computed(() => {
    let count = 0
    if (filters.value.search) count++
    if (filters.value.status.length > 0) count++
    if (filters.value.priority.length > 0) count++
    if (filters.value.tags.length > 0) count++
    if (filters.value.dueDateFrom) count++
    if (filters.value.dueDateTo) count++
    if (filters.value.overdueOnly) count++
    if (filters.value.completedOnly) count++
    return count
  })

  const fetchTasks = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await taskApi.getTasks(filters.value)
      tasks.value = response.tasks
      totalCount.value = response.totalCount
      totalPages.value = response.totalPages
    } catch (err) {
      error.value = err.message || 'Failed to fetch tasks'
      console.error('Error fetching tasks:', err)
    } finally {
      loading.value = false
    }
  }

  const getFilterOptions = async () => {
    try {
      return await taskApi.getFilterOptions()
    } catch (error) {
      console.error('Failed to get filter options:', error)
      throw error
    }
  }

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters, page: 1 }
    fetchTasks()
  }

  const setFilter = (key, value) => {
    filters.value[key] = value
    filters.value.page = 1
    fetchTasks()
  }

  const setPage = (page) => {
    filters.value.page = page
    fetchTasks()
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      status: [],
      priority: [],
      tags: [],
      dueDateFrom: '',
      dueDateTo: '',
      overdueOnly: false,
      completedOnly: false,
      sortBy: 'createdDate',
      sortOrder: 'desc',
      page: 1,
      pageSize: 20
    }
    fetchTasks()
  }

  return {
    tasks,
    totalCount,
    totalPages,
    loading,
    error,
    filters,
    hasActiveFilters,
    activeFilterCount,
    fetchTasks,
    getFilterOptions,
    updateFilters,
    setFilter,
    setPage,
    resetFilters
  }
})