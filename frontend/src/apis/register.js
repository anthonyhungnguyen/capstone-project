import axios from "axios"
import { API_PATH } from "constants/api"
import authHeader from "helpers/auth-header"

export const testPublishTopic = registerData => {
  return new Promise((resolve, reject) =>
    axios
      .post(API_PATH.TEACHER, registerData, {
        headers: {
          ...authHeader()
        }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(reject)
  )
}

export const fetchSchedules = ({ teacherid }) => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.TEACHER_SUBJECTS, {
        params: { teacherid: teacherid },
        headers: { ...authHeader() }
      })
      .then(response => resolve(response.data))
      .catch(reject)
  })
}

export const updateSchedule = schedule => {
  return new Promise((resolve, reject) => {
    axios
      .put(
        API_PATH.TEACHER,
        {
          ...schedule
        },
        { headers: { ...authHeader() } }
      )
      .then(response => resolve(response.data))
      .catch(reject)
  })
}

export const deleteSchedule = schedule => {
  return new Promise((resolve, reject) => {
    axios
      .delete(
        API_PATH.TEACHER,
        { ...schedule },
        { headers: { ...authHeader() } }
      )
      .then(response => resolve(response.data))
      .catch(reject)
  })
}

// "{"userID": 1752259, "semester": 201, "groupCode": "CC01", "timestamp": 1615562389727.7053, "deviceID": 1, "imgSrcBase64": "12321", "teacherID": 1}"
