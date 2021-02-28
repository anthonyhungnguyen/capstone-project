import moment from "moment"

const DATE_FORMAT = "DD/MM/YYYY"

export const convertZoneDateTime = raw => {
  return moment(raw).format(DATE_FORMAT)
}
