import axios from "axios"
import { API_PATH } from "../constants/api"
export const loginApi = ({ username, password }) =>
  new Promise((resolve, reject) => {
    axios
      .post(API_PATH.LOGIN, {
        username,
        password
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error.response.data)
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
        reject(error.response.data)
      })
  })

export const signUpApi = ({ id, username, password }) =>
  new Promise((resolve, reject) => {
    axios
      .post(API_PATH.SIGNUP, { id, username, password })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error.response.data)
      })
  })
