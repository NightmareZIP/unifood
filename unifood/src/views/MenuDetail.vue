<template>
    <div>
        <div class="bg-gray-200 p-4 rounded-lg">
            <p class="text-lg font-bold">Вам достпно еще {{ available_menu }} новых меню</p>
            <p class="text-gray-700">Для увеличения количества меню, необходимо приобрести расширение тарифа.</p>
        </div>
        <button v-if="can_add" class="bg-orange-500 hover:bg-orange-700 text-white font-bold py-4 px-6 rounded-full">
            +
        </button>
        <div class="flex flex-wrap justify-center mt-10">
            <ProfileMenuCard v-for="(item, index) in menu_data" :headText="item.name" :bodyText="item.description"
                :image="item.image" />

        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "MenuDetail", props: {}, data() {
        return {
            tarifs_data: {},
            company_tarif: {},
            errors: [],
            tarif: 0,
            worker: {},
            menus: {},
        }
    },
    created() {
        this.get_data();
        this.get_user().then(res => {
            if (this.tarif) {
                this.get_tarif();
            }
        })

        // this.tarif = this.$store.state.worker.company.tarif
        // this.company_id = this.$store.state.worker.company.id

    },
    computed: {
        is_head() { return this.$store.state.worker.is_head },
        can_add() {
            return this.$store.state.worker.is_head && this.tarif.max_menu > this.menu_data.length
        },
        available_menu() {
            return this.tarif.max_menu - this.menus.length
        }
    },

    methods: {
        async get_data() {
            await axios.get("/api/v1/menu/").then(response => {
                console.log(response)
                this.menu_data = response.data
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
                .put("/api/v1/company/" + this.menu_data.id + '/', this.menu_data)
                .then(response => {
                    console.log(response)
                    this.menu_data = response.data[0]
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
