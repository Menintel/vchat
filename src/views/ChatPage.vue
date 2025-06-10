<template>
  <div class="container-fluid mt-4">
    <div class="mb-3">
      <span class="mb-0 h2 text-primary">{{ roomName }}</span>
      <span class="ml-1">
        Hosted by: <strong class="text-danger">{{ hostDisplayName }}</strong>
      </span>
    </div>

    <div class="row">
      <div class="col-md-8"></div>
      <div class="col-md-4">
        <button class="btn btn-outline-primary rounded-pill">Join</button>
        <button class="btn btn-outline-danger mx-2 rounded-pill">Leave</button>

        <h4 class="mt-2">Attendees</h4>
        <ul class="list-unstyled">
          <li>
            <span class="mr-2" title="On Air">
              <font-awesome-icon icon="podcast" />
            </span>
            <span></span>
            <span class="pl-1"></span>
          </li>
        </ul>

        <div v-if="user !== null && user.uid === hostID">
          <h5 class="mt-4">Pending</h5>
          <ul class="list-unstyled">
            <li class="mb-1" v-for="attendee in attendeesPending" :key="attendee.id">
              <span>
                <a type="button" class="mr-2" title="Approve Attendee">
                  <font-awesome-icon icon="user" />
                </a>
                <a
                  type="button"
                  class="text-secondary pr-1"
                  title="Delete Attendee"
                  @click="deleteAttendee(attendee.id)"
                >
                  <font-awesome-icon icon="trash" />
                </a>
              </span>
              <span class="pl-1">{{ attendee.displayName }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="user !== null && user.uid !== hostID">
      <p class="lead">
        Hi
        <strong class="text-primary font-weight-bold">{{ user.displayName }}</strong
        >, you're currently in the room waiting for the owner to start the chat. Please wait.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import db from '../db'
import { doc, getDoc, collection, onSnapshot, deleteDoc } from 'firebase/firestore'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const emit = defineEmits(['checkin'])

// Props
const props = defineProps({
  user: {
    type: [Object, null],
    required: true,
  },
})

// Routing
const route = useRoute()
const router = useRouter()
const hostID = route.params.hostID
const roomID = route.params.roomID

// State
const roomName = ref(null)
const hostDisplayName = ref(null)
const message = ref('')

// Variables
const attendeesPending = ref([])

onMounted(() => {
  const roomRef = doc(db, 'users', hostID, 'rooms', roomID)

  // Get room name
  getDoc(roomRef).then((docSnap) => {
    if (docSnap.exists()) {
      roomName.value = docSnap.data().name
      hostDisplayName.value = docSnap.data().createdBy || 'Unknown'
    } else {
      router.replace('/')
    }
  })

  // Real-time listener for attendees
  const attendeesRef = collection(db, 'users', hostID, 'rooms', roomID, 'attendees')
  onSnapshot(attendeesRef, (querySnapshot) => {
    const tempPending = []
    let amCheckedIn = false

    querySnapshot.forEach((doc) => {
      if (doc.id === props.user?.uid) {
        amCheckedIn = true
      }

      tempPending.push({
        id: doc.id,
        displayName: doc.data().name,
      })
    })

    attendeesPending.value = tempPending

    if (!amCheckedIn && props.user?.uid) {
      emit('checkin', hostID, roomID)
    }
  })
})

const deleteAttendee = async (attendeeID) => {
  if (!props.user || props.user.uid !== hostID) {
    message.value = 'You are not authorized to delete attendees'
    return
  }

  if (!attendeeID) {
    message.value = 'Invalid attendee ID Provided'
    return
  }

  try {
    const attendeeRef = doc(db, 'users', hostID, 'rooms', roomID, 'attendees', attendeeID)
    await deleteDoc(attendeeRef)
    message.value = 'Attendee deleted successfully'
  } catch (error) {
    console.error('Error deleting attendee:', error)
    message.value = 'Failed to delete attendee: ' + error.message
  }
}
</script>
