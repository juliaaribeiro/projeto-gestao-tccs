import { createApp } from 'vue'
import App from './App.vue'
import TopBar from './components/TopBar.vue'
import router from './router'
import './styles.css'

const app = createApp(App)
app.component('TopBar', TopBar)
app.use(router)
app.mount('#app')
