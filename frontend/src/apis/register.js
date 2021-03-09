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
