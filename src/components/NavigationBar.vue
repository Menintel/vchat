<template>
  <div class="fixed-top">
    <nav class="navbar navbar-expand bg-primary navbar-dark rounded mt-2 h-10 mx-2 py-1">
      <div class="container-fluid">
        <RouterLink to="/" class="navbar-brand"
          ><span class="h2 pr-1">VChat</span>
          <span v-if="user" class="navbar-text small"
            >: Hi <span class="font-weight-bold green">{{ user }}</span></span
          >
        </RouterLink>
        <div class="navbar-nav ml-auto">
          <button v-if="user" @click="logout" class="btn btn-outline-danger rounded-pill mx-1">
            <span class="text-white">Log Out</span>
          </button>
          <RouterLink v-else to="/login" class="btn btn-outline-light rounded-pill mx-1"
            >Log In</RouterLink
          >
          <RouterLink to="/about" class="btn btn-outline-light rounded-pill mx-1">About</RouterLink>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
const { user, logout } = defineProps({
  user: String,
  logout: Function,
})
</script>
