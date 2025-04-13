<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">

        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <h1 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Ваши данные</h1>
        </div>
        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form @submit.prevent="submitForm" class="space-y-6">

                <div>
                    <label class="label">E-mail</label>
                    <div class="control">
                        <input disabled readonly="readonly" type="email" name="username" class="input"
                            v-model="user_info.email">
                    </div>
                </div>
                <div>
                    <label class="label">Имя</label>
                    <div class="control">
                        <input type="text" name="name" class="input" v-model="user_info.name">
                    </div>
                </div>
                <div>
                    <label class="label">Фамилия</label>
                    <div class="control">
                        <input type="text" name="last_name" class="input" v-model="user_info.last_name">
                    </div>
                </div>
                <div>
                    <label class="label">Отчество</label>
                    <div class="control is-horizontal">
                        <input type="text" name="surname" class="input" v-model="user_info.surname">
                    </div>
                </div>
                <div>
                    <label class="label">Компания</label>
                    <div class="control is-horizontal">
                        <input disabled readonly="readonly" type="text" name="surname" class="input"
                            v-model="user_info.company.name">
                    </div>
                </div>
                <div>
                    <label class="label">Телефон</label>
                    <div class="control">
                        <input type="tel" name="contact_phone" class="input" v-model="user_info.contact_phone">
                    </div>
                </div>
                <div>
                    <label class="label">Страна</label>
                    <div class="control">
                        <input type="text" name="country" class="input" v-model="user_info.country">
                    </div>
                </div>
                <div class="notification is-danger" v-if="error">
                    <p>Убедитесь, что поля заоплнены корректно</p>
                </div>
                <button
                    class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-outline-amber-500"
                    @click="save">Сохранить</button>

            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Profile",
    props: {
        data: Object
    },
    data() {
        return {
            user_info: {},
            errors: [],
        }
    },
    computed: {

    },
    created() {
        this.get_data()
    },
    methods: {
        async get_data() {
            await axios
                .get("/api/v1/workers/")
                .then(response => {
                    console.log(response)
                    this.user_info = response.data[0]
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
        },
        async save() {
            this.errors = []
            await axios
                .put("/api/v1/workers/" + this.user_info.id + '/', this.user_info)
                .then(response => {
                    console.log(response)
                    this.user_info = response.data[0]
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

        }
    },
}
</script>
