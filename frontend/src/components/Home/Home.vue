<script setup lang="ts">
import { RouterLink } from 'vue-router'; // Import RouterLink for navigation
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-100 text-gray-800 p-4 border border-blue-300 rounded-lg">

    <header class="w-full h-16 flex items-center justify-between p-4 bg-white shadow-md mb-4 rounded-lg border border-gray-300">
      <div class="text-lg font-bold border border-gray-200 p-1 rounded-md">
        E-commerce App
      </div>
      <nav class="flex space-x-4 border border-gray-200 p-1 rounded-md">
        <RouterLink to="/" class="p-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">Home</RouterLink>
        <RouterLink to="/products" class="p-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">Products</RouterLink>
        <RouterLink to="/auth" class="p-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">Login/Register</RouterLink>
        <RouterLink to="/cart" class="p-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">Cart</RouterLink>
      </nav>
    </header>

    <main class="flex-grow w-full p-6 bg-white shadow-md mb-4 rounded-lg border border-gray-300">
      <div class="p-4 border border-gray-200 rounded-md mb-4">
        <p class="text-lg font-medium">This is home page</p>
        <RouterLink to="/auth">
          <button class="mt-4 p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors">Go to Login and register</button>
        </RouterLink>
      </div>

      <div class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 border border-gray-300 p-4 rounded-lg">
        <div class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
          <div class="h-32 w-full bg-gray-200 rounded-md mb-2 border border-gray-300"></div>
          <h3 class="font-medium">Product Title 1</h3>
          <p class="text-sm text-gray-500">Price: $X.XX</p>
        </div>
        <div class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
          <div class="h-32 w-full bg-gray-200 rounded-md mb-2 border border-gray-300"></div>
          <h3 class="font-medium">Product Title 2</h3>
          <p class="text-sm text-gray-500">Price: $Y.YY</p>
        </div>
        <div class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
          <div class="h-32 w-full bg-gray-200 rounded-md mb-2 border border-gray-300"></div>
          <h3 class="font-medium">Product Title 3</h3>
          <p class="text-sm text-gray-500">Price: $Z.ZZ</p>
        </div>
      </div>
    </main>

    <footer class="w-full h-12 flex items-center justify-center p-4 bg-white shadow-md rounded-lg border border-gray-300">
      <p class="text-sm text-gray-600">
        &copy; 2025 E-commerce App. All rights reserved.
      </p>
    </footer>
  </div>
</template>

<style scoped lang="scss">
/* No specific SCSS needed for this structural layout if using Tailwind */
/* The .display class and its styles are no longer needed here as the root div handles it */
</style>
