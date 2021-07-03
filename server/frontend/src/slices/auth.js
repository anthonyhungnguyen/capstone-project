import { createSlice } from "@reduxjs/toolkit"
import { loginApi, signUpApi, verifyApi } from "apis/user"
import { setMessage } from "./message"

// Slice

const userData = JSON.parse(localStorage.getItem("user"))

const slice = createSlice({
  name: "user",
  initialState: {
    user: userData ?? null,
    isLoggedIn: userData !== null
  },
  reducers: {
    loginSuccess: (state, action) => {
      state.isLoggedIn = true
      state.user = action.payload
      localStorage.setItem("user", JSON.stringify(action.payload))
    },
    loginFail: (state, _) => {
      state.isLoggedIn = false
      state.user = null
    },
    signUpSuccess: (state, _) => {
      state.isLoggedIn = false
    },
    signUpFail: (state, _) => {
      state.isLoggedIn = false
    },
    logOut: (state, _) => {
      state.isLoggedIn = false
      state.user = null
      localStorage.removeItem("user")
    }
  }
})

export default slice.reducer

// Actions

const {
  loginSuccess,
  loginFail,
  logOut,
  signUpSuccess,
  signUpFail
} = slice.actions

export const login = data => async dispatch => {
  return loginApi(data).then(
    result => {
      if (typeof result === "object") {
        dispatch(loginSuccess(result))
        return Promise.resolve()
      }
    },
    error => {
      dispatch(loginFail())
      dispatch(setMessage(error))
      return Promise.reject()
    }
  )
}

export const signup = data => async dispatch => {
  return signUpApi(data).then(
    () => {
      dispatch(signUpSuccess())
      return Promise.resolve()
    },
    error => {
      dispatch(signUpFail())
      dispatch(setMessage(error))
      return Promise.reject()
    }
  )
}

export const verify = () => async dispatch => {
  return verifyApi().then(
    () => {},
    error => {
      if (error.response.status === 401) {
        dispatch(logout())
      }
    }
  )
}

export const logout = () => dispatch => {
  dispatch(logOut())
}
