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
    <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
      <div class="text-xl lg:flex-grow lg:justify-center lg:flex">

        <span class="navbar"><router-link to="/company-register" v-if=!$store.state.isAuthenticated>Зарегестрировать
            компанию</router-link></span>
        <span class="navbar"><router-link to="/menu" v-if=$store.state.isAuthenticated>Меню</router-link></span>
        <span class="navbar"><router-link to="/my-profile" v-if=$store.state.isAuthenticated>Моя
            компания</router-link></span>
      </div>
      <div>

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
      let done = false
      axios
        .get("/api/v1/workers/0/")
        .then(response => {
          let worker = response.data
          this.$store.commit('setWorker', worker)
        })
        .catch(error => {
          console.log(error)
        })


    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
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
