import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import db from './db'
import { createBootstrap } from 'bootstrap-vue-next'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrash, faVideo, faUser } from '@fortawesome/free-solid-svg-icons'

library.add(faTrash, faVideo, faUser)
const app = createApp(App)

app.use(router)
app.use(createBootstrap)
app.provide('db', db)
app.mount('#app')
