import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import db from './db'
import * as io from 'socket.io-client'
import { getAuth } from 'firebase/auth'
import { createBootstrap } from 'bootstrap-vue-next'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrash, faVideo, faPodcast, faUser } from '@fortawesome/free-solid-svg-icons'

library.add(faTrash, faVideo, faUser, faPodcast)

const app = createApp(App)

app.use(createBootstrap)
app.provide('db', db)
window.io = io

getAuth().onAuthStateChanged(() => {
  app.use(router)
  app.mount('#app')
})
