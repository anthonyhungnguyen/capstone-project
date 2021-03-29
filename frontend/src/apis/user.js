import axios from "axios"
import { API_PATH } from "../constants/api"
export const loginApi = ({ userid, password }) =>
  new Promise((resolve, reject) => {
    axios
      .post(API_PATH.LOGIN, {
        userid,
        password
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })

export const logoutApi = () =>
  new Promise((resolve, reject) => {
    axios
      .post(API_PATH.LOGOUT)
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })

export const signUpApi = ({ id, userid, password }) =>
  new Promise((resolve, reject) => {
    axios
      .post(API_PATH.SIGNUP, { id, userid, password })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })
