import { initializeApp, type FirebaseApp } from 'firebase/app'
import { getAuth, type Auth } from 'firebase/auth'
import { getFirestore, type Firestore } from 'firebase/firestore'

/**
 * Firebase configuration loaded from environment variables
 */
const firebaseConfig = {
  apiKey: "AIzaSyCWugE__f_fDjoS3TzVwZFTIki0C9FcuRk",
  authDomain: "vchat-ers.firebaseapp.com",
  projectId: "vchat-ers",
  storageBucket: "vchat-ers.firebasestorage.app",
  messagingSenderId: "504298001405",
  appId: "1:504298001405:web:b036f25bda1d3c6cefbf94"
};

// Initialize Firebase
let app: FirebaseApp
let auth: Auth
let db: Firestore

try {
  app = initializeApp(firebaseConfig)
  auth = getAuth(app)
  db = getFirestore(app)
} catch (error) {
  console.error('Firebase initialization error:', error)
  throw error
}

export { app, auth, db }
export default db
