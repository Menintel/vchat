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
    <div class="row justify-content-center">
      <div class="col-11 col-md-8 col-lg-6">
        <div class="card border-top-0 rounded-0">
          <div class="card-body py-2">
            <h4 class="card-title">Your Rooms</h4>
          </div>
          <div class="list-group list-group-flush">
            <div v-if="!rooms || rooms.length === 0" class="list-group-item">
              No rooms available. Create one above!
            </div>
            <template v-else>
              <div
                class="list-group-item list-group-item-action"
                v-for="room in rooms"
                :key="room.id"
              >
                {{ room.name }}
                <span class="text-muted small" v-if="room.createdBy">
                  (created by {{ room.createdBy }})</span
                >
              </div>
            </template>
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

defineProps({
  rooms: {
    type: Array,
    required: true,
    default: () => [],
  },
})

const emit = defineEmits(['addRoom'])

const handleAdd = () => {
  if (!roomName.value.trim()) return
  emit('addRoom', roomName.value)
  roomName.value = ''
  roomNameRef.value.focus()
}
</script>
