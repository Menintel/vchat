import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import RoomsPage from '../views/RoomsPage.vue'
import CheckInPage from '../views/CheckInPage.vue'
import ChatPage from '../views/ChatPage.vue'

import { getAuth } from 'firebase/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
    },
    {
      path: '/rooms',
      name: 'rooms',
      component: RoomsPage,
      props: true,
    },
    {
      path: '/checkin/:hostID/:roomID',
      name: 'checkin',
      component: CheckInPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/chat/:hostID/:roomID',
      name: 'chat',
      component: ChatPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
    // This is a default path, if invalid path, go to home page
  ],
})

router.beforeEach(async (to) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

  return new Promise((resolve, reject) => {
    const unsubscribe = getAuth().onAuthStateChanged((user) => {
      unsubscribe() // Unsubscribe to prevent memory leaks

      if (requiresAuth && !user) {
        resolve('/login')
      } else {
        resolve() // Proceed with the navigation
      }
    }, reject)
  })
})

export default router
