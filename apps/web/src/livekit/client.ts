import { Room, RoomEvent, type RoomOptions } from 'livekit-client'
import { useRoomStore } from '@/store/room.store'

const DEFAULT_ROOM_OPTIONS: RoomOptions = {
  adaptiveStream: true,
  dynacast: true,
  videoCaptureDefaults: {
    resolution: {
      width: 1280,
      height: 720,
      frameRate: 30,
    },
  },
  audioCaptureDefaults: {
    echoCancellation: true,
    noiseSuppression: true,
    autoGainControl: true,
  },
}

/**
 * Connect to a LiveKit room
 */
export async function connectToRoom(
  serverUrl: string,
  token: string,
  options: Partial<RoomOptions> = {}
): Promise<Room> {
  const roomStore = useRoomStore()
  
  try {
    roomStore.setConnectionState('CONNECTING')

    const room = new Room({ ...DEFAULT_ROOM_OPTIONS, ...options })
    
    // Set up event handlers
    room.on(RoomEvent.Disconnected, () => {
      roomStore.setConnectionState('DISCONNECTED')
      roomStore.setCurrentRoom(null)
    })

    room.on(RoomEvent.Reconnecting, () => {
      roomStore.setConnectionState('RECONNECTING')
    })

    room.on(RoomEvent.Reconnected, () => {
      roomStore.setConnectionState('CONNECTED')
    })

    room.on(RoomEvent.ParticipantConnected, (participant) => {
      console.log('Participant connected:', participant.identity)
    })

    room.on(RoomEvent.ParticipantDisconnected, (participant) => {
      console.log('Participant disconnected:', participant.identity)
    })

    // Connect to the room
    await room.connect(serverUrl, token)
    
    roomStore.setCurrentRoom(room)
    roomStore.setConnectionState('CONNECTED')
    
    return room
  } catch (error) {
    roomStore.setConnectionState('DISCONNECTED')
    roomStore.setError(error instanceof Error ? error.message : 'Connection failed')
    throw error
  }
}

/**
 * Disconnect from the current room
 */
export async function disconnectFromRoom(): Promise<void> {
  const roomStore = useRoomStore()
  const room = roomStore.currentRoom

  if (room) {
    await room.disconnect()
    roomStore.setCurrentRoom(null)
  }
}

/**
 * Get the LiveKit server URL from environment
 */
export function getLiveKitUrl(): string {
  return import.meta.env.VITE_LIVEKIT_URL || 'ws://localhost:7880'
}
