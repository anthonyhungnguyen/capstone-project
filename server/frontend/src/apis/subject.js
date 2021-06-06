import axios from "axios"
import { API_PATH } from "constants/api"
import authHeader from "helpers/auth-header"

export const findAllSubjects = () => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.SUBJECT + "/all", {
        headers: { ...authHeader() }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(reject)
  })
}

export const findStudentCountForSubjectsByTeacherID = userid => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.SUBJECT + "/count", {
        params: {
          teacherid: userid
        },
        headers: { ...authHeader() }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(reject)
  })
}
