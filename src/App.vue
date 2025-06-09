<template>
  <header class="container-fluid">
    <NavigationBar :user="user" :logout="logout" />
    <RouterView v-slot="{ Component, route }">
      <component
        :is="Component"
        :key="route.path"
        :user="user"
        :rooms="rooms"
        @logout="logout"
        @checkin="checkin"
        @addRoom="addRoom"
        @deleteRoom="deleteRoom"
      />
    </RouterView>
  </header>
</template>

<script setup>
import NavigationBar from './components/NavigationBar.vue'

import { ref, onMounted } from 'vue'
import db from './db'
import { getAuth, signOut } from 'firebase/auth'
import {
  addDoc,
  serverTimestamp,
  collection,
  onSnapshot,
  doc,
  deleteDoc,
  getDoc,
  setDoc,
} from 'firebase/firestore'

const user = ref(null)
const message = ref('')
const rooms = ref([])

const logout = async () => {
  try {
    await signOut(getAuth())
    // Redirect to login page after logout
    window.location.href = '/'
  } catch (error) {
    console.error('Error logging out:', error)
  }
}
onMounted(() => {
  // use the newer methode to intead of the old db.collection
  getAuth().onAuthStateChanged((firebaseUser) => {
    if (firebaseUser) {
      user.value = firebaseUser
      const userRoomsRef = collection(db, 'users', firebaseUser.uid, 'rooms')
      onSnapshot(userRoomsRef, (querySnapshot) => {
        rooms.value = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }))
        rooms.value.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
      })
    } else {
      user.value = null
    }
  })
})

const addRoom = async (roomName) => {
  const currentUser = getAuth().currentUser

  if (!currentUser) {
    message.value = 'Please login to add a room'
    return
  }

  try {
    const roomRef = collection(db, 'users', currentUser.uid, 'rooms')
    await addDoc(roomRef, {
      name: roomName,
      createdAt: serverTimestamp(),
      createdBy: currentUser.displayName,
    })
    message.value = `Room "${roomName}" added successfully`
  } catch (error) {
    console.error('Error adding room:', error)
    message.value = 'Failed to add room: ' + error.message
  }
}

const deleteRoom = async (roomId) => {
  const currentUser = getAuth().currentUser

  if (!currentUser) {
    message.value = 'Please login to delete a room'
    return
  }

  try {
    const roomRef = doc(db, 'users', currentUser.uid, 'rooms', roomId)
    await deleteDoc(roomRef)
    message.value = `Room "${roomId}" deleted successfully`
  } catch (error) {
    console.error('Error deleting room:', error)
    message.value = 'Failed to delete room: ' + error.message
  }
}

const checkin = async (hostID, roomID) => {
  const currentUser = getAuth().currentUser

  if (!currentUser) {
    message.value = 'Please login to check in'
    return
  }

  const roomRef = doc(db, 'users', hostID, 'rooms', roomID)

  try {
    const docSnap = await getDoc(roomRef)

    if (docSnap.exists()) {
      const attendeeRef = doc(db, 'users', hostID, 'rooms', roomID, 'attendees', currentUser.uid)
      await setDoc(attendeeRef, {
        name: currentUser.displayName,
        createdAt: serverTimestamp(),
      })
      message.value = `Successfully checked in to room "${roomID}"`
    } else {
      message.value = `Room "${roomID}" not found`
    }
  } catch (error) {
    console.error('Error checking in:', error)
    message.value = 'Failed to check in: ' + error.message
  }
}
</script>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  width: 100%;
  margin: 1rem !important;
  padding: 1rem !important;
}
</style>
