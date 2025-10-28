<template>
  <div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <!-- Search Bar -->
    <div class="mb-4">
      <input
        v-model="filters.search"
        @input="debouncedApplyFilters"
        type="text"
        placeholder="Search tasks..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Active Filters -->
    <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 mb-4">
      <span
        v-for="filter in activeFilters"
        :key="filter.key"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
      >
        {{ filter.label }}
        <button @click="removeFilter(filter.key)" class="ml-2 hover:text-blue-600">
          ×
        </button>
      </span>
      <button @click="resetFilters" class="text-sm text-gray-500 hover:text-gray-700">
        Clear all
      </button>
    </div>

    <!-- Filter Controls -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Status Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
        <select
          v-model="filters.status"
          @change="applyFilters"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option v-for="option in filterOptions.statuses" :key="option.value" :value="option.value">
            {{ option.label }} ({{ option.count }})
          </option>
        </select>
      </div>

      <!-- Priority Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
        <select
          v-model="filters.priority"
          @change="applyFilters"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option v-for="option in filterOptions.priorities" :key="option.value" :value="option.value">
            {{ option.label }} ({{ option.count }})
          </option>
        </select>
      </div>

      <!-- Date Range Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Due Date Range</label>
        <input
          v-model="filters.dueDateFrom"
          @change="applyFilters"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md mb-2"
          placeholder="From"
        />
        <input
          v-model="filters.dueDateTo"
          @change="applyFilters"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
          placeholder="To"
        />
      </div>

      <!-- Tags Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
        <select
          v-model="filters.tags"
          @change="applyFilters"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option v-for="option in filterOptions.tags" :key="option.value" :value="option.value">
            {{ option.label }} ({{ option.count }})
          </option>
        </select>
      </div>
    </div>

    <!-- Quick Filters -->
    <div class="flex gap-2 mt-4">
      <button
        v-for="quickFilter in quickFilters"
        :key="quickFilter.key"
        @click="applyQuickFilter(quickFilter)"
        :class="[
          'px-4 py-2 rounded-md text-sm font-medium transition-colors',
          isQuickFilterActive(quickFilter)
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        {{ quickFilter.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { debounce } from 'lodash-es'
import { useTaskStore } from '@/stores/taskStore'

const taskStore = useTaskStore()

const filters = ref({
  search: '',
  status: [],
  priority: [],
  tags: [],
  dueDateFrom: '',
  dueDateTo: '',
  overdueOnly: false,
  completedOnly: false
})

const filterOptions = ref({
  statuses: [],
  priorities: [],
  tags: []
})

const quickFilters = [
  { key: 'overdue', label: 'Overdue', filter: { overdueOnly: true } },
  { key: 'completed', label: 'Completed', filter: { completedOnly: true },
  { key: 'today', label: 'Due Today', filter: { dueDateFrom: new Date().toISOString().split('T')[0] } }
]

const hasActiveFilters = computed(() => {
  return Object.values(filters.value).some(value =>
    value !== '' && value !== null && value !== false &&
    (Array.isArray(value) ? value.length > 0 : true)
  )
})

const activeFilters = computed(() => {
  const active = []
  // Build active filters display logic here
  return active
})

const debouncedApplyFilters = debounce(() => {
  applyFilters()
}, 300)

const applyFilters = () => {
  taskStore.updateFilters(filters.value)
}

const removeFilter = (key) => {
  if (Array.isArray(filters.value[key])) {
    filters.value[key] = []
  } else {
    filters.value[key] = ''
  }
  applyFilters()
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
    completedOnly: false
  }
  applyFilters()
}

const applyQuickFilter = (quickFilter) => {
  Object.assign(filters.value, quickFilter.filter)
  applyFilters()
}

const isQuickFilterActive = (quickFilter) => {
  return Object.entries(quickFilter.filter).every(([key, value]) =>
    filters.value[key] === value
  )
}

onMounted(async () => {
  // Load filter options
  try {
    const options = await taskStore.getFilterOptions()
    filterOptions.value = options
  } catch (error) {
    console.error('Failed to load filter options:', error)
  }
})
</script>