// Подключение компонентов
import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import CompanyRegister from '../views/CompanyRegister.vue'
import HomeView from '../views/Home.vue'
import Tarifs from '../views/Tarifs.vue'
import MenuDetail from '../views/MenuDetail.vue'
import Menu from '../views/Menu.vue'

import Login from '../views/Login.vue'
import Profile from '../views/Profile.vue'
import CompanyInfo from '../views/CompanyInfo.vue'
import Workers from '../views/Workers.vue'
import ProfileMenu from '../views/ProfileMenu.vue'
import Orders from '../views/Orders.vue'
import UserOrder from '../views/UserOrder.vue'
// import { props } from 'stylus/lib/utils'

// Объявление объекта роутера
const routes = [
  {
    path: '/', //Задаем путь подлкючения
    name: 'home', //Задаем имя, для возможности простого поиска данной настрйоки 
    component: HomeView, //Задаем название компонента, который необходимо подключить
    meta: { requiresAuth: false }, // Помечаем, что для посещения страницы не нужна авторизация

  },


  {
    path: '/register/:companyid',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },

  {
    path: '/my-profile',
    name: 'my-profile',
    meta: { requiresAuth: true },

    component: ProfileMenu
  },
  {
    path: '/tarifs/',
    name: 'tarifs',
    component: Tarifs
  },
  {
    path: '/menu-items/:menu_id',
    name: 'menu-id',
    meta: { requiresAuth: true },
    component: MenuDetail,
    props: { orderMode: false }
  },
  {
    path: '/order-menu-items/:menu_id',
    name: 'order-menu-items-id',
    meta: { requiresAuth: false },
    component: MenuDetail,
    props: { orderMode: true }
  },
  {
    path: '/menu/',
    name: 'menu',
    meta: { requiresAuth: true },
    component: Menu
  },
  {
    path: '/orders/',
    name: 'orders',
    meta: { requiresAuth: true },
    component: Orders
  },
  {
    path: '/orders/:uuiid',
    name: 'orders-detail',
    meta: { requiresAuth: false },
    component: UserOrder
  },
  

  {
    path: '/order-menu/:id',
    name: 'order-menu-id',
    meta: { requiresAuth: false },
    props: { orderMode: true },
    component: MenuDetail,
  },

  {
    path: '/company-register',
    name: 'company-register',

    component: CompanyRegister
  },

  {
    path: '/workers/:id',
    name: 'profile',
    meta: { requiresAuth: true },

    component: Profile
  },

  {
    path: '/company-info',
    name: 'company-info',
    meta: { requiresAuth: true },

    component: CompanyInfo
  },
  {
    path: '/workers',
    name: 'workers',
    meta: { requiresAuth: true },

    component: Workers
  },

]

// Создаем объект роутера
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})


export default router
