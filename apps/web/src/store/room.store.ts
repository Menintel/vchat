import type { Room as LiveKitRoom, LocalParticipant, RemoteParticipant } from 'livekit-client'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export interface RoomInfo {
  id: string
  name: string
  hostId: string
  hostName: string
  isPublic: boolean
  activeParticipants: number
  createdAt: Date
}

export type ConnectionState = 'DISCONNECTED' | 'CONNECTING' | 'CONNECTED' | 'RECONNECTING'

export const useRoomStore = defineStore('room', () => {
  // State
  const rooms = ref<RoomInfo[]>([])
  const currentRoom = ref<LiveKitRoom | null>(null)
  const connectionState = ref<ConnectionState>('DISCONNECTED')
  const error = ref<string | null>(null)

  // Getters
  const isConnected = computed(() => connectionState.value === 'CONNECTED')
  const isConnecting = computed(() => connectionState.value === 'CONNECTING')
  const localParticipant = computed(() => currentRoom.value?.localParticipant ?? null)
  const remoteParticipants = computed(() =>
    currentRoom.value ? Array.from(currentRoom.value.remoteParticipants.values()) : []
  )
  const participantCount = computed(() => remoteParticipants.value.length + 1)

  // Actions
  function setRooms(newRooms: RoomInfo[]) {
    rooms.value = newRooms
  }

  function addRoom(room: RoomInfo) {
    rooms.value.push(room)
  }

  function removeRoom(roomId: string) {
    rooms.value = rooms.value.filter((r) => r.id !== roomId)
  }

  function setCurrentRoom(room: LiveKitRoom | null) {
    currentRoom.value = room
    connectionState.value = room ? 'CONNECTED' : 'DISCONNECTED'
  }

  function setConnectionState(state: ConnectionState) {
    connectionState.value = state
  }

  function setError(message: string) {
    error.value = message
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    rooms,
    currentRoom,
    connectionState,
    error,
    // Getters
    isConnected,
    isConnecting,
    localParticipant,
    remoteParticipants,
    participantCount,
    // Actions
    setRooms,
    addRoom,
    removeRoom,
    setCurrentRoom,
    setConnectionState,
    setError,
    clearError,
  }
})
