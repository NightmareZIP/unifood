<template>
    <div class="p-4 max-w-sm font-bold">
        <div class="w-fit flex rounded-lg h-full dark:bg-gray-800 bg-lime-400 p-8 flex-col">
            <div class="flex items-center mb-3">
                <h2 class="text-white dark:text-white text-lg">{{ headText }}</h2>
            </div>
            <div class="flex flex-col justify-between flex-grow">
                <p class="leading-relaxed text-base text-white dark:text-gray-300">
                    {{ address }}
                </p>
                <div class="mt-1 flex">
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">
                        Содержимое меню
                    </button>
                    <!-- <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">
                        Получить QR-код
                    </button> -->
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
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

    },
}
</script>
