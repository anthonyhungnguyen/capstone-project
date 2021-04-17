import { TimePicker } from "antd"
import axios from "axios"
import authHeader from "helpers/auth-header"
import { API_PATH } from "../constants/api"
import { firebase_storage } from "./firebase"

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

export const saveFace = ({ userid, blob }) => {
  return new Promise((resolve, reject) => {
    const formData = new FormData()
    formData.append("image", blob)
    axios
      .post(API_PATH.ROOT_FACE, formData, {
        headers: {
          "content-type": "multipart/form-data",
          ...authHeader()
        },
        params: { userid }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error)
      })
  })
}

export const getFaces = userid => {
  return new Promise((resolve, reject) => {
    axios
      .get(API_PATH.ROOT_FACE, {
        headers: {
          ...authHeader()
        },
        params: {
          userid
        }
      })
      .then(response => {
        resolve(response.data)
      })
      .catch(reject)
  })
}

export const fetchFaces = (userid, folder) => {
  return new Promise((resolve, reject) => {
    firebase_storage
      .ref(`/student/${userid}/${folder}/photos`)
      .list()
      .then(blob => {
        return blob.items.map(i => i.getDownloadURL())
      })
      .then(urlArray => Promise.all(urlArray).then(resolve))
  })
}

export const fetchFacesMetadata = (userid, folder) => {
  return new Promise((resolve, reject) => {
    firebase_storage
      .ref(`/student/${userid}/${folder}/photos`)
      .list()
      .then(blob => {
        return blob.items.map(i => i.getMetadata())
      })
      .then(urlArray => Promise.all(urlArray).then(resolve))
  })
}
