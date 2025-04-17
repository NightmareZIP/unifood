<template>
    <div class="p-4 font-bold max-w-md">
        <div class="flex rounded-lg h-full dark:bg-gray-800 bg-lime-400 p-8 flex-col">
            <div v-if="image" class="max-h-50 relative">
                <img :src="image" alt="Логотип не задан" class="w-full h-full rounded-lg bg-lime-400 object-scale-down">
            </div>
            <div class="flex items-center mb-3">
                <h2 class="text-white dark:text-white text-lg">{{ headText }}</h2>
            </div>
            <p class="leading-relaxed text-base text-white dark:text-gray-300">
                {{ address }}
            </p>
            <div class="mt-1 flex font-normal">
                <button class="h-auto bg-amber-600 hover:bg-amber-700 text-white py-2 px-2 rounded mr-2">
                    <router-link :to="'/menu-items/' + id">Содержимое
                        меню</router-link>
                </button>
                <button @click="open" class="h-auto bg-amber-600 hover:bg-amber-700 text-white py-2 px-2 rounded mr-2">
                    Детальное описание меню

                </button>
                <button class="h-auto bg-amber-600 hover:bg-amber-700 text-white py-2 px-2 rounded mr-2">
                    <router-link :to="'/orders/?menu=' + id"> Заказы </router-link>
                </button>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name: "MenuCard",
    props: {
        headText: String,
        address: String,
        image: String,
        id: Number,
    },
    data() {
        return {

        }
    },
    computed: {

    },
    created() {
    },
    methods: {

        open() {
            console.log('open')
            this.$emit('open')
        },
    },
}
</script>
