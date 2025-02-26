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
      // Create a new object with only non-null/empty values
      const filteredSearch = Object.fromEntries(
        Object.entries(this.search).filter(([_, value]) =>
          value !== null && value !== '' && value !== undefined
        )
      )

      const params = new URLSearchParams(filteredSearch).toString()
      try {
        const response = await this.$axios.get(
          `${this.$baseUrl}cars/search${params ? '?' + params : ''}`,
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
