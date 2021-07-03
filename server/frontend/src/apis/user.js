import axios from "axios"
import authHeader from "helpers/auth-header"
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
export const verifyApi = () =>
  new Promise((resolve, reject) => {
    axios
      .get(API_PATH.VERIFY, { headers: { ...authHeader() } })
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

export const fetchUsersInfo = () =>
  new Promise((resolve, reject) => {
    axios
      .get(API_PATH.USER_ALL, { headers: { ...authHeader() } })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })

export const fetchUserInfo = userid =>
  new Promise((resolve, reject) => {
    axios
      .get(API_PATH.USER, {
        headers: { ...authHeader() },
        params: {
          id: userid
        }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })
