<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">

        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <h1 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">{{ header }}</h1>
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
                        <input disabled type="text" name="name" class="input" v-model="user_info.name">
                    </div>
                </div>
                <div>
                    <label class="label">Фамилия</label>
                    <div class="control">
                        <input :disabled="!canEdit" type="text" name="last_name" class="input"
                            v-model="user_info.last_name">
                    </div>
                </div>
                <div>
                    <label class="label">Отчество</label>
                    <div class="control is-horizontal">
                        <input :disabled="!canEdit" type="text" name="surname" class="input"
                            v-model="user_info.surname">
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
                        <input :disabled="!canEdit" type="tel" name="contact_phone" class="input"
                            v-model="user_info.contact_phone">
                    </div>
                </div>
                <div>
                    <label class="label">Страна</label>
                    <div class="control">
                        <input :disabled="!canEdit" type="text" name="country" class="input"
                            v-model="user_info.country">
                    </div>
                </div>
                <div class="notification is-danger" v-if="error">
                    <p>Убедитесь, что поля заоплнены корректно</p>
                </div>
                <button v-if="canEdit"
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
            user_info: {
                company: {
                    name: '',
                }
            },
            is_head: false,
            company_id: 0,
            id: 0,
            errors: [],
        }
    },
    computed: {
        header() {
            if (this.id == this.$route.params.id) {
                return 'Ваши данные'
            }
            return `Данные сотрудника ${this.user_info.name} ${this.user_info.last_name} ${this.user_info.surname}`
        },
        canEdit() {
            return this.is_head || this.id == this.$route.params.id
        }
    },
    created() {
        this.get_data()
        this.get_user()
    },
    methods: {
        async get_data() {
            await axios
                .get("/api/v1/workers/"+this.$route.params.id+'/')
                .then(response => {
                    console.log(response)
                    this.user_info = response.data

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
                    this.user_info = response.data

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
        async get_user() {
            await axios
                .get("/api/v1/workers/0/")
                .then(response => {
                    this.company_id = response.data.company.id
                    this.id = response.data.id
                    console.log(response.data.head == null)
                    this.is_head = response.data.head == null
                })
                .catch(error => {
                    console.log(error)
                })
        },
    },
}
</script>
