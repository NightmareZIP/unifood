<template>
    <h1 class="title">Ваши коллеги</h1>
    <div class='box'>
        <div class="content has-text-left">
            <ol type="1">

                <li v-for="(value, index) in workers_info" :key="index">
                    <router-link :to="get_link(value.id)">{{ value.name }} {{ value.second_name }} {{ value.last_name
                    }}</router-link>


                </li>

            </ol>
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

            }
            ,
            errors: [],
        }
    },
    computed: {

    },
    created() {
        this.get_data()
    },
    methods: {
        get_link(id) {
            return "/my-calendar/" + id
        },
        async get_data() {
            await axios
                .get("/api/v1/workers/get_workers/")
                .then(response => {
                    console.log(response)
                    this.workers_info = response.data
                    // this.$router.push('/login')
                })
                .catch(error => {

                    console.log(error)

                })
        },

    },
}
</script>
