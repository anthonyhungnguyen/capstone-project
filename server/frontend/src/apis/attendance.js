import axios from "axios"
import authHeader from "helpers/auth-header"
import { firebase_storage } from "apis/firebase"
import { API_PATH } from "../constants/api"

export const fetchLogs = userid => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.LOGS, {
        headers: { ...authHeader() },
        params: { userid: userid }
      })
      .then(response => resolve(response.data))
      .catch(error => reject(error))
  })
}
