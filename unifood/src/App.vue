<template>
  <!-- Выводим элементы навигации роутера, так же проверяем, аторизован ли пользователь для отобра
  жения каждого из элементов -->
  <nav class="flex items-center justify-between flex-wrap bg-amber-600 p-6">
    <div class="flex-col items-center flex-shrink-0 text-white mr-6">
      <div class="font-semibold tracking-down">
        Unifood - eat it
      </div>
      <div><a href="/"><img class="size-20" src="./assets/unifood.png" alt="unifood"></a></div>
    </div>
    <div class="block lg:hidden">
      <button
        class="flex items-center px-3 py-2 border rounded text-border-red-50 border-red-50 hover:text-white hover:border-white">
        <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
          <title>Меню</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
        </svg>
      </button>
    </div>
    <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
      <div class="text-xl lg:flex-grow lg:justify-center lg:flex">

        <span class="navbar"><router-link to="/company-register" v-if=!$store.state.isAuthenticated>Зарегестрировать
            компанию</router-link></span>
        <span class="navbar"><router-link to="/menu" v-if=$store.state.isAuthenticated>Меню</router-link></span>
        <span class="navbar"><router-link to="/orders" v-if=$store.state.isAuthenticated>Заказы</router-link></span>

      </div>
      <div>
        <span
          class="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-red-50 hover:bg-white mt-4 lg:mt-0"><router-link
            to="/my-profile" v-if=$store.state.isAuthenticated>Моя
            компания</router-link></span>

        <span class="navbar"><router-link id='logout' @click="logout" to=''
            v-if=$store.state.isAuthenticated>Выйти</router-link></span>
        <span class="navbar"><router-link to="/login"
            v-if=!$store.state.isAuthenticated>Авторизоваться</router-link></span>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<script>
import axios from 'axios'
// Прописываем информаию о комопненте и логику его работы
export default {
  //Имя комопнента
  name: 'App',
  //Логика выполняемая перед созданием компонента при его вызове
  beforeCreate() {
    //Инициализируем хранилища приложения
    this.$store.commit('initializeStore')
    //Получаем токен авторизации их хранилища браузера
    const token = this.$store.state.token
    if (token) {
      //Если токен существует, то записываем это в данные хранилища, и передаем его в axios
      // по умолчанию при отправке запросов
      axios.defaults.headers.common['Authorization'] = "Token " + token
      // Шлем запрос для получения информации о сотруднике и так же записывае информацию в хранилище
      axios
        .get("/api/v1/workers/")
        .then(response => {
          console.log(response)
          let worker = response.data[0]
          this.$store.commit('setWorker', worker)
          // this.$router.push('/login')
        })
        .catch(error => {
          console.log(error)
        })
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
    // console.log(this.$store);
    // console.log(Object.values(this.$store.state.user));
  },
  methods: {
    //Прописываем метод для разавторизации пользователя
    logout() {
      //Передаем на сервер, что мы выходим из учетной записи и токен должен стать неактивным
      axios
        .post("/api/v1/token/logout/")
        .then(response => {
          //Очищаем информацию о токене на стороне пользователя
          axios.defaults.headers.common["Authorization"] = ""
          sessionStorage.removeItem("username")
          sessionStorage.removeItem("userid")
          sessionStorage.removeItem("token")
          this.$store.commit('removeToken')
          this.$router.push('/')
        })
        .catch(error => {
          if (error.response) {
            console.log(JSON.stringify(error.response.data))
          } else if (error.message) {
            console.log(JSON.stringify(error.message))
          } else {
            console.log(JSON.stringify(error))
          }
        })
    }
  }
}
</script>
<!-- Подключаем стили -->
<style>
/* @import "../node_modules/bulma"; */


#logout {
  color: #2c3e50;
}
</style>
