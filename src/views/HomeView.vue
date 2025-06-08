<script setup>
import HelloWorld from '../components/HelloWorld.vue'

const props = defineProps({
  user: String,
})
</script>

<template>
  <div class="mt-3">
    <div v-if="user" class="text-center">
      <HelloWorld msg="You did it!" />
      Welcome <span class="font-weight-bold green">{{ props.user }}</span>
    </div>
    <div v-else class="text-center">
      <HelloWorld msg="You did it!" />
    </div>
    <div class="container text-center">
      <div class="col-12">
        <h4 class="display-4 text-primary mb-2">Video Chat</h4>
        <p class="lead">
          This App uses firebase for real time communication and Jisti WebRTC for video chat between
          multiple users, this awllows you to create rooms for your meetings.
        </p>
        <RouterLink v-if="!user" to="/login" class="btn btn-outline-primary rounded-pill mr-2"
          >Login</RouterLink
        >
        <RouterLink
          v-if="!user"
          to="/register"
          class="btn btn-outline-secondary rounded-pill mr-2 mx-2"
          >Register</RouterLink
        >
        <RouterLink v-if="user" to="/rooms" class="btn btn-outline-success rounded-pill mr-2 mx-2"
          >Rooms</RouterLink
        >
      </div>
    </div>
  </div>
</template>
