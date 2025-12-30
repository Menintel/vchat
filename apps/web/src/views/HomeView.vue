<script setup>
import HelloWorld from '../components/HelloWorld.vue'

defineProps({
  user: {
    type: Object,
    required: false,
    default: null,
  },
})
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-8 col-lg-6 text-center">
      <div v-if="user">
        <HelloWorld msg="You did it!" />
        Welcome <span class="font-weight-bold green">{{ user.displayName }}</span>
      </div>
      <div v-else>
        <HelloWorld msg="You did it!" />
      </div>
      <h4 class="display-4 text-primary mb-2">Video Chat</h4>
      <p class="lead">
        This App uses firebase for real time communication and Jisti WebRTC for video chat between
        multiple users, this awllows you to create rooms for your meetings.
      </p>
      <RouterLink v-if="!user" to="/login" class="btn btn-outline-primary rounded-pill mr-2"
        >Login</RouterLink
      >
      <RouterLink v-if="!user" to="/register" class="btn btn-outline-secondary rounded-pill me-2"
        >Register</RouterLink
      >
      <RouterLink v-if="user" to="/rooms" class="btn btn-outline-success rounded-pill"
        >Rooms</RouterLink
      >
    </div>
  </div>
</template>
