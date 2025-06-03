//components/Account/Account.vue
<script setup lang="ts">
import { ref, defineEmits } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const showConfirmLogout = ref<boolean>(false); // Reactive state for confirmation pop-up

// Define emits for communicating with the parent component (Shop.vue)
const emit = defineEmits(['logout-complete']);

const initiateLogout = () => {
  showConfirmLogout.value = true; // Show the confirmation pop-up
};

const confirmLogout = () => {
  authStore.clearAuth(); // Perform the actual logout
  showConfirmLogout.value = false; // Hide the confirmation pop-up
  emit('logout-complete'); // Emit event to parent to close modal
};

const cancelLogout = () => {
  showConfirmLogout.value = false; // Hide the confirmation pop-up
};
</script>

<template>
  <div class="account-details-container">
    <h3>Your Profile Information</h3>
    <div v-if="authStore.user">
      <div class="info-item">
        <span>Username:</span> {{ authStore.user.username }}
      </div>
      <div class="info-item">
        <span>Email:</span> {{ authStore.user.email }}
      </div>
      <div class="info-item">
        <span>Role:</span> {{ authStore.user.role }}
      </div>
      <div class="info-item">
        <span>First Name:</span> {{ authStore.user.first_name || 'N/A' }}
      </div>
      <div class="info-item">
        <span>Last Name:</span> {{ authStore.user.last_name || 'N/A' }}
      </div>
      <div class="info-item">
        <span>Address:</span> {{ authStore.user.address || 'N/A' }}, {{ authStore.user.city || 'N/A' }}, {{ authStore.user.state || 'N/A' }} {{ authStore.user.zip_code || 'N/A' }}, {{ authStore.user.country || 'N/A' }}
      </div>
      <div class="info-item">
        <span>Phone:</span> {{ authStore.user.phone_number || 'N/A' }}
      </div>

      <div>
        <button @click="initiateLogout">Logout</button>
      </div>
    </div>
    <div v-else>
      <p>User information not available. Please log in.</p>
    </div>

    <div v-if="showConfirmLogout" class="confirmation-overlay">
      <div class="confirmation-content">
        <p>Are you sure you want to log out?</p>
        <div>
          <button @click="confirmLogout">Yes</button>
          <button @click="cancelLogout">No</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>