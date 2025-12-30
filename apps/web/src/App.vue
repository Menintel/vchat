<template>
  <div class="app-container">
    <NavigationBar />
    <main class="main-content">
      <RouterView v-slot="{ Component, route }">
        <Suspense>
          <template #default>
            <component :is="Component" :key="route.path" />
          </template>
          <template #fallback>
            <div class="loading-container">
              <div class="loading-spinner"></div>
              <p>Loading...</p>
            </div>
          </template>
        </Suspense>
      </RouterView>
    </main>
  </div>
</template>

<script setup lang="ts">
import NavigationBar from './components/NavigationBar.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--glass-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--space-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
