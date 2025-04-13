<template>
    <table class="table">
        <thead>
            <tr>
                <td>
                    <button v-on:click="decrease">{{ '<' }} </button>
                </td>
                <td colspan="5"> {{ months[month] }} {{ year }} </td>
                <td>
                    <button v-on:click="increase">{{ '>' }}</button>
                </td>
            </tr>
            <tr>
                <td v-for="d in day" :key="`${d}`"> {{ d }}</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(week, ind) in      calendar     " :key="`${ind}`">
                <td :class="[day_el.date == date ? 'active' : '', '']" @click="change_active($event, day_el)"
                    v-for=" (day_el, ind) in      week     " :key="`${ind}`"> {{ day_el.index }}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name: "calendarinput",
    data() {
        return {
            month: new Date().getMonth(),
            year: new Date().getFullYear(),
            cur_day: new Date().getDate(),

            dFirstMonth: '1',
            day: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
            months: ["Январь", "Февраль", "Март", "Апрель", "Май",
                "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрт", "Декабрь"],
            date: new Date(),

        }
    },
    mounted() {

    },
    methods: {
        // Смена дня
        change_active(event, day_el) {
            this.date = day_el.date;
            this.$emit('changeDay', day_el)
        },
        //Предыдущий месяц
        decrease() {
            this.month--;
            if (this.month < 0) {
                this.month = 12
                this.month--
                this.year--
            }

        },
        // Следующий месяц
        increase() {

            this.month++;
            if (this.month > 11) {
                this.month = 0
                this.year++
            }
        },
    },
    computed: {
        //дни месяца
        calendar() {
            this.date.setHours(0, 0, 0, 0)
            let days = []
            let week = 0
            days[week] = []
            //последний день месяца
            let last_day = new Date(this.year, this.month + 1, 0).getDate();
            //Проходим по всем дням месяца
            for (let i = 1; i <= last_day; i++) {
                //определяем является ли день понедельником
                if (new Date(this.year, this.month, i).getDay() == this.dFirstMonth) {
                    week++;
                    days[week] = [];
                }
                //Помечаем выбранный день
                let a = { index: i, date: new Date(this.year, this.month, i) }
                if (a.date.valueOf() == this.date.valueOf()) {
                    this.date = a.date
                }
                //добавляем день в его неделю
                days[week].push(a)
                if ((i == new Date().getDate()) && (this.year == new Date().getFullYear()) && (this.month == new Date().getMonth())) { a.current = '#747ae6' }
            }
            //Не выводим дни прошлого месяца, вместо этого заполняем их пустыми значениями
            if (days[0].length > 0) {
                for (let i = days[0].length; i < 7; i++) {
                    days[0].unshift('')

                }
            }
            return days;
        },
    },



}
</script>
<style lang="scss">
.table {
    margin-left: 20px;
    margin-right: 20px;
    border-collapse: collapse;
    float: left;
    position: sticky;
    top: 20%;
    left: 20px;
    right: 20px;

    table-layout: fixed;
}

.format-week {
    float: right;
}

.table td {
    text-align: center;
    cursor: pointer;

    &.active {
        color: #42b983;
    }
}

.table thead tr:last-child {
    background-color: #42b983;
}
</style>