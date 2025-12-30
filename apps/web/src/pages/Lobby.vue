<template>
  <div class="lobby-page">
    <div class="lobby-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="text-gradient">Video Rooms</span>
        </h1>
        <p class="page-subtitle">Join a room or create your own to start conferencing</p>
      </div>
      <button 
        class="btn-modern btn-primary create-btn"
        @click="showCreateModal = true"
      >
        <FontAwesomeIcon icon="video" />
        Create Room
      </button>
    </div>

    <!-- Room Grid -->
    <div class="rooms-section">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner spinner-lg"></div>
        <p>Loading rooms...</p>
      </div>
      
      <div v-else-if="rooms.length === 0" class="empty-state glass-card">
        <div class="empty-icon">
          <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
            <circle cx="40" cy="40" r="38" stroke="url(#emptyGrad)" stroke-width="2" stroke-dasharray="4 4"/>
            <path d="M30 35L40 30L50 35V45L40 50L30 45V35Z" stroke="url(#emptyGrad)" stroke-width="2" fill="none"/>
            <circle cx="40" cy="40" r="4" fill="url(#emptyGrad)"/>
            <defs>
              <linearGradient id="emptyGrad" x1="0" y1="0" x2="80" y2="80">
                <stop stop-color="#6366f1"/>
                <stop offset="1" stop-color="#a855f7"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <h3>No rooms yet</h3>
        <p>Be the first to create a video room and invite others to join.</p>
        <button class="btn-modern btn-primary" @click="showCreateModal = true">
          <FontAwesomeIcon icon="video" />
          Create Your First Room
        </button>
      </div>
      
      <div v-else class="rooms-grid">
        <div 
          v-for="room in rooms" 
          :key="room.id"
          class="room-card"
        >
          <div class="room-header">
            <div class="room-status" :class="{ active: room.activeParticipants > 0 }">
              <span class="status-dot"></span>
              {{ room.activeParticipants > 0 ? 'Live' : 'Empty' }}
            </div>
          </div>
          <h3 class="room-name">{{ room.name }}</h3>
          <p class="room-host">
            <FontAwesomeIcon icon="user" class="host-icon" />
            {{ room.hostName || 'Unknown host' }}
          </p>
          <div class="room-stats">
            <div class="stat">
              <FontAwesomeIcon icon="user" />
              <span>{{ room.activeParticipants || 0 }} online</span>
            </div>
          </div>
          <button 
            class="btn-modern btn-primary btn-join"
            @click="joinRoom(room)"
          >
            <FontAwesomeIcon icon="video" />
            Join Room
          </button>
        </div>
      </div>
    </div>

    <!-- Create Room Modal -->
    <Teleport to="body">
      <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
        <div class="modal-content glass-card">
          <div class="modal-header">
            <h2>Create New Room</h2>
            <button class="modal-close" @click="showCreateModal = false">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <form @submit.prevent="createRoom" class="modal-form">
            <div class="form-group">
              <label class="input-label">Room Name</label>
              <input 
                type="text" 
                class="input-modern"
                v-model="newRoomName"
                placeholder="My Awesome Meeting"
                required
              />
            </div>
            <div class="form-group">
              <label class="checkbox-modern">
                <input type="checkbox" v-model="isPublic" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Make this room public</span>
              </label>
              <p class="checkbox-hint">Public rooms can be discovered by anyone</p>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn-modern btn-secondary" @click="showCreateModal = false">
                Cancel
              </button>
              <button type="submit" class="btn-modern btn-primary" :disabled="!newRoomName.trim()">
                <FontAwesomeIcon icon="video" />
                Create Room
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { collection, addDoc, onSnapshot, serverTimestamp, query, where } from 'firebase/firestore'
import { db } from '@/firebase/config'

interface RoomInfo {
  id: string
  name: string
  hostId: string
  hostName: string
  isPublic: boolean
  activeParticipants: number
  createdAt: Date
}

const router = useRouter()
const authStore = useAuthStore()

