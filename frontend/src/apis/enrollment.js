import axios from "axios"
import authHeader from "helpers/auth-header"
import { API_PATH } from "../constants/api"

export const findAllSubjectsEnrolledByUser = userid => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.ENROLL + "/user", {
        params: { userid: userid },
        headers: {
          ...authHeader()
        }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })
}
