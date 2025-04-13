<template>
  <div class="calendar-column" :class="{ selected: active }">
    <div class="calendar-column-header">
      <span class="day">{{
        day.toLocaleString('ru-RU', { weekday: "short" })
      }}
        {{ day.getDate() }}
      </span>
    </div>

    <div class="calendar-column-body">
      <div class="calendar-time" @click="$emit('newEvent', n - 1, day)" v-for="n in 24" :key="`${n - 1}`">
        {{ n - 1 }}:00
      </div>
      <div class="calendar-eventgrid">
        <div class="index" v-if="new Date().getDay() === day.getDay()" :style="{}"></div>

        <calendar-event @showPopup="(id) => $emit('showPopup', id)" v-for="(e, index) in positioning" :key="index"
          :data="e"></calendar-event>
      </div>
    </div>
  </div>
</template>

<script>
import CalendarEvent from "./CalendarEvent.vue"

import * as fn from "../utils"

export default {
  name: "calendarcolumn",
  emits: ['showPopup',],
  components: {
    CalendarEvent
  },
  props: {
    day: Date,
    data: Array
  },
  data() {
    return {
      scrollPercent: 0,
      editing: true,
      active: true
    }
  },
  methods: {

  },
  computed: {
    positioning() {
      if (!this.data) return []
      return [...this.data] // Сортируем события по их дате начала
        .sort((a, b) =>
          fn.isSame(a.grid.start, b.grid.start)
            ? b.grid.dur - a.grid.dur
            : fn.diffMinutes(a.grid.start, b.grid.start)
        )
        // Ищем пересекающиеся события
        .map(item => {

          let same = this.data.filter(i =>
            (fn.isSame(i.grid.start, item.grid.start) &&
              fn.isSame(i.grid.end, item.grid.end)
            ) ||
            (
              fn.isBefore(i.grid.start, item.grid.start) &&
              !fn.isBefore(i.grid.end, item.grid.start)
            ) ||
            (
              fn.isAfter(i.grid.start, item.grid.start)
            )
          )
          //Если нет пересекающихся событий, помечаем, что пересечения нет
          if (same.length <= 1) {
            item.grid["index"] = null
            item.grid["indexOf"] = null
          } else {
            // Иначае присваиваем каждому событию его порядковый номер, для последующего сдвига в верстке
            //Чтобы события не перекрывали друг друга
            let index = 1

            same.forEach(i => {
              if (i.grid.index) {
                if (i.grid.index == index) index++
              }
            })

            item.grid["index"] = index
            item.grid["indexOf"] = same.length
          }

          return item
        })
    }
  }
}
</script>

<style scoped lang="scss">
.calendar-column {
  height: 90%;
  z-index: 3;

  &.border-left {
    border-left: 1px solid rgba(0, 0, 0, 0.1);
  }

  .calendar-column-header {
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding: 10px;
    background-color: #42b983;
    color: black;
    display: grid;
    align-items: center;

    position: relative;
    top: 0;
    z-index: 200;

    .day {
      font-size: 16px;
      text-transform: uppercase;
    }
  }

  .calendar-column-body {
    position: relative;
    // height: 100%;

    .calendar-column-body-slotgrid,
    .calendar-eventgrid {
      z-index: 1;

    }

    .calendar-column-body-editgrid {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      height: 100%;
    }

    .calendar-eventgrid {
      right: 15px;

      .index {
        position: relative;
        background-color: rgba(255, 0, 0, 0.5);
        left: 0px;
        right: -5px;
        height: 10px;
        z-index: 10;
        border-radius: 2px;
      }
    }

    // grid-template-rows: repeat(24, 1fr);

    .calendar-time {
      display: grid;
      z-index: 1;
      height: 100px;
      color: rgba(128, 121, 121, 0.9);
      margin-left: 2%;
      text-align: left;
      font-size: 14px;
      display: grid;

      &:not(:first-child) {
        border-top: 1px solid rgba(170, 170, 170, 0.2);
      }
    }
  }

}
</style>
