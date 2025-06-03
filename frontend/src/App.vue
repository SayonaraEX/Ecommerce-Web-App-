// App.vue
<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
<div class="display">
  <RouterView />
</div>
</template>

<style scoped>
.display {
  overflow: hidden;
  height: 100%;
  width: 100%;
}

</style>