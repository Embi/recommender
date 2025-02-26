<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" type="email" placeholder="Enter your email" required>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post(
          `${this.$baseUrl}token/fake-token`,
          { email: this.email }
        )
        localStorage.setItem('token', response.data.token)
        this.$router.push('/main')
      } catch (error) {
        console.error('Login failed:', error)
        alert('Login failed')
      }
    }
  }
}
</script>
