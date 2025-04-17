<template>
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
        <button v-if="orderMode" @click="newMenu()"
            class="fixed bottom-5 right-5 bg-amber-600 hover:bg-orange-700 text-white font-bold text-md py-4 px-6 mt-10 z-2">
            Перейти в корзину
        </button>
        <div class="w-full flex flex-wrap justify-start mt-10">
            <div v-for="(items, key) in items_data">
                <p class="text-gray-500 text-lg font-bold">{{ key }}</p>
                <MenuItemCard v-for="(item, index) in items" @click="showDetail(item.id)" @open="showDetail(item.id)"
                    @add_to_cart="add_to_cart(item.id, 1)" @set_to_cart="set_to_cart" :orderMode="orderMode" :headText="item.name"
                    :address="item.address" :image="item.image" :id="item.id" :amount="amount_in_cart(item.id)" />
            </div>
        </div>
        <MenuItemPopup v-if="!orderMode && showPopup" @close="close()" :item_data="item_info" :is_new="is_new" />
        <MenuItemOrderPopup v-if="orderMode && showPopup" @close="close()" :item_data="item_info"
            :amount="amount_in_cart(item_info.id)" />

    </div>
</template>

<script>
import axios from 'axios'
import MenuItemCard from "../components/MenuItemCard.vue";
import MenuItemPopup from "../components/MenuItemPopup.vue";
import MenuItemOrderPopup from "../components/MenuItemOrderPopup.vue";

export default {
    components: { MenuItemPopup, MenuItemCard, MenuItemOrderPopup },
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
            cart: {},
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
        can_add() {
            return this.$store.state.worker.is_head && this.company_tarif.max_menu > this.count
        },
        available_menu() {
            return this.company_tarif.max_menu - this.count
        },

    },

    methods: {
        //Вынести в отдельную либу?
        async get_user() {
            await axios
                .get("/api/v1/workers/")
                .then(response => {
                    console.log(response)
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
                .get("/api/v1/tarif/" + this.tarif + '/')
                .then(response => {
                    console.log(response)
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
            if (!this.cart[itemId]) {
                return 0
            }
            else {
                return this.cart[itemId].amount
            }
        },
        add_to_cart(itemId, amount) {
            if (!this.cart[itemId]) {
                let copy_item = [...this.unsorted_data]
                let item = copy_item.filter(e => e.id == itemId)[0]
                item.amount = amount
                this.cart[itemId] = item
            }
            else {
                this.cart[itemId].amount += amount
            }
        },
        delete_from_cart(itemId, amount) {
            if (!this.cart[itemId]) {
                return
            }
            else {
                this.cart[itemId].amount -= amount
            }
        },
        set_to_cart(itemId, amount) {
            console.log(amount)
            if (!this.cart[itemId]) {
                let copy_item = [...this.unsorted_data]
                let item = copy_item.filter(e => e.id == itemId)[0]
                item.amount = amount
                this.cart[itemId] = item
            }
            this.cart[itemId].amount = amount
        },
    },
}
</script>
