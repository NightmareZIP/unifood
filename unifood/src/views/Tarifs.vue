<template>
    <div>
        <p v-if="is_tarif" class="text-center text-3xl font-bold underline">Ваш тариф {{ company_tarif.name }} действует
            до
            {{ worker.company.tarif_date }}</p>
        <p v-else class="text-center text-3xl font-bold underline">У вас нет активного тарифа, функционал не доступен
        </p>
        <div class="flex flex-wrap justify-center mt-10">

            <div v-for="(item, index) in tarifs_data" class="max-w-sm rounded shadow-xl">
                <img class="h-1/4 w-full" :src="item.logo" alt="Image description">
                <div class="h-1/2 px-6 py-4">
                    <div class="font-bold text-xl mb-2">{{ item.name }}</div>
                    <p class="text-gray-700 text-base">
                        {{ item.description }}
                    </p>
                </div>
                <div v-if="is_head && item.id > tarif" class="relative bottom-1 pl-6 pt-4 pb-4">
                    <button @click="set_tarif(item.id, 12)"
                        class=" bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        {{ `Купить всего за ${item.price}!` }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Tarifs", props: {},
    data() {
        return {
            tarifs_data: {},
            company_tarif: {},
            errors: [],
            tarif: 0,
            company_id: 0,
            worker: {},
        }
    },
    mount() {

    },
    created() {
        this.get_data();
        this.get_user().then(res => {
            if (this.tarif) {
                this.get_tarif();
            }
        }
        )

    },
    computed: {
        is_head() { return this.$store.state.worker.is_head },
        is_tarif() {
            return this.company_tarif.tarif_date && new Date(this.company_tarif.tarif_date) > Date.now()
        },
    },

    methods: {
        async get_user() {
            await axios
                .get("/api/v1/workers/0")
                .then(response => {
                    this.worker = response.data
                    this.tarif = this.worker.company.tarif
                    this.company_id = this.worker.company.id


                })
                .catch(error => {
                    console.log(error)
                })
        },
        async get_data() {
            await axios.get("/api/v1/tarif/").then(response => {
                this.tarifs_data = response.data
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
        async get_tarif() {
            this.errors = []
            await axios
                .get("/api/v1/tarif/" + this.tarif + '/')
                .then(response => {
                    console.log(response)
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
        async set_tarif(tarif, months = 12) {
            this.errors = []
            await axios
                .patch("/api/v1/company-tarif/" + this.company_id + '/', { tarif: tarif, months: months })
                .then(async response => {
                    console.log(response);
                    this.tarif = response.data.tarif;
                    await this.get_tarif();

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
