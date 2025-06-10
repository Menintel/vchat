<template>
  <form class="mt-5" @submit.prevent="login">
    <div class="row justify-content-center">
      <div class="card bg-light p-4 mx-5">
        <div class="card-body">
          <h3 class="card-title text-center mb-4">Welcome Back</h3>
          <div class="alert alert-danger mb-3" v-if="error">{{ error }}</div>
          <div class="form-group mb-3">
            <label class="form-label" for="email">Email</label>
            <input
              type="email"
              id="email"
              class="form-control"
              placeholder="Enter your email"
              v-model="email"
              required
            />
          </div>
          <div class="form-group mb-3">
            <label class="form-label" for="password">Password</label>
            <input
              type="password"
              id="password"
              class="form-control"
              placeholder="Enter your password"
              v-model="password"
              required
            />
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-lg">Login</button>
          </div>
          <div class="d-grid gap-2">
            <p>
              Don't have an account? <RouterLink to="/register" class="link">Register</RouterLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'

export default {
  data() {
    return {
      email: null,
      password: null,
      error: null,
    }
  },
  methods: {
    async login() {
      this.error = null
      if (!this.email || !this.password) {
        this.error = 'Please enter an email and password'
        return
      }
      const auth = getAuth()

      try {
        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password)
        const user = userCredential.user
        console.log('Logged in as', user.email)

        // Redirect only after successful login
        this.$router.push('/rooms')
      } catch (error) {
        console.error('Error logging in:', error)
        this.error = 'Failed to log in. Please try again.'
      }
    },
  },
}
</script>
