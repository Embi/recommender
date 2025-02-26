import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api/v1/'
app.config.globalProperties.$axios = axios
app.config.globalProperties.$baseUrl = baseUrl

app.use(router)
app.mount('#app')
