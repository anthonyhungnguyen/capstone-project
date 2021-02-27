import axios from "axios"
import authHeader from "helpers/auth-header"
import { API_PATH } from "../constants/api"

export const cropFaceApi = photo => {
  return new Promise((resolve, reject) => {
    axios
      .post(API_PATH.CROP_FACE, { data: photo })
      .then(response => {
        const cropPhoto = response.data
        resolve(cropPhoto)
      })
      .catch(error => {
        reject(error)
      })
  })
}

export const saveFace = ({ username, blob }) => {
  return new Promise((resolve, reject) => {
    const formData = new FormData()
    formData.append("image", blob)
    axios
      .post(API_PATH.ROOT_FACE, formData, {
        headers: {
          "content-type": "multipart/form-data",
          ...authHeader()
        },
        params: { username }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })
}

export const getFaces = username => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.ROOT_FACE, {
        headers: {
          ...authHeader()
        },
        params: {
          username
        }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(reject)
  })
}
