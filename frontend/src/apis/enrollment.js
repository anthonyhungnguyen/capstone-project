import axios from "axios"
import authHeader from "helpers/auth-header"
import { API_PATH } from "../constants/api"

export const findAllSubjectsEnrolledByUser = username => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.ENROLL + "/user", {
        params: { userid: username },
        headers: {
          ...authHeader()
        }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error.response.data)
      })
  })
}
