<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Регистрация сотрудника</h2>
        </div>
        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">

            <form @submit.prevent="submitForm" class="space-y-6">
                <div>
                    <label for="email" class="label">Email</label>
                    <div class="mt-2">
                        <input type="email" name="username" id="email" autocomplete="email" required v-model="username"
                            class="input">
                    </div>
                </div>

                <div>
                    <label class="label">Пароль</label>
                    <div class="mt-2">
                        <input type="password" name="password" class="input" v-model="password">
                    </div>
                </div>

                <div>
                    <label class="label">Имя</label>
                    <div class="mt-2">
                        <input type="text" name="name" class="input" v-model="name">
                    </div>
                </div>
                <div>

                    <label class="label">Фамилия</label>
                    <div class="mt-2">
                        <input type="text" name="last_name" class="input" v-model="last_name">
                    </div>
                </div>
                <div>

                    <label class="label">Отчество</label>
                    <div class="mt-2">
                        <input type="text" name="surname" class="input" v-model="surname">
                    </div>
                </div>
                <div>
                    <label class="label">Телефон</label>
                    <div class="mt-2">
                        <input type="tel" name="contact_phone" class="input" v-model="contact_phone">
                    </div>
                </div>
                <div>
                    <label class="label">Страна</label>
                    <div class="mt-2">
                        <input type="text" name="country" class="input" v-model="country">
                    </div>
                </div>

                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
                <div>
                    <button type="submit"
                        class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-outline-amber-500">
                        {{enterText}}</button>
                </div>
            </form>

            <hr>

            <router-link v-if="!is_head" to="/login">Войти в сущетсвующий аккаунт</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Register',
    data() {
        return {
            username: '',
            password: '',
            name: '',
            last_name: '',
            surname: '',
            contact_phone: '',
            country: '',
            company: Number(this.$route.params.companyid),
            errors: [],
            is_head: this.$store.state.worker?.is_head
        }
    },
    computed: {
        enterText() {
            return this.is_head ? "Зарегистрировать сотрудника" : "Зарегистрироваться"
        }
    },
    methods: {
        async submitForm(e) {
            axios.defaults.headers.common["Authorization"] = ""
            sessionStorage.removeItem("token")
            this.errors = []
            const formData = {
                username: this.username,
                password: this.password
            }

            let user_id = 0;
            //Создаем django пользователя (поля логин и пароль)
            await axios
                .post("/api/v1/users/", formData)
                .then(response => {
                    console.log(response)
                    user_id = response.data.id

                    // this.$router.push('/login')
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
            console.log('ID ' + user_id)
            //авторизируемся, нужно для записи других данных
            if (!this.is_head) {
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
            }
            const userData = {
                user_id: user_id,
                name: this.name,
                last_name: this.last_name,
                surname: this.surname,
                email: this.username,
                contact_phone: this.contact_phone,
                country: this.country,
                company: this.$route.params.companyid,
            }
            //Создаем самого работника
            await axios
                .post("/api/v1/workers/", userData)
                .then(response => {
                    console.log(response)

                })
                .catch(error => {
                    console.log("ERROR")
                    const deliting = {
                        current_password: formData.password
                    }
                    //В случае неудачи удаляем пользователя django 
                    axios
                        .delete("/api/v1/users/me", { data: deliting, headers: { "Authorization": "Token " + sessionStorage.getItem("token") } })
                        .then(response => {
                            console.log(response)
                            // this.$router.push('/login')
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
                    throw "Oops"
                })
            if (!this.is_head) {
                await axios
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
}
</script>