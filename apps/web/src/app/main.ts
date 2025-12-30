import '../styles/design-system.css'
import '../assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faGoogle } from '@fortawesome/free-brands-svg-icons'
import {
  faDesktop,
  faMicrophone,
  faMicrophoneSlash,
  faPhone,
  faPodcast,
  faSignOutAlt,
  faTrash,
  faUser,
  faVideo,
  faVideoSlash,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createBootstrap } from 'bootstrap-vue-next'
import { createApp } from 'vue'
import App from '../App.vue'
import { initAuthListener } from '../firebase/auth'
import { pinia } from '../store'
import router from './router'

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
  faGoogle
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
