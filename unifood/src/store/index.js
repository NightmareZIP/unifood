import { createStore } from 'vuex'

export default createStore({
  //Создаем хранилище с именем state
  state: {
    user: {
      id: '',
      username: '',
    },
    isAuthenticated: false,
    token: '',
    worker: {},
  },
  getters: {
  },
  mutations: {
    //Любое измененеие хранила реализуется через специальные методы мутаций
    //Инициализация хранилища, проверяем, есть ли в sessionStorage информация о токене
    initializeStore(state) {
      if (sessionStorage.getItem('token')) {
        state.token = sessionStorage.getItem('token')
        state.isAuthenticated = true
        state.user.username = sessionStorage.getItem('username')
        state.user.id = sessionStorage.getItem('userid')
      } else {
        state.user.id = ''
        state.user.username = ''
        state.token = ''
        state.isAuthenticated = false
      }
      state.worker = {}

    },
    //Установка токена
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    // Установка данных работник
    setWorker(state, worker) {
      state.worker = worker

    },
    //Удаление токена
    removeToken(state) {
      state.user.id = ''
      state.user.username = ''
      state.token = ''
      state.isAuthenticated = false
    },
    //Установка минимальной информации пользователя
    setUser(state, user) {
      state.user = user
    },
  },
  actions: {
  },
  modules: {
  }
})
