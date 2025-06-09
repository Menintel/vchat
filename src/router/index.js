import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import RoomsPage from '../views/RoomsPage.vue'
import CheckInPage from '../views/CheckInPage.vue'

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
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
    // This is a default path, if invalid path, go to home page
  ],
})

export default router
