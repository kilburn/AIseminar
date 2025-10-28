<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
        <p class="mt-2 text-sm text-gray-700">
          Welcome back, {{ authStore.user?.full_name || authStore.user?.username }}!
          Here's an overview of your tweet analysis projects.
        </p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div
          v-for="stat in stats"
          :key="stat.name"
          class="card p-6 hover-lift"
        >
          <div class="flex items-center">
            <div :class="stat.iconClasses" class="p-3 rounded-lg">
              <component :is="stat.icon" class="w-6 h-6" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ stat.name }}</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stat.value }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Datasets -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-medium text-gray-900">Recent Datasets</h2>
              <RouterLink to="/datasets" class="text-sm text-primary-600 hover:text-primary-500">
                View all
              </RouterLink>
            </div>
            <div class="card-body">
              <div v-if="loading" class="flex justify-center py-8">
                <div class="loading-spinner"></div>
              </div>
              <div v-else-if="recentDatasets.length === 0" class="text-center py-8">
                <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <svg class="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p class="text-gray-600 mb-4">No datasets yet</p>
                <RouterLink to="/datasets/upload" class="btn-primary">
                  Upload your first dataset
                </RouterLink>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="dataset in recentDatasets"
                  :key="dataset.id"
                  class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                      <svg class="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div class="ml-4">
                      <h3 class="text-sm font-medium text-gray-900">{{ dataset.name }}</h3>
                      <p class="text-sm text-gray-600">{{ dataset.total_rows }} tweets</p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span :class="getStatusClasses(dataset.processing_status)" class="badge">
                      {{ dataset.processing_status }}
                    </span>
                    <RouterLink
                      :to="`/datasets/${dataset.id}`"
                      class="text-primary-600 hover:text-primary-500"
                    >
                      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="lg:col-span-1">
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-medium text-gray-900">Quick Actions</h2>
            </div>
            <div class="card-body">
              <div class="space-y-4">
                <RouterLink
                  to="/datasets/upload"
                  class="block w-full text-center btn-primary"
                >
                  <svg class="w-5 h-5 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  Upload Dataset
                </RouterLink>
                <RouterLink
                  to="/search"
                  class="block w-full text-center btn-outline"
                >
                  <svg class="w-5 h-5 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Search Tweets
                </RouterLink>
                <RouterLink
                  to="/analytics"
                  class="block w-full text-center btn-outline"
                >
                  <svg class="w-5 h-5 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  View Analytics
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { Dataset, ProcessingStatus } from '@/types'

// Icons
const DocumentIcon = () => (
  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
)

const SearchIcon = () => (
  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
)

const ChartIcon = () => (
  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
  </svg>
)

const authStore = useAuthStore()

// Mock data - will be replaced with API calls
const loading = ref(false)
const recentDatasets = ref<Dataset[]>([])

const stats = ref([
  {
    name: 'Total Datasets',
    value: '0',
    icon: DocumentIcon,
    iconClasses: 'bg-blue-100 text-blue-600'
  },
  {
    name: 'Tweets Analyzed',
    value: '0',
    icon: SearchIcon,
    iconClasses: 'bg-green-100 text-green-600'
  },
  {
    name: 'Search Queries',
    value: '0',
    icon: ChartIcon,
    iconClasses: 'bg-purple-100 text-purple-600'
  },
  {
    name: 'Active Projects',
    value: '0',
    icon: DocumentIcon,
    iconClasses: 'bg-yellow-100 text-yellow-600'
  }
])

const getStatusClasses = (status: ProcessingStatus) => {
  switch (status) {
    case 'completed':
      return 'badge-success'
    case 'processing':
      return 'badge-warning'
    case 'failed':
      return 'badge-error'
    default:
      return 'badge-info'
  }
}

onMounted(async () => {
  // TODO: Load real data from API
  // This will be implemented in later phases
  loading.value = true
  try {
    // const response = await datasetsApi.getRecentDatasets()
    // recentDatasets.value = response.items
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loading.value = false
  }
})
</script>