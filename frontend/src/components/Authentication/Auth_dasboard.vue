//components/Authentication/Auth_dasboard.vue
<script setup lang="ts">
import { ref, markRaw } from 'vue';
import Login from './Login.vue';
import Register from './Register.vue';

const currentView = ref(markRaw(Login));

const showLogin = () => {
  currentView.value = markRaw(Login);
};

const showRegister = () => {
  currentView.value = markRaw(Register);
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-tabs">
      <button
        @click="showLogin"
        :class="{ 'active-tab': currentView.__name === 'Login' }"
        class="tab-button"
      >
        Login
      </button>
      <button
        @click="showRegister"
        :class="{ 'active-tab': currentView.__name === 'Register' }"
        class="tab-button"
      >
        Register
      </button>
    </div>

    <div class="auth-form-area">
      <component :is="currentView" />
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>
