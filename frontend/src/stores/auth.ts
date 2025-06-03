// frontend/src/stores/auth.ts
// frontend/src/stores/auth.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

// Define the structure of a User object (matching your backend schema)
interface User {
  user_id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  phone_number?: string;
  role: string;
}

export const useAuthStore = defineStore('auth', () => {
  // Reactive state variables
  const isAuthenticated = ref<boolean>(false); // Tracks if a user is logged in
  const user = ref<User | null>(null); // Stores the logged-in user's data
  const token = ref<string | null>(null); // Stores the authentication token (e.g., JWT)

  // Function to set user data and authentication status upon login
  const setUser = (userData: User, userToken: string) => { // userToken is now expected to be a string (JWT)
    user.value = userData;
    token.value = userToken;
    isAuthenticated.value = true;
    // Persist token and user data to localStorage
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', userToken);
  };

  // Function to clear user data and authentication status upon logout
  const clearAuth = () => {
    user.value = null;
    token.value = null;
    isAuthenticated.value = false;
    // Clear data from localStorage
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  // Initialize auth state from localStorage on store creation
  // This helps maintain login state across page refreshes
  const initializeAuth = () => {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');
    if (storedUser && storedToken) { // Both user and token must be present for authenticated state
      try {
        user.value = JSON.parse(storedUser);
        token.value = storedToken;
        isAuthenticated.value = true;
      } catch (e) {
        console.error("Failed to parse stored user data or token:", e);
        clearAuth(); // Clear corrupted data
      }
    }
  };

  // Call initialization when the store is created
  initializeAuth();

  // Expose state and actions
  return {
    isAuthenticated,
    user,
    token,
    setUser,
    clearAuth,
    initializeAuth
  };
});
