<template>
  <div class="container mt-4">
    <div class="container">
      <div class="col-12 col-10">
        <h1 class="font-weight-light text-center">Add Room</h1>
        <div class="card bg-light rounded-pill">
          <div class="card-body text-center">
            <form class="form-group">
              <div class="input-group input-group-lg">
                <input
                  type="text"
                  class="form-control rounded-pill"
                  name="roomName"
                  placeholder="Room Name"
                  aria-describedby="buttonAdd"
                  v-model="roomName"
                  ref="roomNameRef"
                />
                <div class="input-group-append">
                  <button
                    class="btn btn-outline-primary rounded-pill mx-4"
                    type="submit"
                    id="buttonAdd"
                    @click.prevent="handleAdd"
                  >
                    +
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const roomName = ref('')
const roomNameRef = ref(null)
const emit = defineEmits(['addRoom'])

const handleAdd = () => {
  emit('addRoom', roomName.value)
  roomName.value = ''
  roomNameRef.value.focus()
}
</script>
