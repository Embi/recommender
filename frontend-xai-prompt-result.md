Here's a simple Vue.js frontend app that meets your requirements. I'll break it down into multiple files for better organization:

1. First, create a new Vue project (assuming you have Node.js installed):
```bash
npm create vue@latest
```
Follow the prompts to set up the project with Vue Router.

2. Here's the complete code structure:

`src/App.vue`:
```vue
<template>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'App'
}
</script>
```

`src/main.js`:
```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

app.config.globalProperties.$axios = axios
app.config.globalProperties.$baseUrl = 'http://<BASE_URL>/api/v1/'

app.use(router)
app.mount('#app')
```

`src/router/index.js`:
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import MainPage from '../views/MainPage.vue'
import CarDetail from '../views/CarDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/main',
    name: 'MainPage',
    component: MainPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/car/:id',
    name: 'CarDetail',
    component: CarDetail,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/')
  } else {
    next()
  }
})

export default router
```

`src/views/Login.vue`:
```vue
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
```

`src/views/MainPage.vue`:
```vue
<template>
  <div class="main-page">
    <h1>Car Recommendation System</h1>

    <section class="search">
      <h2>Search Cars</h2>
      <form @submit.prevent="searchCars">
        <input v-model="search.brand" placeholder="Brand">
        <input v-model.number="search.min_year" type="number" placeholder="Min Year">
        <input v-model.number="search.max_year" type="number" placeholder="Max Year">
        <input v-model.number="search.min_price" type="number" placeholder="Min Price">
        <input v-model.number="search.max_price" type="number" placeholder="Max Price">
        <input v-model="search.fuel" placeholder="Fuel">
        <button type="submit">Search</button>
      </form>

      <div v-if="searchResults.length">
        <h3>Search Results (Page {{ currentPage }})</h3>
        <div v-for="car in paginatedResults" :key="car.id" class="car-item" @click="viewDetail(car.id)">
          <span>{{ car.brand }} {{ car.name }} - {{ car.selling_price }}</span>
        </div>
        <button @click="currentPage--" :disabled="currentPage === 1">Previous</button>
        <button @click="currentPage++" :disabled="currentPage === totalPages">Next</button>
      </div>
    </section>

    <section class="recommendations">
      <h2>Recommended Cars</h2>
      <div v-for="car in recommendations.slice(0, 10)" :key="car.id" class="car-item" @click="viewDetail(car.id)">
        <span>{{ car.brand }} {{ car.name }} - {{ car.selling_price }}</span>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: {
        brand: '',
        min_year: null,
        max_year: null,
        min_price: null,
        max_price: null,
        fuel: ''
      },
      searchResults: [],
      recommendations: [],
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.searchResults.length / this.itemsPerPage)
    },
    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.searchResults.slice(start, end)
    }
  },
  created() {
    this.loadRecommendations()
  },
  methods: {
    async searchCars() {
      const params = new URLSearchParams(this.search).toString()
      try {
        const response = await this.$axios.get(
          `${this.$baseUrl}cars/search?${params}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
        )
        this.searchResults = response.data.listings
        this.currentPage = 1
      } catch (error) {
        console.error('Search failed:', error)
      }
    },
    async loadRecommendations() {
      try {
        const response = await this.$axios.get(
          `${this.$baseUrl}cars/recommendations`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
        )
        this.recommendations = response.data.recommended
      } catch (error) {
        console.error('Recommendations failed:', error)
      }
    },
    viewDetail(id) {
      this.$router.push(`/car/${id}`)
    }
  }
}
</script>

<style scoped>
.car-item { cursor: pointer; padding: 10px; border-bottom: 1px solid #ddd; }
.car-item:hover { background: #f5f5f5; }
</style>
```

`src/views/CarDetail.vue`:
```vue
<template>
  <div class="car-detail">
    <h1>Car Details</h1>
    <div v-if="car">
      <p><strong>Brand:</strong> {{ car.brand }}</p>
      <p><strong>Name:</strong> {{ car.name }}</p>
      <p><strong>Year:</strong> {{ car.year }}</p>
      <p><strong>Price:</strong> {{ car.selling_price }}</p>
      <p><strong>KM Driven:</strong> {{ car.km_driven }}</p>
      <p><strong>Fuel:</strong> {{ car.fuel }}</p>
      <p><strong>Seller Type:</strong> {{ car.seller_type }}</p>
      <p><strong>Transmission:</strong> {{ car.transmission }}</p>
      <p><strong>Owner:</strong> {{ car.owner }}</p>
    </div>
    <button @click="$router.push('/main')">Back to Main</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      car: null
    }
  },
  async created() {
    await this.loadCarDetails()
  },
  methods: {
    async loadCarDetails() {
      try {
        const response = await this.$axios.get(
          `${this.$baseUrl}cars/detail/${this.$route.params.id}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
        )
        this.car = response.data
      } catch (error) {
        console.error('Failed to load car details:', error)
      }
    }
  }
}
</script>
```

To use this app:

1. Install dependencies:
```bash
npm install
npm install axios
```

2. Replace `<BASE_URL>` in `main.js` with your actual API base URL.

3. Run the app:
```bash
npm run dev
```

This implementation includes:
- Login page with email-based authentication
- Main page with search and recommendations sections
- Search functionality with pagination (10 items per page)
- Recommendations showing first 10 items
- Car detail page
- Token-based authentication for all API calls
- Basic routing with authentication guard
- Simple styling (you can enhance this further)

The app assumes the API endpoints work as specified. You might need to:
- Adjust the API response handling based on actual response structures
- Add error handling for various scenarios
- Enhance the styling
- Add loading states
- Add form validation

Let me know if you need any clarification or have questions about specific parts!
