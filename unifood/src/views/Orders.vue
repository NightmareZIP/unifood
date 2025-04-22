<template>
    <h1 v-if="!is_tarif">Внимание! У вас нет активного тарифа функционал сервиса недоуступен!</h1>
    <div v-else class="w-full flex flex-wrap justify-start mt-10 p-8 flex-col">
        <div v-for="(items, key) in items_data" class="">
            <p class="text-gray-500 text-lg font-bold">{{ translateStatus(key) }}</p>
            <div class="flex flex-wrap">
                <OrderCard v-for="(item, index) in items" :headText=item.id :customer_name=item.customer_name
                    :custumer_phone=item.custumer_phone :uuid=item.uuid />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import OrderCard from "../components/OrderCard.vue";

export default {
    components: { OrderCard },
    name: "Order",
    props: {

    },
    data() {
        return {
            company_tarif: {},
            errors: [],
            tarif: 0,
            worker: {},
            items_data: {},
            showPopup: false,
            item_info: {},
            is_new: true,
            count: 0,
            unsorted_data: [],
            cart: {},
            showOrderPopup: false,
        }
    },
    mounted() {
        this.get_data();
        this.get_user().then(res => {
            if (this.tarif) {
                this.get_tarif();
            }
        })
    },
    computed: {
        is_head() { return this.$store.state.worker.is_head },

        is_tarif() {
            return this.company_tarif.tarif_date && new Date(this.company_tarif.tarif_date) > Date.now()
        },


    },

    methods: {
        //Вынести в отдельную либу?
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
        async get_data() {
            await axios.get("/api/v1/orders/?menu=" + Number(this.$route.query.menu), {

            }).then(response => {
                this.items_data = {
                    'new': [],
                    'ready': [],
                    'cancel': [],
                    'reject': [],
                }
                this.unsorted_data = response.data
                for (let key in response.data) {
                    let item = response.data[key]
                    if (!(item.status in this.items_data)) {
                        this.items_data[item.status] = [item]
                    }
                    else {
                        this.items_data[item.status].push(item)
                    }
                }
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
        translateStatus(status) {
            let statuses = {
                'new': 'Новые заказы',
                'ready': 'Завершенные заказы',
                'cancel': 'Отмененные заказы',
                'reject': 'Отклоненные заказы',

            }
            return statuses[status]
        }
    },
}
</script>