const rooms = ref<RoomInfo[]>([])
const isLoading = ref(true)
const showCreateModal = ref(false)
const newRoomName = ref('')
const isPublic = ref(true)

onMounted(() => {
  const roomsRef = collection(db, 'rooms')
  const publicRoomsQuery = query(roomsRef, where('isPublic', '==', true))
  
  onSnapshot(publicRoomsQuery, (snapshot) => {
    rooms.value = snapshot.docs.map(doc => ({
      id: doc.id,
      name: doc.data().name,
      hostId: doc.data().hostId,
      hostName: doc.data().hostName,
      isPublic: doc.data().isPublic,
      activeParticipants: doc.data().activeParticipants || 0,
      createdAt: doc.data().createdAt?.toDate() || new Date(),
    }))
    isLoading.value = false
  })
})

async function createRoom() {
  if (!newRoomName.value.trim() || !authStore.user) return
  
  try {
    const roomsRef = collection(db, 'rooms')
    const docRef = await addDoc(roomsRef, {
      name: newRoomName.value.trim(),
      hostId: authStore.uid,
      hostName: authStore.displayName,
      isPublic: isPublic.value,
      activeParticipants: 0,
      createdAt: serverTimestamp(),
    })
    
    showCreateModal.value = false
    newRoomName.value = ''
    
    router.push(`/chat/${authStore.uid}/${docRef.id}`)
  } catch (error) {
    console.error('Error creating room:', error)
  }
}

function joinRoom(room: RoomInfo) {
  router.push(`/chat/${room.hostId}/${room.id}`)
}
</script>

<style scoped>
.lobby-page {
  padding: 100px var(--space-lg) var(--space-2xl);
  max-width: 1400px;
  margin: 0 auto;
}

.lobby-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-2xl);
  flex-wrap: wrap;
  gap: var(--space-lg);
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: var(--space-sm);
}

.page-subtitle {
  color: var(--color-text-muted);
  margin: 0;
}

.create-btn {
  padding: var(--space-md) var(--space-xl);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-2xl);
  color: var(--color-text-muted);
}

.spinner-lg {
  width: 40px;
  height: 40px;
  margin-bottom: var(--space-md);
}

.empty-state {
  text-align: center;
  padding: var(--space-2xl);
  max-width: 500px;
  margin: 0 auto;
}

.empty-icon {
  margin-bottom: var(--space-lg);
}

.empty-state h3 {
  margin-bottom: var(--space-sm);
}

.empty-state p {
  margin-bottom: var(--space-lg);
}

.rooms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.room-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.room-header {
  display: flex;
  justify-content: flex-end;
}

.room-status {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  padding: var(--space-xs) var(--space-sm);
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-full);
}

.room-status.active {
  color: var(--color-success);
  background: rgba(34, 197, 94, 0.1);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.room-status.active .status-dot {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.room-name {
  font-size: 1.25rem;
  margin: 0;
}

.room-host {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin: 0;
}

.host-icon {
  font-size: 0.75rem;
}

.room-stats {
  display: flex;
  gap: var(--space-md);
  margin: var(--space-sm) 0;
}

.stat {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.btn-join {
  margin-top: auto;
  width: 100%;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: var(--space-lg);
}

.modal-content {
  width: 100%;
  max-width: 480px;
  padding: var(--space-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xl);
}

.modal-header h2 {
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: var(--space-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.modal-close:hover {
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.checkbox-modern {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  cursor: pointer;
}

.checkbox-modern input {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.checkbox-modern input:checked + .checkmark {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.checkbox-modern input:checked + .checkmark::after {
  content: '✓';
  color: white;
  font-size: 0.75rem;
}

.checkbox-label {
  font-size: 0.875rem;
  color: var(--color-text-primary);
}

.checkbox-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin: var(--space-xs) 0 0 calc(20px + var(--space-sm));
}

.modal-actions {
  display: flex;
  gap: var(--space-md);
  justify-content: flex-end;
  margin-top: var(--space-md);
}
</style>
