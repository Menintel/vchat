import '../styles/design-system.css'
import '../assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'

import { createApp } from 'vue'
import App from '../App.vue'
import router from './router'
import { pinia } from '../store'
import { initAuthListener } from '../firebase/auth'
import { createBootstrap } from 'bootstrap-vue-next'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
  faTrash, 
  faVideo, 
  faPodcast, 
  faUser,
  faMicrophone,
  faMicrophoneSlash,
  faVideoSlash,
  faDesktop,
  faPhone,
  faSignOutAlt,
} from '@fortawesome/free-solid-svg-icons'
import { faGoogle } from '@fortawesome/free-brands-svg-icons'

// Add Font Awesome icons
library.add(
  faTrash, 
  faVideo, 
  faUser, 
  faPodcast,
  faMicrophone,
  faMicrophoneSlash,
  faVideoSlash,
  faDesktop,
  faPhone,
  faSignOutAlt,
  faGoogle,
)

const app = createApp(App)

// Use plugins
app.use(pinia)
app.use(createBootstrap())
app.use(router)

// Register global components
app.component('FontAwesomeIcon', FontAwesomeIcon)

// Initialize auth listener BEFORE mounting
initAuthListener()

// Mount the app
app.mount('#app')
