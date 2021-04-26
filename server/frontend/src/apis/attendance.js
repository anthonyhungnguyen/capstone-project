import axios from "axios"
import authHeader from "helpers/auth-header"
import { API_PATH } from "../constants/api"

export const fetchLogsStudent = userid => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.STUDENT_LOGS, {
        headers: { ...authHeader() },
        params: { userid: userid }
      })
      .then(response => resolve(response.data))
      .catch(error => reject(error))
  })
}

export const fetchLogsTeacher = userid => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.TEACHER_LOGS, {
        headers: { ...authHeader() },
        params: { teacherid: userid }
      })
      .then(response => resolve(response.data))
      .catch(error => reject(error))
  })
}
