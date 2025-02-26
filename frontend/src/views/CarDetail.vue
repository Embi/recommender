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
