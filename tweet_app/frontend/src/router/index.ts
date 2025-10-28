import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Import components
import Dashboard from '@/views/Dashboard.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import Datasets from '@/views/datasets/Datasets.vue'
import DatasetDetail from '@/views/datasets/DatasetDetail.vue'
import DatasetUpload from '@/views/datasets/DatasetUpload.vue'
import Search from '@/views/search/Search.vue'
import Analytics from '@/views/analytics/Analytics.vue'
import Profile from '@/views/profile/Profile.vue'
import NotFound from '@/views/NotFound.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true,
      title: 'Dashboard'
    }
  },
  {
    path: '/auth',
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: {
          requiresGuest: true,
          title: 'Login'
        }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: {
          requiresGuest: true,
          title: 'Register'
        }
      }
    ]
  },
  {
    path: '/datasets',
    name: 'Datasets',
    component: Datasets,
    meta: {
      requiresAuth: true,
      title: 'Datasets'
    }
  },
  {
    path: '/datasets/upload',
    name: 'DatasetUpload',
    component: DatasetUpload,
    meta: {
      requiresAuth: true,
      title: 'Upload Dataset'
    }
  },
  {
    path: '/datasets/:id',
    name: 'DatasetDetail',
    component: DatasetDetail,
    props: true,
    meta: {
      requiresAuth: true,
      title: 'Dataset Details'
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: Search,
    meta: {
      requiresAuth: true,
      title: 'Search'
    }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics,
    meta: {
      requiresAuth: true,
      title: 'Analytics'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true,
      title: 'Profile'
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: 'Page Not Found'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Update page title
  if (to.meta.title) {
    document.title = `${to.meta.title} - TweetEval NLP Platform`
  }

  // Check authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router