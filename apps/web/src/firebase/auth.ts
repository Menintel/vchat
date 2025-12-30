import {
  createUserWithEmailAndPassword,
  GoogleAuthProvider,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
  type User,
  type UserCredential,
  updateProfile,
} from 'firebase/auth'
import { useAuthStore } from '@/store/auth.store'
import { auth } from './config'

/**
 * Sign in with email and password
 */
export async function loginWithEmail(email: string, password: string): Promise<User> {
  const authStore = useAuthStore()
  authStore.setInitializing()

  try {
    const credential: UserCredential = await signInWithEmailAndPassword(auth, email, password)
    authStore.setUser(credential.user)
    return credential.user
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Login failed'
    authStore.setError(message)
    throw error
  }
}

/**
 * Register with email and password
 */
export async function registerWithEmail(
  email: string,
  password: string,
  displayName?: string
): Promise<User> {
  const authStore = useAuthStore()
  authStore.setInitializing()

  try {
    const credential: UserCredential = await createUserWithEmailAndPassword(auth, email, password)

    // Update display name if provided
    if (displayName && credential.user) {
      await updateProfile(credential.user, { displayName })
    }

    authStore.setUser(credential.user)
    return credential.user
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Registration failed'
    authStore.setError(message)
    throw error
  }
}

/**
 * Sign in with Google
 */
export async function loginWithGoogle(): Promise<User> {
  const authStore = useAuthStore()
  authStore.setInitializing()

  try {
    const provider = new GoogleAuthProvider()
    const credential: UserCredential = await signInWithPopup(auth, provider)
    authStore.setUser(credential.user)
    return credential.user
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Google login failed'
    authStore.setError(message)
    throw error
  }
}

/**
 * Sign out the current user
 */
export async function logout(): Promise<void> {
  const authStore = useAuthStore()

  try {
    await signOut(auth)
    authStore.setUser(null)
  } catch (error) {
    console.error('Logout error:', error)
    throw error
  }
}

/**
 * Initialize auth state listener
 * Should be called once at app startup
 * @returns Unsubscribe function to remove the listener
 */
export function initAuthListener(): () => void {
  const authStore = useAuthStore()
  authStore.setInitializing()

  const unsubscribe = onAuthStateChanged(auth, (user) => {
    authStore.setUser(user)
  })

  return unsubscribe
}

/**
 * Get the current user synchronously (may be null if not yet initialized)
 */
export function getCurrentUser(): User | null {
  return auth.currentUser
}

/**
 * Wait for the auth state to be determined
 * Useful for navigation guards
 */
export function waitForAuth(): Promise<User | null> {
  return new Promise((resolve) => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      unsubscribe()
      resolve(user)
    })
  })
}
