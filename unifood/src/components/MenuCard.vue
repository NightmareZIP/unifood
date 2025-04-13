<template>
    <div class="p-4 max-w-sm font-bold">
        <div class="w-fit flex rounded-lg h-full dark:bg-gray-800 bg-lime-400 p-8 flex-col">
            <div v-if="image" class="max-h-50 sm:col-span-4 lg:col-span-5 relative">
                <img :src="image" alt="Логотип не задан" class="w-full h-full rounded-lg bg-lime-400 object-scale-down">
            </div>
            <div class="flex items-center mb-3">
                <h2 class="text-white dark:text-white text-lg">{{ headText }}</h2>
            </div>
            <div class="flex flex-col justify-between flex-grow">
                <p class="leading-relaxed text-base text-white dark:text-gray-300">
                    {{ address }}
                </p>
                <div class="mt-1 flex">
                    <button class="h-auto bg-amber-600 hover:bg-amber-700 text-white font py-2 px-4 rounded mr-2">
                        <router-link :to="'/menu/' + id">Содержимое
                            меню</router-link>
                    </button>
                    <button @click="open"
                        class="h-auto bg-amber-600 hover:bg-amber-700 text-white font py-2 px-4 rounded">
                        Детальное описание меню
                    </button>
                </div>
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
