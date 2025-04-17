<template>
    <div class="p-4 max-w-sm font-bold">
        <div class="flex justify-center items-center rounded-lg dark:bg-gray-800 bg-lime-400 p-8 flex-col">
            <div v-if="image" class="relative">
                <img :src="image" alt="Логотип не задан" class="w-full max-h-full rounded-lg bg-lime-400 object-fit">
            </div>
            <div class="flex items-center mb-3">
                <h2 class="text-white dark:text-white text-lg">{{ headText }}</h2>
            </div>
            <div class="flex flex-col justify-between flex-grow">
                <p class="leading-relaxed text-base text-white dark:text-gray-300">
                    {{ address }}
                </p>
            </div>
            <div @click.stop class="mt-1 flex justify-center w-min">
                <div v-if="orderMode" class="flex flex-row card_countert">
                    <button @click.stop.prevent="$emit('add_to_cart')"
                        class=" h-auto w-fit bg-amber-600 hover:bg-amber-700 text-white font py-2 px-4 rounded mr-2">
                        Добавить </button>
                    <input class="w-auto bg-gray-200 font-bold rounded-lg" type="number" min="0" max="100"
                        :value="amount" @input="event => set_to_cart(event.target.value)">
                </div>
                <button v-else @click="$emit('open')"
                    class="h-auto w-fit bg-amber-600 hover:bg-amber-700 text-white font py-2 px-4 rounded mr-2">
                    Просмотр
                </button>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name: "MenuШItemCard",
    props: {
        headText: String,
        address: String,
        image: String,
        id: Number,
        amount: 0,
        orderMode: true,
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
            this.$emit('open')
        },
        set_to_cart(amount){
            this.$emit('set_to_cart', this.id, Number(amount))
        }
        
    },
}
</script>
