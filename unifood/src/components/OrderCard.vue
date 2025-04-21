<template>
    <div class="p-4 max-w-sm font-bold">
        <div class="flex justify-center items-center rounded-lg dark:bg-gray-800 bg-lime-400 p-8 flex-col">
            <div class="flex items-center mb-3">
                <h2 class="text-white dark:text-white text-lg">Номер: {{ headText }}</h2>
            </div>
            <div class="flex flex-col justify-between flex-grow">
                <p class="leading-relaxed text-base text-white dark:text-gray-300">
                    {{ customer_name }}: {{ custumer_phone }}
                </p>
            </div>
            <div @click.stop class="mt-1 flex justify-center w-min">
                <button @click="this.$router.push('/orders/'+uuid)"
                    class="h-auto w-fit bg-amber-600 hover:bg-amber-700 text-white font py-2 px-4 rounded mr-2">
                    Просмотр
                </button>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name: "OrderCard",
    props: {
        headText: String,
        customer_name: String,
        custumer_phone: String,
        uuid: String,
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
