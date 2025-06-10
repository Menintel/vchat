<template>
  <div class="container mt-4">
    <div class="container">
      <div class="col-12 col-10">
        <h1 class="font-weight-light text-center">Add Room</h1>
        <div class="card bg-light rounded-4">
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
                <div>
                  <button
                    class="btn btn-outline-primary rounded-pill mx-4"
                    type="submit"
                    id="buttonAdd"
                    @click.prevent="handleAdd"
                  >
                    Add Room
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-5">
      <div class="col-12">
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
                <section class="btn-group align-self-center" role="group" aria-label="Room Options">
                  <button
                    title="Delete Room"
                    class="btn btn-outline-secondary btn-sm"
                    @click="handleDelete(room.id)"
                  >
                    <FontAwesomeIcon icon="fa-trash" />
                  </button>
                  <RouterLink
                    :to="`/checkin/${user?.uid}/${room.id}`"
                    class="btn btn-outline-secondary btn-sm"
                    title="Check In"
                  >
                    <FontAwesomeIcon icon="fa-user" />
                  </RouterLink>
                  <RouterLink
                    class="btn btn-outline-secondary btn-sm"
                    title="chat"
                    :to="`/chat/${user?.uid}/${room.id}`"
                  >
                    <FontAwesomeIcon icon="fa-video" />
                  </RouterLink>
                </section>
                <section class="align-self-center pl-3 text-center">
                  {{ room.name }}
                </section>
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
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const roomName = ref('')
const roomNameRef = ref(null)

defineProps({
  rooms: {
    type: Array,
    required: true,
    default: () => [],
  },
  user: {
    type: Object,
    required: false,
    default: null,
  },
})

const emit = defineEmits(['addRoom', 'deleteRoom'])

const handleAdd = () => {
  if (!roomName.value.trim()) return
  emit('addRoom', roomName.value)
  roomName.value = ''
  roomNameRef.value.focus()
}

const handleDelete = (roomId) => {
  if (confirm('Are you sure you want to delete this room?')) {
    emit('deleteRoom', roomId)
  }
}
</script>
