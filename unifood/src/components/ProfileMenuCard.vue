<template>
    <div class="p-4 max-w-sm">
        <div class="flex rounded-lg h-full dark:bg-gray-800 bg-lime-400 p-8 flex-col">
            <div class="flex items-center mb-3">
                <h2 class="text-white dark:text-white text-lg font-medium">{{ headText }}</h2>
            </div>
            <div class="flex flex-col justify-between flex-grow">
                <p class="leading-relaxed text-base text-white dark:text-gray-300">
                    {{ bodyText }}
                </p>
                <span>
                    <router-link :to="link">Перейти</router-link>
                    <span>
                        <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                            stroke-width="2" class="w-4 h-4 ml-2" viewBox="0 0 24 24">
                            <path d="M5 12h14M12 5l7 7-7 7"></path>
                        </svg>
                    </span>
                </span>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name: "ProfileMenuCard",
    props: {
        headText: String,
        bodyText: String,
        link: String,
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
