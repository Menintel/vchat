<template>
  <form class="mt-3" @submit.prevent="handleCheckIn">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-10">
          <div class="card bg-light rounded-5">
            <div class="card-body" v-if="user">
              <h1 class="font-weight-light mb-0">Check In</h1>
              <p class="font-weight-bold" v-if="roomName">
                To: <span class="text-primary"> {{ roomName }}</span>
              </p>
              <section class="form-group">
                <label class="form-control-label mx-2" for="displayName">User Name</label>
                <input
                  required
                  type="text"
                  id="displayName"
                  class="form-control rounded-pill"
                  v-model="displayName"
                />
              </section>
              <div class="form-group text-right mb-0">
                <button type="submit" class="btn btn-outline-primary mt-2 rounded-pill">
                  Check In
                </button>
              </div>
            </div>
            <div v-else class="card-body card-outline-danger text-center">
              <h1 class="text-danger card-title">Sorry</h1>
              <p class="card-text lead">
                You must be logged in to check in
                <RouterLink to="/login" class="btn btn-primary">Login</RouterLink> or
                <RouterLink to="/register" class="btn btn-primary">Register</RouterLink> and try
                again.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { doc, getDoc } from 'firebase/firestore'
import { getAuth, updateProfile } from 'firebase/auth'
import db from '../db'

const emit = defineEmits(['checkin'])

const props = defineProps({
  user: {
    type: [Object, null],
    required: false,
    default: null,
  },
})

const route = useRoute()
const router = useRouter()

const roomName = ref('')
const displayName = ref('')
const hostID = route.params.hostID
const roomID = route.params.roomID

const fetchRoom = async () => {
  try {
    const roomDocRef = doc(db, 'users', hostID, 'rooms', roomID)
    const roomDoc = await getDoc(roomDocRef)

    if (roomDoc.exists()) {
      roomName.value = roomDoc.data().name
    } else {
      router.replace('/')
    }
  } catch (error) {
    console.error('Error fetching room:', error)
    router.replace('/')
  }
}

onMounted(() => {
  if (props.user?.displayName) {
    displayName.value = props.user.displayName || 'Anonymous'
  }
  fetchRoom()
})

const handleCheckIn = async () => {
  const auth = getAuth()

  if (auth.currentUser && auth.currentUser.displayName !== displayName.value) {
    try {
      await updateProfile(auth.currentUser, { displayName: displayName.value })
    } catch (error) {
      console.error('Error updating profile:', error)
    }
  }
  emit('checkin', hostID, roomID)
  router.push(`/attendees/${hostID}/${roomID}`)
}
</script>
