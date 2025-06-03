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
    <div class="auth-form-area">
      <div class="auth-tabs">
      <button @click="showLogin":class="{ 'active-tab': currentView.__name === 'Login' }"class="tab-button">
        Login
      </button>
      <button @click="showRegister":class="{ 'active-tab': currentView.__name === 'Register' }"class="tab-button">
        Register
      </button>
      </div>
      <component class="current-view" :is="currentView" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.auth-container {
  background-color: #3498db;
  height: 100vh;
  width: 100%;
  display: flex; 
  justify-content: center; 
  align-items: center; 
  overflow: hidden;
  margin: 0;
  padding: 0;
}
.auth-form-area {
  width: 700px;
  height: 300px;
  border: 4px solid #5fc68c; 
  margin: 0;
  padding: 0;

}
.auth-tabs {
  display: flex;
  justify-content: center;
  gap: 10px; 
  height: 15%;
  button { 
    padding: 10px 20px;
    border: 1px solid #ccc;
    background-color: #f0f0f0;
    cursor: pointer;
  }

}
.current-view{
  height: 85%;
}

</style>
