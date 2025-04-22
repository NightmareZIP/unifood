<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img class="size-24 mx-auto" src="../assets/unifood.png" alt="Unifood">
            <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Введите данные для
                регистрации</h2>
        </div>

        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">

            <form @submit.prevent="submitForm" class="space-y-6">
                <div>
                    <label class="label">Ваш E-mail</label>
                    <div class="control">
                        <input type="email" name="username" class="input" v-model="username">
                    </div>
                </div>

                <div>
                    <label class="label">Пароль</label>
                    <div class="control">
                        <input type="password" name="password" class="input" v-model="password">
                    </div>
                </div>

                <div>
                    <label class="label">Имя</label>
                    <div class="control">
                        <input type="text" name="name" class="input" v-model="name">
                    </div>
                </div>
                <div>

                    <label class="label">Фамилия</label>
                    <div class="control">
                        <input type="text" name="last_name" class="input" v-model="last_name">
                    </div>
                </div>
                <div>

                    <label class="label">Отчество</label>
                    <div class="control">
                        <input type="text" name="surname" class="input" v-model="surname">
                    </div>
                </div>
                <div>
                    <label class="label">Телефон</label>
                    <div class="control">
                        <input type="tel" name="contact_phone" class="input" v-model="contact_phone">
                    </div>
                </div>
                <div>
                    <label class="label">Страна</label>
                    <div class="control">
                        <input type="text" name="country" class="input" v-model="country">
                    </div>
                </div>
                <!-- Данные компании -->
                <div>
                    <label class="label">Название компании</label>
                    <div class="control">
                        <input type="text" name="cmp_name" class="input" v-model="company_data.name">
                    </div>
                </div>

                <div>
                    <label class="label">Страна Компании</label>
                    <div class="control">
                        <input type="text" name="cmp_country" class="input" v-model="company_data.country">
                    </div>
                </div>

                <div>
                    <label class="label">Адрес</label>
                    <div class="control">
                        <input type="text" name="place" class="input" v-model="company_data.place">
                    </div>
                </div>

                <div>
                    <label class="label">Представитель</label>
                    <div class="control">
                        <input type="text" name="contact_person" class="input" v-model="company_data.contact_person">
                    </div>
                </div>

                <div>
                    <label class="label">Контактный телефон</label>
                    <div class="control">
                        <input type="text" name="contact_phone" class="input" v-model="company_data.contact_phone">
                    </div>
                </div>

                <div>
                    <label class="label">Контактный e-mail</label>
                    <div class="control">
                        <input type="text" name="cmp_email" class="input" v-model="company_data.email">
                    </div>
                </div>
                <div>
                    <label class="label">ИНН</label>
                    <div class="control">
                        <input type="text" name="inn" class="input" v-model="company_data.inn">
                    </div>
                </div>


                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">
                        {{ error }}
                    </p>
                </div>

                <div>
                    <button type="submit"
                        class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-outline-amber-500">Войти</button>
                </div>
            </form>

            <hr>

            <router-link to="/login">Нажмите чтобы войти в сущетсвующий аккаунт</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'CompanyRegister',
    data() {
        return {
            username: '',
            password: '',
            name: '',
            last_name: '',
            surname: '',
            contact_phone: '',
            country: '',
            company_data: {
                name: '',
                country: '',
                place: '',
                contact_person: '',
                contact_phone: '',
                email: '',
                inn: '',
            },
            errors: []
        }
    },
    methods: {
        async submitForm(e) {
            axios.defaults.headers.common["Authorization"] = ""
            sessionStorage.removeItem("token")
            this.errors = []
            const userData = {
                name: this.name,
                last_name: this.last_name,
                surname: this.surname,
                email: this.username,
                contact_phone: this.contact_phone,
                country: this.country,
                company: this.company_data,
                username: this.username,
                password: this.password,
            }
            //Создаем самого работника
            await axios
                .post("/api/v1/workercompany/", userData)
                .then(response => {
                    console.log(response)

                })
                .catch(error => {
                    console.log("ERROR")
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
            await axios
                .post("/api/v1/token/login/", userData)
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
</script>