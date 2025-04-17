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
                        <input :disabled="!is_head" @change="setImage" id="rela-file" type="file"
                            class="hidden absolute bottom-0" />
                    </div>
                    <div v-else class="w-full h-full sm:col-span-4 lg:col-span-5 relative">
                        <label for="relative dropzone-file"
                            class="flex flex-col items-center justify-center w-full h-full border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
                            <div class="flex flex-col items-center justify-center pt-5 pb-6">
                                <svg class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
                                </svg>
                            </div>
                            <input :disabled="!is_head" @change="setImage" id="rela-file" type="file"
                                class="hidden absolute bottom-0" />
                        </label>
                    </div>
                    <div class="sm:col-span-8 lg:col-span-7">
                        <input :disabled="!is_head" v-model="item_data.name" placeholder="Задайте название блюда"
                            id="information-heading" class="w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
                        <input :disabled="!is_head" type="text" v-model="item_data.category"
                            placeholder="Категория блюда"
                            class="mt-6 w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
                        <div>
                            <p class="mt-6 text-sm text-gray-500">Установите Цену</p>
                            <input min="1" :disabled="!is_head" type="number" v-model="item_data.price"
                                placeholder="Цена (рубли)"
                                class="mt-2 w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
                        </div>
                        <div>
                            <p class="mt-6 text-sm text-gray-500">Установите скидку, если требуется</p>
                            <input min="0" max="100" :disabled="!is_head" type="number" v-model="item_data.discount"
                                placeholder="Размер скидки рубли"
                                class="mt-2 w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
                        </div>
                        <div>
                            <p class="mt-6 text-sm text-gray-500">Установите дату начала скидки</p>
                            <input :disabled="!is_head" type="date" v-model="item_data.discount_start"
                                placeholder="Дата начала скидки"
                                class="w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
                        </div>
                        <div>
                            <p class="mt-6 text-sm text-gray-500">Установите дату окончания скидки</p>
                            <input :disabled="!is_head" type="date" v-model="item_data.discount_end"
                                placeholder="Дата окончания скидки"
                                class="w-1/2 text-3xl font-bold text-gray-900 sm:text-4xl" />
                        </div>
                        <textarea :disabled="!is_head" rows="4" v-model="item_data.description"
                            placeholder="Доп описание для меню"
                            class="text-3xl mt-6 w-auto text-gray-900 sm:text-4xl"></textarea>
                        <button v-if="is_head" @click="save" type="submit"
                            class="mt-6 flex w-full items-center justify-center rounded-md border border-transparent bg-green-600 px-8 py-3 text-base font-medium text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-hidden">Сохранить</button>
                        <button v-if="!item_data.is_new && is_head" @click="delete_menu" type="submit"
                            class="mt-6 flex w-full items-center justify-center rounded-md border border-transparent bg-red-600 px-8 py-3 text-base font-medium text-white hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:outline-hidden">Удалить</button>
                    </div>
                </div>
            </div>
        </form>
    </div>

</template>

<script>

import axios from 'axios'

export default {
    name: "MenuItemPopup",
    props: {
        is_new: false,
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

    },
    data() {
        return {
            types: {},
            can_edit: this.is_head,
            logo_input: null,
        }
    },
    mounted() {

    },
    computed: {
        is_head() {
            return this.$store.state.worker.is_head
        },
    },
    methods: {
        setImage(e) {
            if (e.target.files && e.target.files[0]) {

                this.logo_input = e.target.files[0];
            }
            else {
                this.logo_input = null
            }
        },
        async save() {
            let url = '/api/v1/menu-items/'
            let sending_data = { ...this.item_data }
            if (this.logo_input) {
                sending_data.image = this.logo_input;
            }
            else {
                sending_data.image = null
            }
            if (sending_data.id != 0) {
                url += sending_data.id + '/'
                await axios
                    .put(url, sending_data, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        this.$store.commit('change_event', this.item_data)
                        this.item_data.image = response.data.image
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
            else {
                await axios
                    .post(url, sending_data, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        console.log(response)
                        this.close()

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        },
        async delete_menu() {
            if (this.$store.state.worker.id) {
                this.item_data.user_id = this.$route.params.id
            }
            await axios
                .delete("/api/v1/menu-items/" + this.item_data.id + '/', {
                    headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                    },
                })
                .then(response => {
                    this.close()
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
        close() {
            this.$emit('close')
        },
        download_qr() {
            let canvas = document.getElementsByClassName('canvas_qr')[0];
            let ctx = canvas.getContext('2d');
            let canvasUrl = canvas.toDataURL();
            const createEl = document.createElement('a');
            createEl.href = canvasUrl;
            createEl.download = "my-menu";
            createEl.click();
            createEl.remove();
        },
    },
}
</script>
