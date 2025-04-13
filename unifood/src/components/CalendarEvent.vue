<template>
  <div @click="$emit('showPopup', data.e.id)" class="calendar-event" :style="getPos(data.grid)">
    <div class="cal-event-content" :style="getColor">
      {{ data.e.event_name }}
    </div>
  </div>
</template>

<script>
import * as fn from "../utils"

export default {
  name: "calendareventv2",
  props: {
    data: Object
  },
  data() {
    return {
      opened: false
    }
  },
  computed: {
    getColor() {

      return {
        backgroundColor: this.data.color,
        color: 'white'
      }
    }
  },
  methods: {

    timeToPercent(t) {
      //set top position of event block
      let percent = (t - 0) / (60 * 24 - 0)
      let outputX = percent * (100 - 0) + 0
      return outputX + "%"
    },
    durationToPercent(l) {
      //set height of event block
      let percent = (l - 0) / (60 * 24 - 0)
      let outputX = percent * (100 - 0) + 0
      return outputX + "%"
    },

    getPos({ start, end, index, indexOf }) {
      // Рассчитывает позицию события относительно его вермени, а так же наличия
      // событий пересекающихся с ним по времени
      let offset = start.getMinutes() + start.getHours() * 60
      let duration = fn.diffMinutes(start, end)

      if (this.opened) {
        return {
          position: "absolute",
          right: "0px",
          left: "2.5px",
          top: this.timeToPercent(offset),
          height: this.durationToPercent(duration)
        }
      }
      let width = 90
      //Индекс элемента указывает количество пересекающихся событий
      if (index !== null) width = width / indexOf
      let left = 0
      //Рассчитываем отступ
      if (index !== null) {
        left = left + width * (index - 1)
      }


      return {
        position: "absolute",
        // right: right + "rem",
        width: width + "%",
        left: left + "%",
        top: this.timeToPercent(offset),
        height: this.durationToPercent(duration)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.calendar-event {
  position: relative;

  z-index: 2;
  border-radius: 2px;
  // overflow: hidden;
  border: 1px solid rgb(222, 222, 222);

  transition: all 50ms;

  &:hover {
    transition: all 250ms;
    opacity: 1;
    cursor: pointer;
    transform: scale(1.025);
    z-index: 10;
    font-weight: bold;
  }



  .cal-event-content {
    width: 100%;
    height: 100%;
    padding: 4px;
    word-wrap: break-word;
    text-align: auto;
    box-sizing: border-box;
    align-items: center;
    // display: flex;
    // align-items: flex-start;
    // justify-content: flex-start;
    font-size: 1.5vmin;

    color: #454545;
  }
}
</style>
