<template>
  <form class="mt-5" @submit.prevent="register">
    <div class="row justify-content-center">
      <div class="card bg-light p-4 mx-5">
        <div class="card-body">
          <h3 class="card-title text-center mb-4">Register</h3>
          <div class="alert alert-danger mb-3" v-if="error">{{ error }}</div>
          <div class="form-group mb-3">
            <label class="form-label" for="userName">User Name</label>
            <input
              type="text"
              id="userName"
              class="form-control"
              placeholder="Enter your user name"
              v-model="userName"
              required
            />
          </div>
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
            <label class="form-label" for="password1">Password</label>
            <input
              type="password"
              id="password1"
              class="form-control"
              placeholder="Enter your password"
              v-model="password1"
              required
            />
          </div>
          <div class="form-group mb-3">
            <label class="form-label" for="password2">Confirm Password</label>
            <input
              type="password"
              id="password2"
              class="form-control"
              placeholder="Confirm your password"
              v-model="password2"
              required
            />
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-lg">Register</button>
          </div>
          <div class="d-grid gap-2">
            <p>Already have an account? <RouterLink to="/login" class="link">Log In</RouterLink></p>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import { getAuth, createUserWithEmailAndPassword, updateProfile } from 'firebase/auth'

export default {
  data() {
    return {
      userName: null,
      email: null,
      password1: null,
      password2: null,
      error: null,
    }
  },
  methods: {
    async register() {
      this.error = null
      if (!this.email || !this.password1 || !this.userName) {
        this.error = 'Please enter an email and password and username'
        return
      }
      if (this.password1 !== this.password2) {
        this.error = 'Passwords do not match'
        return
      }
      const auth = getAuth()

      try {
        const userCredential = await createUserWithEmailAndPassword(
          auth,
          this.email,
          this.password1,
        )
        const user = userCredential.user

        await updateProfile(user, {
          displayName: this.userName,
        })

        console.log('Registered as', user.email)

        // Redirect only after successful registration
        this.$router.push('/')
      } catch (error) {
        console.error('Error registering:', error)

        if (error.code === 'auth/email-already-in-use') {
          this.error = 'Email already in use'
        } else if (error.code === 'auth/invalid-email') {
          this.error = 'Invalid email'
        } else if (error.code === 'auth/weak-password') {
          this.error = 'Weak password'
        } else {
          this.error = 'Failed to register. Please try again.'
        }
      }
    },
  },
}
</script>
