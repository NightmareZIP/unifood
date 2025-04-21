<template>
    <div class="fixed inset-0 bg-gray-500/75 z-10 w-screen overflow-y-auto md:block" role="dialog" aria-hidden="true"
        aria-modal="true">
        <form @submit.prevent="submitForm"
            class="flex min-h-full justify-center text-center md:items-center md:px-2 lg:px-4 lg:items-center">
            <div
                class="lg:max-w-4xl relative flex w-full items-stretch overflow-hidden bg-white px-4 pt-14 pb-8 shadow-2xl sm:px-6 sm:pt-8 md:p-6 lg:p-8">
                <button @click="close()" type="button" class="absolute top-2 right-2 text-gray-400 hover:text-gray-500">
                    <span class="sr-only">Закрыть</span>
                    <svg class="size-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                        aria-hidden="true" data-slot="icon">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                    </svg>
                </button>

                <div class="grid w-full grid-cols-1 items-stretch gap-x-6 gap-y-8 sm:grid-cols-12 lg:gap-x-8">
                    <div v-if="item_data?.image" class="sm:col-span-4 lg:col-span-5 relative">
                        <img :src="item_data.image" alt="Добавьте сюда ваш логотип"
                            class="w-full h-full rounded-lg bg-gray-100 object-scale-down">
                    </div>
                    <div v-else class="w-full h-full sm:col-span-4 lg:col-span-5 relative">
                        <label for="relative dropzone-file"
                            class="flex flex-col items-center justify-center w-full h-full border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
                            <div class="flex flex-col items-center justify-center pt-5 pb-6">
                                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="#000000">
                                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                    <g id="SVGRepo_iconCarrier">
                                        <path
                                            d="M7.828 5l-1-1H22v15.172l-1-1v-.69l-3.116-3.117-.395.296-.714-.714.854-.64a.503.503 0 0 1 .657.046L21 16.067V5zM3 20v-.519l2.947-2.947a1.506 1.506 0 0 0 .677.163 1.403 1.403 0 0 0 .997-.415l2.916-2.916-.706-.707-2.916 2.916a.474.474 0 0 1-.678-.048.503.503 0 0 0-.704.007L3 18.067V5.828l-1-1V21h16.172l-1-1zM17 8.5A1.5 1.5 0 1 1 15.5 7 1.5 1.5 0 0 1 17 8.5zm-1 0a.5.5 0 1 0-.5.5.5.5 0 0 0 .5-.5zm5.646 13.854l.707-.707-20-20-.707.707z">
                                        </path>
                                        <path fill="none" d="M0 0h24v24H0z"></path>
                                    </g>
                                </svg>
                            </div>
                        </label>
                    </div>
                    <div class="sm:col-span-8 lg:col-span-7">
                        <p class=" text-md  text-gray-900 sm:text-4xl">
                            Блюдо: {{ item_data.name }}
                        </p>
                        <p class=" text-md  text-gray-900 sm:text-4xl">
                            Категория: {{ item_data.category }}
                        </p>
                        <p v-if="item_data.price==item_data.discount_price" class=" text-md  text-gray-900 sm:text-4xl">
                            Цена: {{ item_data.price }}₽
                        </p>
                        <div v-else class="flex justify-center items-center">
                            <p class="line-through text-gray-500 mr-2">{{ item_data.price }}₽</p>
                            <p class="text-lg  mr-2">{{ item_data.discount_price }}₽</p>
                            <p class="text-sm text-gray-500">-{{ item_data.discount }}%</p>
                        </div>
                        <p class=" text-md  text-gray-900 sm:text-4xl">
                            Описание: {{ item_data.description }}
                        </p>
                        <textarea rows="4" v-model="user_comment" placeholder="Ваш комментарий для блюда"
                            class="text-3xl mt-6 mb-6 w-auto text-gray-900 sm:text-4xl"></textarea>
                        <div class="flex items-center">
                            <button @click="decrease"
                                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">
                                -
                            </button>
                            <input :value="current_amount" @input="set_amount($event.target.value)"
                                class="border border-gray-400 rounded px-4 py-2 mr-2 text-center" type="text">
                            <button @click="increase"
                                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                                +
                            </button>
                        </div>
                        <button @click="add_to_cart" type="submit"
                            class="mt-6 flex w-full items-center justify-center rounded-md border border-transparent bg-green-600 px-8 py-3 text-base font-medium text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-hidden">
                            Подтвердить выбор
                        </button>
                    </div>
                </div>
            </div>
        </form>
    </div>

</template>

<script>

export default {
    name: "MenuItemOrderPopup",
    props: {
        item_data: {
            name: "",
            detail: "",
            logo: "",
            category: "",
            image: "",
            price: 0,
            discount: 0,
            discount_start: null,
            discount_end: null,
            menu: null,
        },
        amount: 0,

    },
    data() {
        return {
            types: {},
            logo_input: null,
            current_amount: this.amount,
            user_comment: '',
        }
    },
    mounted() {

    },
    computed: {
    },
    methods: {
        set_amount(amount) {
            try {
                if (!isNaN(amount)){
                    console.log(amount)
                    
                    this.current_amount = Number(amount)
                }
                else{
                    this.current_amount = 1
                }
            }
            catch (e) {
                console.log(e)
                this.current_amount = 1
            }
        },
        add_to_cart() {
            try {
                this.current_amount = Number(this.current_amount)
                this.$emit('set_to_cart', this.item_data.id ,this.current_amount, this.user_comment)
                this.close()
            }
            catch (e) {
                this.current_amount = 1
            }
        },
        close() {
            this.$emit('close')
        },
        increase() {
            this.current_amount += 1;
        },
        decrease() {
            if (this.current_amount > 0) {
                this.current_amount -= 1;
            }
        }
    },
}
</script>
