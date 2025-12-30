<template>
  <div class="container-fluid mt-4">
    <div class="mb-3">
      <span class="mb-0 h2 text-primary">{{ roomName }}</span>
      <span class="ml-1" v-if="user && user.uid !== hostID">
        Hosted by: <strong class="text-danger">{{ hostDisplayName }}</strong>
      </span>
    </div>

    <div class="row">
      <div class="col-md-8">
        <div v-if="!attendeeJoined">
          <p class="lead">You are not in the room</p>
        </div>
        <div
          v-if="meetingActive"
          class="w-full h-[60vh] flex flex-col items-center"
        >
          <iframe
            ref="iframeRef"
            :src="jitsiUrl"
            allow="camera; microphone; display-capture; autoplay"
            class="w-full h-full rounded-xl border-none shadow-lg mb-4"
            title="Jitsi Meet"
          ></iframe>
        </div>
      </div>
      <div class="col-md-4">
        <button class="btn btn-outline-primary rounded-pill">Join</button>
        <button class="btn btn-outline-danger mx-2 rounded-pill">Leave</button>

        <h4 class="mt-2">Attendees</h4>
        <ul class="list-unstyled">
          <li v-for="attendee in attendeesApproved" :key="attendee.id">
            <a
              type="button"
              class="mr-2"
              title="On Air"
              @click="toggleApproval(attendee.id, attendee.approved)"
            >
              <font-awesome-icon icon="podcast" />
            </a>
            <span
              :class="[
                attendee.id === user.uid ? 'font-weight-bold text-primary' : '',
              ]"
            >
              {{ attendee.displayName }}
            </span>
          </li>
        </ul>

        <div v-if="user !== null && user.uid === hostID">
          <h5 class="mt-4">Pending</h5>
          <ul class="list-unstyled">
            <li
              class="mb-1"
              v-for="attendee in attendeesPending"
              :key="attendee.id"
            >
              <span>
                <a
                  type="button"
                  class="mr-2"
                  title="Approve Attendee"
                  @click="approveAttendee(attendee.id)"
                >
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
              <span
                class="pl-1"
                :class="[
                  attendee.id === user.uid
                    ? 'font-weight-bold text-danger'
                    : '',
                ]"
              >
                {{ attendee.displayName }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="user !== null && user.uid !== hostID">
      <p class="lead" v-if="user">
        Hi
        <strong class="text-primary font-weight-bold">{{
          user.displayName
        }}</strong
        >, you're currently in the room waiting for the owner to start the chat.
        Please wait.
      </p>
    </div>
  </div>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { collection, deleteDoc, doc, getDoc, onSnapshot, updateDoc } from 'firebase/firestore'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import db from '../db'

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

// Video Meeting State
const meetingActive = ref(false)
const jitsiUrl = ref('')
const iframeRef = ref(null)

// Variables
const attendeesPending = ref([])
const attendeesApproved = ref([])
const attendeeApproved = ref(false)
const attendeeJoined = ref(false)

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
    const tempApproved = []
    let amCheckedIn = false
    let currentUserApproved = false

    querySnapshot.forEach((doc) => {
      const attendeeData = {
        id: doc.id,
        displayName: doc.data().name,
        approved: doc.data().approved || false,
      }

      if (doc.id === props.user?.uid) {
        amCheckedIn = true
        if (attendeeData.approved) {
          currentUserApproved = true
        }
      }

      if (attendeeData.approved) {
        tempApproved.push(attendeeData)
      } else {
        tempPending.push(attendeeData)
      }
    })

    attendeesApproved.value = tempApproved
    attendeesPending.value = tempPending
    attendeeApproved.value = currentUserApproved

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

  message.value = ''

  try {
    const attendeeRef = doc(db, 'users', hostID, 'rooms', roomID, 'attendees', attendeeID)
    await deleteDoc(attendeeRef)
    message.value = 'Attendee deleted successfully'
  } catch (error) {
    console.error('Error deleting attendee:', error)
    message.value = 'Failed to delete attendee: ' + error.message
  }
}

const approveAttendee = async (attendeeID) => {
  if (!props.user || props.user.uid !== hostID) {
    message.value = 'You are not authorized to approve attendees'
    return
  }

  if (!attendeeID) {
    message.value = 'Invalid attendee ID Provided'
    return
  }

  try {
    const attendeeRef = doc(db, 'users', hostID, 'rooms', roomID, 'attendees', attendeeID)
    await updateDoc(attendeeRef, { approved: true })
    message.value = 'Attendee approved successfully'
  } catch (error) {
    console.error('Error approving attendee:', error)
    message.value = 'Failed to approve attendee: ' + error.message
  }
}

const toggleApproval = async (attendeeID, currentApprovalStatus) => {
  if (!props.user || props.user.uid !== hostID) {
    message.value = 'You are not authorized to toggle approval'
    return
  }

  if (!attendeeID) {
    message.value = 'Invalid attendee ID Provided'
    return
  }

  message.value = ''

  try {
    const attendeeRef = doc(db, 'users', hostID, 'rooms', roomID, 'attendees', attendeeID)
    const newApprovalStatus = !currentApprovalStatus

    await updateDoc(attendeeRef, { approved: newApprovalStatus })
    message.value = 'Attendee approval status toggled successfully'
  } catch (error) {
    console.error('Error toggling approval:', error)
    message.value = 'Failed to toggle approval: ' + error.message
  }
}
</script>

<style scoped>
.green {
  color: green;
}

.video-list {
  margin-bottom: 10;
  background: transparent !important;
}

.video-item {
  width: 50%;
  display: inline-block;
  background: transparent !important;
}

.video-item video {
  width: 100%;
  height: auto;
}
</style>
