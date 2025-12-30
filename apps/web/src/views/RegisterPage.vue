<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card glass-card">
        <div class="auth-header">
          <div class="auth-logo">
            <svg width="48" height="48" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="32" height="32" rx="8" fill="url(#gradient2)"/>
              <path d="M8 12L16 8L24 12V20L16 24L8 20V12Z" stroke="white" stroke-width="2" fill="none"/>
              <circle cx="16" cy="16" r="3" fill="white"/>
              <defs>
                <linearGradient id="gradient2" x1="0" y1="0" x2="32" y2="32">
                  <stop stop-color="#6366f1"/>
                  <stop offset="1" stop-color="#a855f7"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 class="auth-title">Create your account</h1>
          <p class="auth-subtitle">Start video conferencing in seconds</p>
        </div>

        <div class="alert-modern alert-error" v-if="error">
          <FontAwesomeIcon icon="exclamation-circle" />
          {{ error }}
        </div>

        <form @submit.prevent="handleRegister" class="auth-form">
          <div class="form-group">
            <label class="input-label" for="displayName">Display name</label>
            <input
              type="text"
              id="displayName"
              class="input-modern"
              placeholder="John Doe"
              v-model="displayName"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label class="input-label" for="email">Email address</label>
            <input
              type="email"
              id="email"
              class="input-modern"
              placeholder="you@example.com"
              v-model="email"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="input-label" for="password">Password</label>
              <input
                type="password"
                id="password"
                class="input-modern"
                placeholder="••••••••"
                v-model="password"
                required
                :disabled="isLoading"
                minlength="6"
              />
            </div>

            <div class="form-group">
              <label class="input-label" for="confirmPassword">Confirm</label>
              <input
                type="password"
                id="confirmPassword"
                class="input-modern"
                placeholder="••••••••"
                v-model="confirmPassword"
                required
                :disabled="isLoading"
              />
            </div>
          </div>

          <button 
            type="submit" 
            class="btn-modern btn-primary btn-full"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="spinner"></span>
            {{ isLoading ? 'Creating account...' : 'Create account' }}
          </button>
        </form>

        <div class="auth-divider">
          <span>or continue with</span>
        </div>

        <button 
          type="button" 
          class="btn-modern btn-secondary btn-full btn-google"
          @click="handleGoogleSignup"
          :disabled="isLoading"
        >
          <svg width="20" height="20" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Continue with Google
        </button>

        <p class="auth-footer">
          Already have an account?
          <RouterLink to="/login" class="auth-link">Sign in</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginWithGoogle, registerWithEmail } from '@/firebase/auth'
import { useAuthStore } from '@/store/auth.store'

const router = useRouter()
const authStore = useAuthStore()

const displayName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref<string | null>(null)

const isLoading = computed(() => authStore.isLoading)

async function handleRegister() {
  error.value = null

  if (!displayName.value || !email.value || !password.value) {
    error.value = 'Please fill in all fields'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  try {
    await registerWithEmail(email.value, password.value, displayName.value)
    router.push('/lobby')
  } catch (err: any) {
    if (err.code === 'auth/email-already-in-use') {
      error.value = 'Email already in use'
    } else if (err.code === 'auth/invalid-email') {
      error.value = 'Invalid email address'
    } else if (err.code === 'auth/weak-password') {
      error.value = 'Password is too weak'
    } else {
      error.value = authStore.error || 'Failed to create account'
    }
  }
}

async function handleGoogleSignup() {
  error.value = null

  try {
    await loginWithGoogle()
    router.push('/lobby')
  } catch (err) {
    error.value = authStore.error || 'Google sign up failed'
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl);
  padding-top: 100px;
}

.auth-container {
  width: 100%;
  max-width: 480px;
}

.auth-card {
  padding: var(--space-2xl);
}

.auth-header {
  text-align: center;
  margin-bottom: var(--space-xl);
}

.auth-logo {
  margin-bottom: var(--space-lg);
}

.auth-logo svg {
  width: 56px;
  height: 56px;
}

.auth-title {
  font-size: 1.75rem;
  margin-bottom: var(--space-sm);
}

.auth-subtitle {
  color: var(--color-text-muted);
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.form-row {
  display: flex;
  gap: var(--space-md);
}

.btn-full {
  width: 100%;
  padding: var(--space-md) var(--space-lg);
  font-size: 1rem;
}

.btn-google {
  gap: var(--space-sm);
}

.auth-divider {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin: var(--space-lg) 0;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.auth-divider::before,
.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--glass-border);
}

.auth-footer {
  text-align: center;
  margin-top: var(--space-xl);
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.auth-link {
  color: var(--color-primary-light);
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}

.alert-modern {
  margin-bottom: var(--space-lg);
}
</style>
