<script setup>
import db from '../db.js'

import { ref, onMounted } from 'vue'

import { doc, getDoc } from 'firebase/firestore'

const user = ref('')

onMounted(() => {
  // use the newer methode to intead of the old db.collection
  const docRef = doc(db, 'users', '2SXGfT4OIMXm9dvSh1MN')
  getDoc(docRef)
    .then((snapshot) => {
      user.value = snapshot.data().name
    })
    .catch((error) => {
      console.error('Error fetching user:', error)
    })
})
</script>

<template>
  <main>
    <h1>
      Welcome : <span class="green">{{ user }}</span>
    </h1>
  </main>
</template>
