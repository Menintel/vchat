<script setup>
import { RouterView } from 'vue-router'
import NavigationBar from './components/NavigationBar.vue'

import { ref, onMounted } from 'vue'
import db from './db'
import { getAuth, signOut } from 'firebase/auth'
import { addDoc, serverTimestamp, collection, onSnapshot } from 'firebase/firestore'

const user = ref('')
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
      user.value = firebaseUser.displayName || 'Anonymous'
      const userRoomsRef = collection(db, 'users', firebaseUser.uid, 'rooms')
      onSnapshot(userRoomsRef, (querySnapshot) => {
        rooms.value = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }))
        rooms.value.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
      })
    } else {
      user.value = ''
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
</script>

<template>
  <header class="container-fluid">
    <NavigationBar :user="user" :logout="logout" />
    <RouterView :user="user" @addRoom="addRoom" :rooms="rooms" v-slot="{ Component, route }">
      <component :is="Component" :key="route.path" :rooms="rooms" />
    </RouterView>
  </header>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  width: 100%;
  margin: 1rem !important;
  padding: 1rem !important;
}
</style>
