<template>
    <div v-if="!is_tarif">
        <h1>Внимание! У вас нет активного тарифа функционал сервиса недоуступен!</h1>
    </div>
    <div v-else>
        <div class="bg-gray-200 p-4 rounded-lg">
            <p class="text-lg font-bold">Вам достпно еще {{ available_menu }} новых меню, согласно тарифу вы можете
                работать с {{ company_tarif.max_menu }} меню </p>
            <p class="text-gray-700">Для увеличения количества меню, необходимо приобрести расширение тарифа.</p>
        </div>
        <div class="pl-5 pr-5">
            <button @click="newMenu()" v-if="can_add"
                class="bg-amber-600 hover:bg-orange-700 text-white font-bold text-3xl py-4 px-6 mt-10 rounded-full">
                +
            </button>
            <div class="w-full flex flex-wrap justify-start mt-10">
                <MenuCard @open="showDetail(item.id)" v-for="(item, index) in menu_data" :headText="item.name"
                    :address="item.address" :image="item.image" :id="item.id" />
            </div>
            <MenuPopup v-if="showPopup" @close="close()" :menu_data="menu_info" :is_new="is_new" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import MenuCard from "../components/MenuCard.vue";
import MenuPopup from "../components/MenuPopup.vue";

export default {
    components: { MenuPopup, MenuCard },
    name: "Menu",
    props: {},
    data() {
        return {
            company_tarif: {},
            errors: [],
            tarif: 0,
            worker: {},
            menu_data: [],
            showPopup: false,
            menu_info: {},
            is_new: true,
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
            return this.$store.state.worker.is_head && this.company_tarif.max_menu > this.menu_data.length
        },
        available_menu() {
            return this.company_tarif.max_menu - this.menu_data.length
        },
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
                    console.log(response)
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
            await axios.get("/api/v1/menu/").then(response => {
                this.menu_data = response.data.results
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

            this.menu_info = {
                id: 0,
                name: "",
                detail: '',
                is_new: true,
                can_edit: true,
                address: "",
                logo: "",

            }
            this.is_new = true
            this.showPopup = true

        },
        //Отображение события
        showDetail(id) {

            let copy_menu = [...this.menu_data]
            let menu = copy_menu.filter(e => e.id == id)[0]
            this.menu_info = menu
            this.is_new = false
            this.showPopup = true

        },
        close() {
            this.get_data()
            this.showPopup = false
            this.menu_info = {}
        },
    },

}
</script>
