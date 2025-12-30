import type { User } from 'firebase/auth'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export type AuthState = 'UNAUTHENTICATED' | 'INITIALIZING' | 'READY'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const state = ref<AuthState>('UNAUTHENTICATED')
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => state.value === 'READY' && user.value !== null)
  const isLoading = computed(() => state.value === 'INITIALIZING')
  const displayName = computed(() => user.value?.displayName ?? 'Anonymous')
  const uid = computed(() => user.value?.uid ?? null)

  // Actions
  function setUser(newUser: User | null) {
    user.value = newUser
    state.value = newUser ? 'READY' : 'UNAUTHENTICATED'
    error.value = null
  }

  function setInitializing() {
    state.value = 'INITIALIZING'
  }

  function setError(message: string) {
    error.value = message
    state.value = 'UNAUTHENTICATED'
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    user,
    state,
    error,
    // Getters
    isAuthenticated,
    isLoading,
    displayName,
    uid,
    // Actions
    setUser,
    setInitializing,
    setError,
    clearError,
  }
})
