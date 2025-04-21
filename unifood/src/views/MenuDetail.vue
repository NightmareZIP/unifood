<template>
    <div v-if="!is_tarif">
        <h1>Внимание! У компании нет активного тарифа функционал сервиса недоступен!</h1>
    </div>
    <div v-else>
        <div v-if="is_head" class="bg-gray-200 p-4 rounded-lg">
            <p class="text-lg font-bold">Вам достпно еще {{ available_menu }} новых меню, согласно тарифу вы можете
                работать с {{ company_tarif.max_menu }} меню </p>
            <p class="text-gray-700">Для увеличения количества меню, необходимо приобрести расширение тарифа.</p>
        </div>
        <div class="pl-5 pr-5 relative">
            <button v-if="can_add" @click=" newMenu()"
                class="bg-amber-600 hover:bg-orange-700 text-white font-bold text-3xl py-4 px-6 mt-10 rounded-full">
                +
            </button>
            <button v-if="orderMode && Object.keys(order.menu_items).length > 0" @click="showOrderPopup = true"
                class="fixed bottom-5 right-5 bg-amber-600 hover:bg-orange-700 text-white font-bold text-md py-4 px-6 mt-10 z-2">
                Перейти в корзину
            </button>
            <div class="w-full flex flex-wrap justify-start mt-10">
                <div v-for="(items, key) in items_data">
                    <p class="text-gray-500 text-lg font-bold">{{ key }}</p>
                    <MenuItemCard v-for="(item, index) in items" @click="showDetail(item.id)"
                        @open="showDetail(item.id)" @add_to_cart="add_to_cart(item.id, 1)" @set_to_cart="set_to_cart"
                        :orderMode="orderMode" :headText="item.name" :address="item.address" :image="item.image"
                        :id="item.id" :amount="amount_in_cart(item.id)" />
                </div>
            </div>
            <MenuItemPopup v-if="!orderMode && showPopup" @close="close()" :item_data="item_info" :is_new="is_new" />
            <MenuItemOrderPopup v-if="orderMode && showPopup" @close="close()" @set_to_cart="set_to_cart"
                :item_data="item_info" :amount="amount_in_cart(item_info.id)" />

            <div v-if="orderMode && showOrderPopup"
                class="fixed inset-0 bg-gray-500/75 z-10 w-screen overflow-y-auto md:block" role="dialog"
                aria-hidden="true" aria-modal="true">
                <div @submit.prevent="submitForm"
                    class="flex min-h-full justify-center text-center md:items-center md:px-2 lg:px-4 lg:items-center">
                    <div
                        class="lg:max-w-4xl relative flex w-full items-stretch overflow-hidden bg-white px-4 pt-14 pb-8 shadow-2xl sm:px-6 sm:pt-8 md:p-6 lg:p-8">
                        <button @click="showOrderPopup = false" type="button"
                            class="absolute top-2 right-2 text-gray-400 hover:text-gray-500">
                            <span class="sr-only">Закрыть</span>
                            <svg class="size-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                aria-hidden="true" data-slot="icon">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        </button>
                        <OrderDetail @close="showOrderPopup = false" :order="order"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import MenuItemCard from "../components/MenuItemCard.vue";
import MenuItemPopup from "../components/MenuItemPopup.vue";
import MenuItemOrderPopup from "../components/MenuItemOrderPopup.vue";
import OrderDetail from "../components/OrderDetail.vue";

export default {
    components: { MenuItemPopup, MenuItemCard, MenuItemOrderPopup, OrderDetail },
    name: "MenuDetail",
    props: {
        orderMode: true,
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
            order: {
                menu_items:{},
                customer_name: '',
                custumer_phone: '',
                customer_comment: '',
                menu: this.$route.params.menu_id,
                uuid: '',
            },
            showOrderPopup: false,
        }
    },
    mounted() {
        this.get_data();
        this.get_user();
        this.get_tarif();

    },
    computed: {
        is_head() { return this.$store.state.worker.is_head },
        can_add() {
            return this.$store.state.worker.is_head && this.company_tarif.max_menu > this.count
        },
        available_menu() {
            return this.company_tarif.max_menu - this.count
        },
        is_tarif() {
            console.log(this.company_tarif.tarif_date)
            return this.company_tarif.tarif_date && new Date(this.company_tarif.tarif_date) > Date.now()
        },

    },

    methods: {
        //Вынести в отдельную либу?
        async get_user() {
            await axios
                .get("/api/v1/workers/")
                .then(response => {
                    this.worker = response.data[0]
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
                .get("/api/v1/tarif/" + this.tarif + '/?menu=' + this.$route.params.menu_id)
                .then(response => {
                    this.company_tarif = response.data
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
        async get_data() {
            await axios.get("/api/v1/menu-items/", {
                params: {
                    menu: Number(this.$route.params.menu_id)
                }
            }).then(response => {
                this.count = response.data.count
                this.items_data = {}
                this.unsorted_data = response.data.results
                for (let key in response.data.results) {
                    let item = response.data.results[key]
                    if (!(item.category in this.items_data)) {
                        this.items_data[item.category] = [item]
                    }
                    else {
                        this.items_data[item.category].push(item)
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
        newMenu() {

            this.item_info = {
                id: 0,
                name: "",
                detail: '',
                is_new: true,
                can_edit: true,
                address: "",
                logo: "",
                menu: Number(this.$route.params.menu_id),
            };
            this.is_new = true
            this.showPopup = true

        },
        //Отображение события
        showDetail(id) {

            let copy_item = [...this.unsorted_data]
            let item = copy_item.filter(e => e.id == id)[0]
            this.item_info = item
            this.item_info.menu = Number(this.$route.params.menu_id)
            this.is_new = false
            this.showPopup = true
        },
        close() {
            this.get_data()
            this.showPopup = false
            this.item_info = {}
        },
        amount_in_cart(itemId) {
            if (!this.order.menu_items[itemId]) {
                return 0
            }
            else {
                return this.order.menu_items[itemId].amount
            }
        },
        add_to_cart(itemId, amount) {
            if (!this.order.menu_items[itemId]) {
                let copy_item = [...this.unsorted_data]
                let item = copy_item.filter(e => e.id == itemId)[0]
                item.amount = amount
                this.order.menu_items[itemId] = item
            }
            else {
                this.order.menu_items[itemId].amount += amount
            }
        },
        delete_from_cart(itemId, amount) {
            if (!this.order.menu_items[itemId]) {
                return
            }
            else {
                this.order.menu_items[itemId].amount -= amount
            }
        },
        set_to_cart(itemId, amount, comment = null) {
            console.log(amount)
            if (!this.order.menu_items[itemId]) {
                let copy_item = [...this.unsorted_data]
                let item = copy_item.filter(e => e.id == itemId)[0]
                item.amount = amount
                this.order.menu_items[itemId] = item
            }
            try {
                amount = Number(amount)
                this.order.menu_items[itemId].amount = amount

            }
            catch (e) {
                console.log('Not number')
                this.order.menu_items[itemId].amount = 1
            }
            if (Boolean(comment)) {
                this.order.menu_items[itemId].user_comment = comment
            }
        },
    },
}
</script>
