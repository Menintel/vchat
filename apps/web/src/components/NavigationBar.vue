<template>
  <nav class="navbar-modern">
    <div class="nav-container">
      <RouterLink to="/" class="nav-brand">
        <div class="brand-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="32" height="32" rx="8" fill="url(#gradient)"/>
            <path d="M8 12L16 8L24 12V20L16 24L8 20V12Z" stroke="white" stroke-width="2" fill="none"/>
            <circle cx="16" cy="16" r="3" fill="white"/>
            <defs>
              <linearGradient id="gradient" x1="0" y1="0" x2="32" y2="32">
                <stop stop-color="#6366f1"/>
                <stop offset="1" stop-color="#a855f7"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span class="brand-text">VChat</span>
      </RouterLink>

      <div class="nav-links">
        <template v-if="isAuthenticated">
          <RouterLink to="/lobby" class="nav-link">
            <FontAwesomeIcon icon="video" />
            <span>Rooms</span>
          </RouterLink>
          <div class="nav-user">
            <div class="user-avatar">
              {{ displayName?.charAt(0)?.toUpperCase() || '?' }}
            </div>
            <span class="user-name">{{ displayName }}</span>
          </div>
          <button @click="handleLogout" class="btn-modern btn-ghost nav-btn">
            <FontAwesomeIcon icon="sign-out-alt" />
            <span class="btn-text">Logout</span>
          </button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn-modern btn-ghost nav-btn">
            Log In
          </RouterLink>
          <RouterLink to="/register" class="btn-modern btn-primary nav-btn">
            Get Started
          </RouterLink>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { logout } from '@/firebase/auth'
import { useAuthStore } from '@/store/auth.store'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const displayName = computed(() => authStore.displayName)

async function handleLogout() {
  try {
    await logout()
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
    // Optionally show a toast/notification to the user
  }
}
</script>

<style scoped>
.navbar-modern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: var(--space-md) var(--space-lg);
  background: rgba(10, 10, 15, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--glass-border);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
}

.brand-icon {
  display: flex;
  align-items: center;
}

.brand-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.nav-link:hover {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.router-link-active {
  color: var(--color-primary-light);
  background: rgba(99, 102, 241, 0.1);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-md);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
}

.user-name {
  font-size: 0.875rem;
  color: var(--color-text-primary);
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.nav-btn {
  padding: var(--space-sm) var(--space-md);
}

.btn-text {
  display: none;
}

@media (min-width: 768px) {
  .btn-text {
    display: inline;
  }
}
</style>
