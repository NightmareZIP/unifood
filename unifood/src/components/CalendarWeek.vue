<template>
    <div class="calendar" ref="calendar">
        <CalendarColumn @newEvent="(n, day) => $emit('newEvent', n, day)" @showPopup="(id) => $emit('showPopup', id)"
            v-for="(value, name, index) in concatenatedData" :key="name" :data="value" :day="days[index]" />
    </div>
</template>

<script>
import * as fn from "../utils"

import CalendarColumn from "../components/CalendarColumn.vue"

export default {
    name: "calendarweek",
    components: { CalendarColumn },
    data() {
        return {
        }
    },
    props: {
        concatenatedData: { default: {} },
        selected: new Date(),
        precision: { type: Number },
    },
    computed: {
        //Разбиваем события по дням недели
        days() {
            let result = []
            console.log(this.selected);
            for (var i = 0; i < 7; i++) {
                result.push(fn.addDays(fn.getMonday(this.selected), i))
            }
            console.log(Object.values(this.concatenatedData))
            return result
        },
    },


    methods: {

    },
}
</script>
<style scoped lang="scss">
.calendar {
    display: grid;
    width: 75%;
    margin-left: auto;
    margin-right: 20px;
    color: rgb(161, 153, 153);

    height: 100%;
    // user-select: none;

    grid-template-columns: repeat(7, 1fr);
    grid-template-rows: 300%;
}
</style>