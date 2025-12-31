<template>
  <nav class="navbar-modern">
    <div class="nav-container">
      <RouterLink to="/" class="nav-brand">
        <div class="brand-icon">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
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
          <button @click="handleLogout" class="nav-btn btn-ghost">
            <FontAwesomeIcon icon="sign-out-alt" />
            <span class="btn-text">Logout</span>
          </button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="nav-btn btn-ghost">
            Log In
          </RouterLink>
          <RouterLink to="/register" class="nav-btn btn-primary">
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
  padding: 0.75rem 1.5rem;
  background: rgba(10, 10, 15, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
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
  gap: 0.75rem;
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.nav-brand:hover {
  opacity: 0.9;
}

.brand-icon {
  display: flex;
  align-items: center;
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(to right, #6366f1, #a855f7);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
  letter-spacing: -0.025em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: var(--color-text-secondary, #94a3b8);
  text-decoration: none;
  border-radius: 9999px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  font-weight: 500;
}

.nav-link:hover {
  color: var(--color-text-primary, #f8fafc);
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.router-link-active {
  color: var(--color-primary-light, #818cf8);
  background: rgba(99, 102, 241, 0.1);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem 0.25rem 0.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 9999px;
  transition: border-color 0.2s ease;
}

.nav-user:hover {
  border-color: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.user-name {
  font-size: 0.85rem;
  color: var(--color-text-primary, #f1f5f9);
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.nav-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  border-radius: 9999px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
}

.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary, #94a3b8);
}
.btn-ghost:hover {
  color: var(--color-text-primary, #f8fafc);
  background: rgba(255, 255, 255, 0.05);
}

.btn-primary {
  background: #6366f1;
  color: white;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25);
}
.btn-primary:hover {
  background: #4f46e5;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
  transform: translateY(-1px);
}

.btn-text {
  display: none;
}

@media (min-width: 768px) {
  .btn-text {
    display: inline;
  }
}

@media (max-width: 640px) {
  .navbar-modern {
    padding: 0.75rem 1rem;
  }
  
  .nav-brand {
    gap: 0.5rem;
  }
  
  .brand-text {
    font-size: 1.1rem;
  }
  
  .nav-links {
    gap: 0.5rem;
  }
  
  .nav-link {
    padding: 0.5rem;
  }
  
  .nav-link span {
    display: none;
  }
}
</style>
