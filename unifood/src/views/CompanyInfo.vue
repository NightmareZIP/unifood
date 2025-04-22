<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">

        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img class="size-24 mx-auto" src="../assets/unifood.png" alt="Unifood">
            <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Данные компании</h2>
        </div>
        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6" @submit.prevent="submitForm">

                <div>
                    <label class="label">Название компании</label>

                    <div class="control">
                        <input :disabled="!is_head" type="text" name="cmp_name" class="input"
                            v-model="company_data.name">
                    </div>

                </div>
                <div>
                    <label class="label">Страна Компании</label>

                    <div class="control">
                        <input :disabled="!is_head" type="text" name="cmp_country" class="input"
                            v-model="company_data.country">
                    </div>

                </div>
                <div>
                    <label class="label">Адрес</label>

                    <input :disabled="!is_head" type="text" name="place" class="input" v-model="company_data.place">

                </div>
                <div>
                    <label class="label">Представитель</label>

                    <div class="control is-horizontal">
                        <input :disabled="!is_head" type="text" name="contact_person" class="input"
                            v-model="company_data.contact_person">
                    </div>

                </div>
                <div>
                    <label class="label">Контактный телефон</label>

                    <div class="control is-horizontal">
                        <input :disabled="!is_head" type="text" name="contact_phone" class="input"
                            v-model="company_data.contact_phone">
                    </div>

                </div>
                <div>
                    <label class="label">Контактный e-mail</label>
                    <div class="control is-horizontal">
                        <input :disabled="!is_head" type="text" name="cmp_email" class="input"
                            v-model="company_data.email">
                    </div>
                </div>
                <div>
                    <div class="field-label">
                        <label class="label">ИНН</label>
                    </div>
                    <div class="control">
                        <input :disabled="!is_head" type="text" name="inn" class="input" v-model="company_data.inn">
                    </div>
                </div>
                <div class="notification is-danger" v-if="error">
                    <p>Убедитесь, что поля заоплнены корректно</p>
                </div>
                <button v-if="is_head" @click="save"
                    class="flex w-full justify-center rounded-md bg-amber-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-amber-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-outline-amber-500">Сохранить</button>

            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "CompanyInfo", props: {}, data() {
        return {
            company_data: {
                "name": "", "country": "", "place": ""
                , "contact_person": "", "contact_phone": "", "email": "", "inn": "", "head": {
                    "id": ''
                    , "name": "", "last_name": "", "surname": "", "email": "", "contact_phone": "", "country"
                        : "", "created_at": "", "user_id": '', "head": '', "company": ''
                }
            }, errors: [],
        }
    },
    computed: { is_head() { return this.$store.state.worker.is_head } }, created() { this.get_data() },
    methods: {
        async get_data() {
            await axios.get("/api/v1/company/").then(response => {
                console.log(response)
                this.company_data = response.data[0]

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
                .put("/api/v1/company/" + this.company_data.id + '/', this.company_data)
                .then(response => {
                    console.log(response)
                    this.company_data = response.data[0]

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
