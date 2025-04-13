<template>
  <h1 v-if="(this.$route.params.id)">Календарь коллеги {{ [collegue.name, collegue.last_name,
  collegue.surname].join(' ') }}</h1>
  <CalendarInput @changeDay="reloadColumns" />
  <CalendarWeek @newEvent="newEvent" @showPopup="showEvent" :key="reload" ref="calendar" :selected="selected_day"
    :concatenatedData="weekData" :precision="precision">
  </CalendarWeek>
  <EventPopup @close="getEvents(); show_popup = false" v-if="show_popup" :event_info="event_info" :is_head="is_head" />
</template>

<script>
import CalendarInput from "../components/CalendarInput.vue"
import CalendarWeek from "../components/CalendarWeek.vue"
import EventPopup from "../components/MenuPopup.vue"


import * as fn from "../utils"
import axios from 'axios'

export default {
  name: "calendar",
  components: { CalendarWeek, CalendarInput, EventPopup },
  data() {
    return {
      //Данные коллеги, если смотрим его календарь 
      collegue: {},
      //Является ли сотрудник руководителм коллеги
      is_head: false,
      cur_date: new Date(),
      event_info: {
      },
      selected_day: new Date(),
      show_popup: false,
      data: [
      ],
    }
  },

  props: {
    //точность рассчета
    precision: {
      type: Number, default: 1
    },
  },

  mounted() {
    if (this.$route.params.id) {
      this.isHead()
    }
    this.getEvents()
  },
  methods: {
    //Получаем данные по коллеги и определяем, является ли пользователь его руководителм
    async isHead() {
      let url = "/api/v1/workers/" + this.$route.params.id + '/'
      await axios
        .get(url)
        .then(response => {
          this.collegue = response.data
          this.is_head = this.$store.state.worker.id == response.data.head
        })
        .catch(error => {
          console.log(error)
        })
    },
    //Проверка прав на изменение календаря
    checkRights() {
      if ((this.$route.params.id && this.$store.state.worker.id != this.$route.params.id) && !this.is_head) {
        alert("Вы можете изменять только свой календарь и календарь своих подчиненных!")
        return false
      }
      return true
    },
    async getEvents() {
      //Получение событий
      let params = {
        date_from: fn.getMonday(this.cur_date).toISOString().split('T')[0],
        date_to: fn.getSunday(this.cur_date).toISOString().split('T')[0],
      }
      if (this.$route.params.id) {
        params.user_id = this.$route.params.id
      }
      await axios
        .get("/api/v1/event/get_events/", { params: params })
        .then(response => {
          let new_data = []
          //Проверка периодичности
          Object.values(response.data).forEach(val => {
            if (val.period == 0) {
              new_data.push(val)
            }
            else {
              let from = new Date(val.date_from)
              from.setHours(0, 0, 0, 0)
              //Получаем дни выбранной недели
              let daters_arr = fn.getDates(fn.getMonday(this.cur_date), fn.getSunday(this.cur_date))
              //Определяем дни на которые должно быть выбрано периодическое событие
              daters_arr.forEach(week_date => {
                if (week_date >= from) {
                  let dif = Math.abs(week_date - from)
                  dif = dif / (1000 * 3600 * 24)
                  //Если разница дней кратна периодичности, то на этот день должно быть установлено событие
                  if (dif % val.period == 0) {
                    let val_copy = JSON.parse(JSON.stringify(val));
                    val_copy.date_from = fn.addDays(new Date(val_copy.date_from), dif)
                    val_copy.date_to = fn.addDays(new Date(val_copy.date_to), dif)

                    new_data.push(val_copy)
                  }
                }
              })
            }
          })
          this.data = new_data
        })
        .catch(error => {
          console.log(error)
        })
    },
    //Создание нового события
    newEvent(n = 0, time = new Date()) {
      if (!this.checkRights()) {
        return false
      }

      time.setHours(n, 0, 0)
      this.event_info = {
        id: 0,
        date_from: time,
        date_to: time,
        period: 0,
        color: '',
        event_type: '',
        event_name: "Новое событие",
        is_new: true,
        can_edit: true,
        created_by: 'Вами',
        comment: "",

      }
      this.show_popup = true

    },
    //Обработка изменения недели
    reloadColumns(day) {
      this.selected_day = day.date
      this.cur_date = day.date
      this.getEvents()
      // this.reload += 1
    },
    //Отображение события
    showEvent(id) {
      // if (!this.checkRights()) {
      //   return false
      // }
      let copy_events = [...this.data]
      let event = copy_events.filter(e => e.id == id)[0]
      event.is_new = false
      this.event_info = event

      this.show_popup = true

    }
  },
  computed: {

    weekData() {
      //Окрругление даты
      const roundTime = t => {
        let m = t.getMinutes()
        let h = t.getHours()

        t.setHours(h)
        t.setMinutes(m)
        t.setSeconds(0)
        t.setMilliseconds(0)
        return t
      }

      let tmp = {
        mon: [],
        tue: [],
        wed: [],
        thu: [],
        fri: [],
        sat: [],
        sun: []
      }
      //Обработка полученных от сервера данных и приведение их к формату для компонентов
      if (this.data)
        this.data.forEach(date => {
          let start = new Date(date.date_from.date || date.date_from)
          let end = new Date(date.date_to.date || date.date_to)
          let weekday = new Date(start)
            .toLocaleString("default", { weekday: "short" })
            .toLowerCase()

          let e = {
            id: date.id,
            color: date.event_type.color,

            owner: date.created_by,
            e: date,

            grid: {
              //начала события
              start: roundTime(start),
              //окончание события
              end:
                start.getTime() != end.getTime()
                  ? roundTime(end)
                  : roundTime(
                    end.setMinutes(end.getMinutes(), this.precision)
                  ),
              // Продолжительность события
              dur:
                start.getTime() != end.getTime()
                  ? Math.round(fn.diffMinutes(end, start) / this.precision)
                  : Math.round(
                    (fn.diffMinutes(end, start) + this.precision) /
                    this.precision
                  )
            }
          }
          //Добавление события по дню недели
          tmp[weekday].push(e)
        })

      return tmp
    }
  }
}
</script>


