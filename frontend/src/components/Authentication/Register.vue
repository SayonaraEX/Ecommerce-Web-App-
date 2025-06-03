//Components/Authentication/Register.vue
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref<string>('');
const email = ref<string>('');
const password = ref<string>('');
const password_confirm = ref<string>('');
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);

const register = async () => {
  errorMessage.value = null;
  successMessage.value = null;

  if (password.value !== password_confirm.value) {
    errorMessage.value = 'Passwords do not match.';
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/v1/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        first_name: '',
        last_name: '',
        address: '',
        city: '',
        state: '',
        zip_code: '',
        country: '',
        phone_number: '',
        role: 'customer', // CHANGED: Set role to 'customer' as required by backend
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      if (Array.isArray(errorData.detail)) {
        const detailedErrors = errorData.detail.map((err: any) => {
          return `${err.loc[1] || 'Field'}: ${err.msg}`;
        }).join('; ');
        throw new Error(`Registration failed: ${detailedErrors}`);
      } else {
        throw new Error(errorData.detail || 'Registration failed: Unknown error.');
      }
    }

    const data = await response.json();
    successMessage.value = 'Registration successful! You can now log in.';
    username.value = '';
    email.value = '';
    password.value = '';
    password_confirm.value = '';
  } catch (error: any) {
    console.error('Registration error:', error);
    errorMessage.value = error.message || 'An unexpected error occurred during registration.';
  }
};
</script>

<template>
  <div class="register-container">
    <form @submit.prevent="register">
      <h2 id="h1">Register</h2>
      <div class="input-box">
        <input v-model="username" type="text" placeholder="Username" required />
      </div>
      <div class="input-box">
        <input v-model="email" type="email" placeholder="Email" required />
      </div>
      <div class="input-box">
        <input v-model="password" type="password" placeholder="Password" required />
      </div>
      <div class="input-box">
        <input v-model="password_confirm" type="password" placeholder="Confirm Password" required />
      </div>
      <button type="submit">Register</button>
      <p v-if="errorMessage">{{ errorMessage }}</p>
      <p v-if="successMessage">{{ successMessage }}</p>
    </form>
  </div>
</template>

<style scoped lang="scss">
.register-container{
  background-color: #93b824;
}
#h1{
  margin: 0; 
  padding: 0;
}
</style>