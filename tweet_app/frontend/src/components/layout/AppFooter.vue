<template>
  <footer class="bg-white border-t border-gray-200 mt-auto">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Company Info -->
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">T</span>
            </div>
            <span class="ml-2 text-xl font-semibold text-gray-900">TweetEval</span>
          </div>
          <p class="mt-2 text-sm text-gray-600">
            A comprehensive platform for tweet dataset analysis using state-of-the-art NLP models.
            Perform sentiment analysis, emotion classification, and semantic search on your Twitter data.
          </p>
        </div>

        <!-- Product Links -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
            Product
          </h3>
          <ul class="space-y-3">
            <li>
              <RouterLink to="/datasets" class="text-sm text-gray-600 hover:text-primary-600">
                Dataset Management
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/search" class="text-sm text-gray-600 hover:text-primary-600">
                Semantic Search
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/analytics" class="text-sm text-gray-600 hover:text-primary-600">
                Analytics Dashboard
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Resources -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 tracking-wider uppercase mb-4">
            Resources
          </h3>
          <ul class="space-y-3">
            <li>
              <a href="/docs" target="_blank" class="text-sm text-gray-600 hover:text-primary-600">
                API Documentation
              </a>
            </li>
            <li>
              <a href="https://github.com/cardiffnlp/tweeteval" target="_blank" class="text-sm text-gray-600 hover:text-primary-600">
                TweetEval Models
              </a>
            </li>
            <li>
              <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
                Support
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t border-gray-200">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-sm text-gray-600">
            &copy; {{ new Date().getFullYear() }} TweetEval NLP Platform. All rights reserved.
          </p>
          <div class="mt-4 md:mt-0 flex space-x-6">
            <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
              Privacy Policy
            </a>
            <a href="#" class="text-sm text-gray-600 hover:text-primary-600">
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component
</script>