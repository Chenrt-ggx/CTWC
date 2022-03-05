import App from '../App'
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/:id',
        name: 'home',
        component: App
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
