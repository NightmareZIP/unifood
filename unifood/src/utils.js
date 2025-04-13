export const diffMinutes = (dt2, dt1) => {
  let diff = (dt2.getTime() - dt1.getTime()) / 1000
  diff /= 60
  return Math.abs(Math.round(diff))
}

export const isBefore = (d1, d2) => {
  return d1.getTime() < d2.getTime()
}
export const isAfter = (d1, d2) => {
  return d1.getTime() > d2.getTime()
}

export const isSame = (d1, d2) => {
  return d1.getTime() === d2.getTime()
}

export const getMonday = d => {
  d = new Date(d)
  let day = d.getDay(),
    diff = d.getDate() - day + (day == 0 ? -6 : 1)
  return new Date(d.setDate(diff))
}
export const getSunday = d => {
  d = new Date(d)
  let day = d.getDay(),
  diff = d.getDate() + (day == 0 ? 0 : 7) - day
  let sunday = new Date(d.setDate(diff))
  sunday.setHours(23,59,59,0)
  return sunday
}

export const addDays = (date, amount) => {
  const d = date
  d.setDate(d.getDate() + amount)
  return d
}


export const getDates = (startDate, stopDate) => {
  startDate.setHours(0, 0, 0, 0)
  stopDate.setHours(23, 59, 59, 0)
  let dateArray = [];
  let currentDate = startDate;
  while (currentDate <= stopDate) {
    dateArray.push(new Date(currentDate));
    currentDate = addDays(new Date(currentDate), 1);
  }
  return dateArray;
}
