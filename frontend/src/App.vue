// App.vue
<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app" class="display"> <RouterView />
  </div>
</template>

<style> 
*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%; 
  width: 100%;  
  overflow: hidden; 
}

#app {
  margin: 0;
  padding: 0;
  height: 100vh; 
  width: 100vw;  
  overflow: hidden;
}
</style>

