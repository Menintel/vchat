<script setup>
const props = defineProps({
  user: String,
})
</script>

<template>
  <div class="mt-3">
    <div v-if="user" class="text-center">
      Welcome <span class="font-weight-bold green">{{ props.user }}</span>
    </div>
    <div class="container text-center">
      <div class="row justify-content-center">
        <div class="col-10 col-md-10 col-lg-8 col-xl-7">
          <h4 class="display-4 text-primary mb-2">Video Chat</h4>
          <p class="lead">
            This App uses firebase for real time communication and Jisti WebRTC for video chat
            between multiple users, this awllows you to create rooms for your meetings.
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
        </div>
      </div>
    </div>
  </div>
</template>
