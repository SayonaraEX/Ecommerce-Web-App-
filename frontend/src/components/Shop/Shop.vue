//components/Shop/Shop.vue
<script setup lang="ts">
import { ref, defineAsyncComponent } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const Account = defineAsyncComponent(() => import('../Account/Account.vue'));

const authStore = useAuthStore();
const showAccountModal = ref<boolean>(false);

const openAccountModal = () => {
  if (authStore.isAuthenticated) {
    showAccountModal.value = true;
  }
};

const closeAccountModal = () => {
  showAccountModal.value = false;
};

const handleLogoutComplete = () => {
  closeAccountModal(); 
};
</script>

<template>
  <div class="container">

    <main>
      <h1 id="h1">Shop Page</h1>
      
      <div>
        <RouterLink v-if="!authStore.isAuthenticated" to="/auth">Sign up</RouterLink>
        <button v-else @click="openAccountModal">Account</button>
      </div>
    </main>

    <div v-if="showAccountModal" class="modal-overlay">
      <div class="modal-content">
        <button @click="closeAccountModal" class="close-button">
          &times;
        </button>
        <h2>Account Details</h2>
        <div>
          <Account @logout-complete="handleLogoutComplete" />
        </div>
      </div>
    </div>
  </div>
</template>


<style lang="scss">
.container{
  background-color: rgb(16, 151, 151);
  height: 100vh;
}
#h1{
  margin: 0; 
  padding: 0;
}
.modal-overlay{
  background-color: #5fc68c;
}
</style>
