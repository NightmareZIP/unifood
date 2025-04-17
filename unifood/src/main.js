import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import './style.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000'
createApp(App).use(store).use(router).mount('#app')

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.state.isAuthenticated) {
            next({ name: 'login' })
        } else {
            next()
        }
    } else {
        next()
    }
})