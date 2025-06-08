<script setup>
import { RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import NavigationBar from './components/NavigationBar.vue'

import { ref, onMounted } from 'vue'
import { getAuth, signOut } from 'firebase/auth'

const user = ref('')

const logout = async () => {
  try {
    await signOut(getAuth())
    // Redirect to login page after logout
    window.location.href = '/'
  } catch (error) {
    console.error('Error logging out:', error)
  }
}
onMounted(() => {
  // use the newer methode to intead of the old db.collection
  getAuth().onAuthStateChanged((firebaseUser) => {
    if (firebaseUser) {
      user.value = firebaseUser.displayName || 'Anonymous'
    } else {
      user.value = ''
    }
  })
})
</script>

<template>
  <header class="m-1">
    <div class="wrapper pt-5">
      <NavigationBar :user="user" :logout="logout" />
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <RouterView :user="user" />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  margin: 1rem !important;
  padding: 1rem !important;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin: 0 !important;
  padding: 0 !important;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
