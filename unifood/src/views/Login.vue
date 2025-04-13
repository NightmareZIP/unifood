<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img class="size-24 mx-auto" src="../assets/unifood.png" alt="Unifood">
            <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Войдите в аккаунт</h2>
        </div>

        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form @submit.prevent="submitForm" class="space-y-6" action="#" method="POST">
                <div>
                    <label for="email" class="block text-sm/6 font-medium text-gray-900">Email</label>
                    <div class="mt-2">
                        <input type="email" name="username" id="email" autocomplete="email" required v-model="username"
                            class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-outline-amber-500 sm:text-sm/6">
                    </div>
                </div>

                <div>
                    <div class="flex items-center justify-between">
                        <label for="password" class="block text-sm/6 font-medium text-gray-900">Пароль</label>
                    </div>

                    <div class="mt-2">
                        <input v-model="password" type="password" name="password" id="password"
                            autocomplete="current-password" required
                            class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-amber-500 sm:text-sm/6">
                    </div>
                </div>
                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
                <div>
                    <button type="submit"
                        class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-outline-amber-500">Войти</button>
                </div>
                <div
                    class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-outline-amber-500">
                    <router-link to="/sign-up">Зарегестрироваться</router-link>
                </div>
            </form>
        </div>
    </div>
    <!-- 
    <div class="page-login">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Авторизация</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>E-mail</label>
                        <div class="control">
                            <input type="email" name="username" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Войти</button>
                        </div>
                    </div>
                </form> 

                <hr>

                <router-link to="/sign-up">Зарегестрироваться</router-link>
            </div>
        </div>
    </div>-->
</template>

<script>
import axios from 'axios'
export default {
    name: 'LogIn',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    methods: {
        async submitForm(e) {
            axios.defaults.headers.common["Authorization"] = ""
            sessionStorage.removeItem("token")
            const formData = {
                username: this.username,
                password: this.password
            }
            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)

                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    sessionStorage.setItem("token", token)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })
            axios
                .get("/api/v1/users/me")
                .then(response => {
                    this.$store.commit('setUser', { 'username': response.data.username, 'id': response.data.id })
                    sessionStorage.setItem('username', response.data.username)
                    sessionStorage.setItem('userid', response.data.id)
                    this.$router.push('/')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    }
}
</script>