<template>

    <div class="flex flex-col w-full">
        <div v-for="(item, key) in order.menu_items" class="p-2 flex items-center  justify-between mb-4 border-1">
            <img class="w-16 h-16 object-cover rounded mr-4" :src="item.image" :alt="item.name">
            <div class="flex flex-left flex-grow flex-1">
                <div>
                    <p class="mr-2  text-nowrap md:text-lg font-medium">{{ item.name }}</p>
                    <p class="mr-2 text-xs text-gray-500">Комментарий: {{ item.user_comment }}</p>
                </div>
            </div>
            <div class="flex flex-col">
                <div class="flex">
                    <button v-if="!is_exist" @click="decrease(item)"
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-2 rounded mr-2">
                        -
                    </button>
                    <input :disabled="is_exist"  :value="item.amount" @input="set_amount(itemt, $event.target.value)"
                        class="w-auto sm:w-full text-3xl border font-bold sm:font-normal sm:text-sm border-gray-400 rounded px-2 py-2 mr-2 text-center"
                        type="text">
                    <button v-if="!is_exist" @click="increase(item)"
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-2 rounded">
                        +
                    </button>
                </div>
                <p class=" mr-2 text-sm md:text-lg md:font-bold ">{{ item.discount_price }} x {{ item.amount }}
                    шт. {{
                    item.discount_price *
                    item.amount }} руб.</p>
            </div>
        </div>
        <input :disabled="is_exist" type="text" v-model="order.customer_name" placeholder="Ваше имя"
            class="mt-2 w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
        <input :disabled="is_exist" type="text" v-model="order.custumer_phone" placeholder="Ваш телефон"
            class="mt-2 w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />

        <textarea :disabled="is_exist" rows="4" v-model="order.customer_comment"
            placeholder="Комментарий к заказу" class="text-3xl mt-6 mb-6 w-auto text-gray-900 sm:text-4xl"></textarea>
        <div class="p-2 flex items-center justify-between mb-4">
            <p class="">Итого: {{ total }}</p>
            <button v-if="total>0" @click="save" type="submit"
                class="mt-6 flex items-center justify-center rounded-md border border-transparent bg-green-600 px-8 py-3 text-base font-medium text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-hidden">Создать
                заказ</button>
        </div>
    </div>


</template>

<script>

import axios from 'axios'

export default {
    name: "OrderDetail",
    props: {
        order: {
            menu_items: {},
            menu: Number,
            uuid: String,
            customer_comment: '',
            customer_name: '',
            custumer_phone: '',
        },
        // menu: null,
        // uuid: null,
    },
    data() {
        return {
            // customer_comment: '',
            // customer_name: '',
            // custumer_phone: '',
        }
    },
    mounted() {

    },
    computed: {
        is_head() {
            return this.$store.state.worker.is_head
        },
        total() {
            let total = 0
            for (let item in this.order.menu_items) {
                console.log(item)
                total += this.order.menu_items[item].discount_price * this.order.menu_items[item].amount
            }
            return total
        },
        is_exist() {
            // console.log(this.order.uuid)
            return this.order.uuid?.length
        }
    },
    methods: {
        set_amount(item, amount) {
            try {
                if (!isNaN(amount)) {
                    console.log(amount)

                    item.amount = Number(amount)
                }
                else {
                    item.amount = 1
                }
            }
            catch (e) {
                item.amount = 1
            }
        },

        close() {
            this.$emit('close')
        },
        increase(item) {
            item.amount += 1;
        },
        decrease(item) {
            if (item.amount > 0) {
                item.amount -= 1;
            }
        },

        async save() {
            let url = '/api/v1/orders-user/'
            let sending_data = {}
            if (this.order.uuid) {
                url = '/api/v1/orders/' + sending_data.uuid + '/'
                await axios
                    .put(url, sending_data, {
                    })
                    .then(response => {
                        this.router.push()
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
                }
                else {
                sending_data = { menu_items: Object.values(this.order.menu_items) }
                for (let item in sending_data.menu_items) {
                    sending_data.menu_items[item].menu_item = sending_data.menu_items[item].id
                }
                sending_data.customer_comment = this.order.customer_comment
                sending_data.customer_name = this.order.customer_name
                sending_data.custumer_phone = this.order.custumer_phone
                sending_data.menu = this.order.menu
                await axios
                    .post(url, sending_data, {
                        headers: {
                        }
                    })
                    .then(response => {
                        console.log(response)
                        this.close()

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        },

        close() {
            this.$emit('close')
        },
    },
}
</script>
