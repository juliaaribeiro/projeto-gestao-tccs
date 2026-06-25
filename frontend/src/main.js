import { createApp } from 'vue'
import App from './App.vue'
import TopBar from './components/TopBar.vue'
import router from './router'
import './styles.css'

const savedTheme = localStorage.getItem('tcc-theme') || 'light'
document.documentElement.setAttribute('data-theme', savedTheme)

const app = createApp(App)
app.component('TopBar', TopBar)
app.use(router)
app.mount('#app')
