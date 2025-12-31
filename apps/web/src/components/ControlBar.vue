<template>
  <div class="control-bar-wrapper">
    <div class="control-bar glass-card">
      <!-- Media Controls -->
      <div class="control-group">
        <button 
          class="control-btn" 
          :class="{ 'is-active': !isMicEnabled, 'is-danger': !isMicEnabled }"
          @click="toggleMic"
          v-b-tooltip.hover
          :title="isMicEnabled ? 'Mute Microphone' : 'Unmute Microphone'"
        >
          <font-awesome-icon :icon="isMicEnabled ? 'microphone' : 'microphone-slash'" />
        </button>

        <button 
          class="control-btn"
          :class="{ 'is-active': !isCameraEnabled, 'is-danger': !isCameraEnabled }"
          @click="toggleCam"
          v-b-tooltip.hover
          :title="isCameraEnabled ? 'Turn Off Camera' : 'Turn On Camera'"
        >
          <font-awesome-icon :icon="isCameraEnabled ? 'video' : 'video-slash'" />
        </button>
      </div>

      <!-- Action Controls -->
      <div class="control-group">
        <button 
          class="control-btn"
          :class="{ 'is-active': isScreenShareEnabled }"
          @click="toggleShare"
          v-b-tooltip.hover
          title="Share Screen"
        >
          <font-awesome-icon icon="desktop" />
        </button>

        <button 
          class="control-btn"
          :class="{ 'is-primary': showChat }"
          @click="$emit('toggle-chat')"
          v-b-tooltip.hover
          title="Toggle Chat"
        >
          <font-awesome-icon icon="comment-dots" />
          <span v-if="unreadCount > 0" class="badge-count">{{ unreadCount }}</span>
        </button>

        <button 
          class="control-btn"
          @click="$emit('toggle-participants')"
          v-b-tooltip.hover
          title="Participants"
        >
          <font-awesome-icon icon="users" />
        </button>
      </div>

      <!-- Leave Control -->
      <div class="control-group">
        <button 
          class="control-btn btn-leave"
          @click="$emit('leave')"
          v-b-tooltip.hover
          title="Leave Room"
        >
          <font-awesome-icon icon="phone-slash" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { computed } from 'vue'
import { toggleCamera, toggleMicrophone, toggleScreenShare } from '@/livekit/tracks'
import { useRoomStore } from '@/store/room.store'

// const props = defineProps... (already defined above in macro, no need to capture if unused)
withDefaults(
  defineProps<{
    showChat: boolean
    unreadCount?: number
  }>(),
  {
    unreadCount: 0,
  }
)

defineEmits(['toggle-chat', 'toggle-participants', 'leave'])

const roomStore = useRoomStore()

// State
// In a real app we might want to listen to store changes reactively.
// Since tracks.ts functions return simple booleans, we might need a reactive source.
// LiveKit events usually drive the state. For now, we will optimize for local optimistic updates.
// Ideally usage of `useRoomStore` which should have reactive state about local participant.

const isMicEnabled = computed(() => roomStore.localParticipant?.isMicrophoneEnabled ?? false)
const isCameraEnabled = computed(() => roomStore.localParticipant?.isCameraEnabled ?? false)
const isScreenShareEnabled = computed(
  () => roomStore.localParticipant?.isScreenShareEnabled ?? false
)

// Actions
const toggleMic = async () => {
  try {
    const newState = !isMicEnabled.value
    await toggleMicrophone(newState)
  } catch (e) {
    console.error('Failed to toggle mic', e)
  }
}

const toggleCam = async () => {
  try {
    const newState = !isCameraEnabled.value
    await toggleCamera(newState)
  } catch (e) {
    console.error('Failed to toggle camera', e)
  }
}

const toggleShare = async () => {
  try {
    const newState = !isScreenShareEnabled.value
    await toggleScreenShare(newState)
  } catch (e) {
    console.error('Failed to toggle screen share', e)
  }
}
</script>

<style scoped>
.control-bar-wrapper {
  display: flex;
  justify-content: center;
  padding: 1rem;
  width: 100%;
}

.control-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.5rem 1.5rem;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.control-bar:hover {
  background: rgba(15, 23, 42, 0.95);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.control-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-secondary, #94a3b8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-2px);
}

.control-btn:active {
  transform: translateY(0);
}

.control-btn.is-active {
  background: white;
  color: var(--color-primary, #6366f1);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
}

.control-btn.is-primary {
  background: var(--color-primary, #6366f1);
  color: white;
}
.control-btn.is-primary:hover {
  background: var(--color-primary-dark, #4f46e5);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.control-btn.is-danger {
  background: var(--color-error, #ef4444);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}
.control-btn.is-danger:hover {
  background: #dc2626;
}

.btn-leave {
  background: rgba(239, 68, 68, 0.15);
  color: var(--color-error, #ef4444);
  width: 42px;
  height: 42px;
}

.btn-leave:hover {
  background: var(--color-error, #ef4444);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.badge-count {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--color-error, #ef4444);
  color: white;
  font-size: 0.65rem;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 10px;
  border: 2px solid #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@media (max-width: 640px) {
  .control-bar {
    gap: 0.75rem;
    padding: 0.5rem 1rem;
    width: auto;
    max-width: 95vw;
  }
  
  .control-group {
    gap: 0.5rem;
  }
  
  .control-btn {
    width: 38px;
    height: 38px;
    font-size: 1rem;
  }
  
  .btn-leave {
    width: 38px;
    height: 38px;
  }
}
</style>
