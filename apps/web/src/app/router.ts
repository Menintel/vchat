import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router'
import { waitForAuth } from '@/firebase/auth'

// Lazy load pages for code splitting
const LoginPage = () => import('@/views/LoginPage.vue')
const RegisterPage = () => import('@/views/RegisterPage.vue')
const HomeView = () => import('@/views/HomeView.vue')
const AboutView = () => import('@/views/AboutView.vue')
const CheckInPage = () => import('@/views/CheckInPage.vue')
const ChatPage = () => import('@/views/ChatPage.vue')
const LobbyPage = () => import('@/pages/LobbyPage.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { guestOnly: true },
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: { guestOnly: true },
    },
    {
      path: '/rooms',
      name: 'rooms',
      component: LobbyPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/lobby',
      redirect: '/rooms',
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
  ],
})

// Navigation guard for authentication
router.beforeEach(async (to: RouteLocationNormalized) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const guestOnly = to.matched.some((record) => record.meta.guestOnly)

  let user
  try {
    user = await waitForAuth()
  } catch (error) {
    console.error('Authentication check failed:', error)
    // Decide on fallback behavior: allow navigation or redirect to error page
    return true // or return { name: 'login' }
  }

  // Redirect to login if auth required but not logged in
  if (requiresAuth && !user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Redirect to home if guest-only page but logged in
  if (guestOnly && user) {
    return { name: 'rooms' }
  }

  return true
})
export default router
