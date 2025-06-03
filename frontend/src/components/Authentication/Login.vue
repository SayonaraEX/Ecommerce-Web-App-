//Components/Authentication/Login.vue
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const router = useRouter();

const loginInput = ref<string>('');
const password = ref<string>('');
const errorMessage = ref<string | null>(null);

const login = async () => {
  errorMessage.value = null;
  try {
    const formData = new URLSearchParams();
    formData.append('username', loginInput.value);
    formData.append('password', password.value);

    const response = await fetch('http://localhost:8000/api/v1/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', 
      },
      body: formData.toString(), 
    });

    if (!response.ok) {
      const errorData = await response.json();

      if (Array.isArray(errorData.detail)) {
        const detailedErrors = errorData.detail.map((err: any) => {
          return `${err.loc[1] || 'Field'}: ${err.msg}`;
        }).join('; ');
        throw new Error(`Login failed: ${detailedErrors}`);
      } else {
        throw new Error(errorData.detail || 'Login failed: Unknown error.');
      }
    }

    const data = await response.json();
    authStore.setUser(data.user, data.access_token); 
    router.push('/');
  } catch (error: any) {
    console.error('Login error:', error);
    errorMessage.value = error.message || 'An unexpected error occurred during login.';
  }
};
</script>

<template>
  <div class="login-container">
    <form @submit.prevent="login">
      <h2 id = "h1">Login</h2>
      <div class="input-box">
        <input v-model="loginInput" type="text" placeholder="Username or email" required />
      </div>
      <div class="input-box">
        <input v-model="password" type="password" placeholder="Password" required />
      </div>
      <button type="submit">Login</button>
      <p v-if="errorMessage">{{ errorMessage }}</p>
    </form>
  </div>
</template>


<style scoped lang="scss">
.login-container{
  background-color: #93b824;
}
#h1{
  margin: 0; 
  padding: 0;
}
</style>