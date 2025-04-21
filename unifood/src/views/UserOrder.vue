<template>
    <div class="p-6">
        <p class="title">Заказ {{ order.id }}</p>
        <div>
            <OrderDetail :order="order" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import OrderDetail from "../components/OrderDetail.vue";
export default {
    name: "UserOrder",
    components: { OrderDetail },
    props: {
    },
    data() {
        return {
            order: {},
            errors: [],
        }
    },
    computed: {

    },
    created() {
        this.get_data()
    },
    methods: {
        
        async get_data() {
            await axios
                .get("/api/v1/orders-user/0/?uuid=" + this.$route.params.uuiid)
                .then(response => {
                    this.order = response.data
                    for (let key in this.order.menu_items) {
                        this.order.menu_items[key] = {
                            ...this.order.menu_items[key],
                            ...this.order.menu_items[key].menu_item_detail,
                            
                        }
                        
                    }
                })
                .catch(error => {

                    console.log(error)

                })
        },

    },
}
</script>
