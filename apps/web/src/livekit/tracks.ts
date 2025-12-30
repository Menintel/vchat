import type { LocalParticipant, Track } from 'livekit-client'
import { useRoomStore } from '@/store/room.store'

/**
 * Enable/disable the local camera
 */
export async function toggleCamera(enabled?: boolean): Promise<void> {
  const roomStore = useRoomStore()
  const participant = roomStore.localParticipant

  if (!participant) {
    throw new Error('Not connected to a room')
  }

  await participant.setCameraEnabled(enabled ?? !participant.isCameraEnabled)
}

/**
 * Enable/disable the local microphone
 */
export async function toggleMicrophone(enabled?: boolean): Promise<void> {
  const roomStore = useRoomStore()
  const participant = roomStore.localParticipant

  if (!participant) {
    throw new Error('Not connected to a room')
  }

  await participant.setMicrophoneEnabled(enabled ?? !participant.isMicrophoneEnabled)
}

/**
 * Enable/disable screen sharing
 */
export async function toggleScreenShare(enabled?: boolean): Promise<void> {
  const roomStore = useRoomStore()
  const participant = roomStore.localParticipant

  if (!participant) {
    throw new Error('Not connected to a room')
  }

  await participant.setScreenShareEnabled(enabled ?? !participant.isScreenShareEnabled)
}

/**
 * Check if camera is currently enabled
 */
export function isCameraEnabled(): boolean {
  const roomStore = useRoomStore()
  return roomStore.localParticipant?.isCameraEnabled ?? false
}

/**
 * Check if microphone is currently enabled
 */
export function isMicrophoneEnabled(): boolean {
  const roomStore = useRoomStore()
  return roomStore.localParticipant?.isMicrophoneEnabled ?? false
}

/**
 * Check if screen share is currently enabled
 */
export function isScreenShareEnabled(): boolean {
  const roomStore = useRoomStore()
  return roomStore.localParticipant?.isScreenShareEnabled ?? false
}
