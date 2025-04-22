<template>
    <div v-if="!is_tarif">
        <h1>Внимание! У вас нет активного тарифа функционал сервиса недоуступен!</h1>
    </div>
    <div v-else class="bg-gray-200 p-4 rounded-lg">
        <p class="text-lg font-bold">Вам достпно еще {{ available_menu }} новых сотрудников, согласно тарифу вы можете
            работать с {{ company_tarif.max_workers }} меню </p>
        <p class="text-gray-700">Для увеличения количества меню, необходимо приобрести расширение тарифа.</p>
    </div>
    <div class="p-6">
        <p class="mb-4 text-3xl font-bold">Ваши коллеги</p>
        <div class="flex flex-wrap">
            <div class="flex flex-wrap">
                <div v-for="(value, index) in workers_info" :key="index"
                    class="bg-white rounded-lg shadow-md p-4 flex items-center w-full">
                    <div class="flex flex-col" @click="$router.push('workers/' + value.id)">
                        <h2 class="text-lg font-medium">{{ value.name }} {{ value.second_name }} </h2>
                        <p class="text-gray-500">{{ value.contact_phone }}</p>
                        <p class="text-gray-500">{{ value.email }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Workers",
    props: {

    },
    data() {
        return {
            workers_info: {

            },
            company_tarif: {},
            errors: [],
        }
    },
    computed: {
        is_tarif() {
            return this.company_tarif?.tarif_date && new Date(this.company_tarif?.tarif_date) > Date.now()
        },
    },
    mounted() {
        this.get_tarif()
        this.get_user().then(() => {
            this.get_data()
        })
    },
    methods: {
        async get_data() {
            await axios
                .get("/api/v1/workers/get_workers/")
                .then(response => {
                    console.log(response)
                    this.workers_info = response.data
                })
                .catch(error => {

                    console.log(error)

                })
        },
        async get_user() {
            await axios
                .get("/api/v1/workers/0")
                .then(response => {
                    console.log(response)
                    this.worker = response.data
                    this.tarif = this.worker.company.tarif
                    this.company_id = this.worker.company.id


                })
                .catch(error => {
                    console.log(error)
                })
        },
        get_tarif() {
            console.log(this.$store.state)
            this.errors = []
            axios
                .get("/api/v1/tarif/" + this.$store.state.worker.company.tarif + '/')
                .then(response => {
                    this.company_tarif = response.data

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
    },

}
</script>
